import numpy 
import pandas
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

DATA_SOURCE = "data/SCMS_Delivery_History_Dataset.csv"

data = pandas.read_csv(DATA_SOURCE)

def preprocess_inputs(df, label_mapping):

    df = df.copy()

    # Drop ID column
    df = df.drop("ID", axis=1)

    # Drop missing target rows
    missing_target_rows = df[df["Shipment Mode"].isna()].index
    df = df.drop(missing_target_rows, axis=0).reset_index(drop=True)

    # Fill missing values
    df["Dosage"] = df["Dosage"].fillna(df["Dosage"].mode()[0])
    df["Line Item Insurance (USD)"] = df["Line Item Insurance (USD)"].fillna(
        df["Line Item Insurance (USD)"].mean()
    )

    # Drop dates columns with too many missing values
    df = df.drop(["PQ First Sent to Client Date", "PO Sent to Vendor Date"], axis=1)

    # Extract date features
    for column in [
        "Scheduled Delivery Date",
        "Delivered to Client Date",
        "Delivery Recorded Date",
    ]:
        df[column] = pandas.to_datetime(df[column])
        df[column + " Year"] = df[column].apply(lambda x: x.year)
        df[column + " Month"] = df[column].apply(lambda x: x.month)
        df[column + " Day"] = df[column].apply(lambda x: x.day)
        df = df.drop(column, axis=1)

    # Drop numeric columns with too many missing values
    df = df.drop(["Weight (Kilograms)", "Freight Cost (USD)"], axis=1)

    # Drop high-cardinality columns with too many unique values
    df = df.drop(["PQ #", "PO / SO #", "ASN/DN #"], axis=1)

    # Binary encoding
    df["Fulfill Via"] = df["Fulfill Via"].replace({"Direct Drop": 0, "From RDC": 1})
    df["First Line Designation"] = df["First Line Designation"].replace(
        {"No": 0, "Yes": 1}
    )

    # One-Hot encoding for remaining categorical values except for the target column
    for column in df.select_dtypes("object").columns.drop("Shipment Mode"):
        dummies = pandas.get_dummies(df[column], prefix=column)
        df = pandas.concat([df, dummies], axis=1)
        df = df.drop(column, axis=1)

    # Split df into X and y
    y = df["Shipment Mode"]
    X = df.drop("Shipment Mode", axis=1)

    # encode the labels
    y = y.replace(label_mapping)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.7, shuffle=True, random_state=1
    )

    # Scale X
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = pandas.DataFrame(
        scaler.transform(X_train), index=X_train.index, columns=X_train.columns
    )
    X_test = pandas.DataFrame(
        scaler.transform(X_test), index=X_test.index, columns=X_test.columns
    )

    return X_train, X_test, y_train, y_test


LABEL_MAPPING = {"Air": 0, "Truck": 1, "Air Charter": 2, "Ocean": 3}
X_train, X_test, y_train, y_test = preprocess_inputs(
    df=data, label_mapping=LABEL_MAPPING
)

# print(X.isna().mean())
# print("\n")

# # Dictionary columns name and unique values count for that column
# dict = {column: len(X[column].unique()) for column in X.select_dtypes("object").columns}

"""
date_features = [
    # "PQ First Sent to Client Date",
    # "PO Sent to Vendor Date",
    "Scheduled Delivery Date",
    "Delivered to Client Date",
    "Delivery Recorded Date",
]

# Check the columns and percentage of the nan values based on specifik columns when compare the all values
for column in date_features:
    # coerce errors makes the not date values to nat (not a date ) value
    print(column, pandas.to_datetime(X[column], errors="coerce").isna().mean())
print("\n")"""


# print(X)

# print(dict)
# print("\n")

"""
# Check the like missing values in a column: like the column values should be integer but there are string values too. Then convert strings to nan end then find number of values of them. later you can drop or change values based on percentages of the values
for column in ["Weight (Kilograms)", "Freight Cost (USD)"]:
    print(X[column].apply(lambda x: numpy.NaN if not x.isnumeric() else x).isna().mean())
print("\n")
"""

"""# high cardinality columns has a lot of unique values; the propblem with them is the encoding could be difficult with them. And can actually slow-down the performans of the model.
print(pandas.get_dummies(X["ASN/DN #"]))
print("\n")"""

# print(X.select_dtypes("object"))
# print("\n")


# print(X["Fulfill Via"])
# print("\n")
# print(X["First Line Designation"])


# print(X_train)
# print(y_train.value_counts().index)
# print(y_train)


# print((X_train.shape(2)))

inputs = tf.keras.Input(shape=(771,))
x = tf.keras.layers.Dense(128, activation="relu")(inputs)
x = tf.keras.layers.Dense(128, activation="relu")(x)
outputs = tf.keras.layers.Dense(4, activation="softmax")(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    batch_size=32,
    epochs=100,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=15, restore_best_weights=True
        )
    ],
)

y_pred = numpy.argmax(model.predict(X_test), axis=1)

cm = confusion_matrix(y_test, y_pred, labels=list(LABEL_MAPPING.values()))
clr = classification_report(y_test, y_pred, labels=list(LABEL_MAPPING.values()), target_names=list(LABEL_MAPPING.keys()))

print("Test Set Accuracy: {:.2f}%".format(model.evaluate(X_test, y_test, verbose=0)[1] * 100))

plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True, fmt='g', vmin=0, cmap='Blues', cbar=False)
plt.xticks(ticks=[0.5, 1.5, 2.5, 3.5], labels=list(LABEL_MAPPING.keys()))
plt.yticks(ticks=[0.5, 1.5, 2.5, 3.5], labels=list(LABEL_MAPPING.keys()))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

print("Classification Report:\n----------------------\n", clr)