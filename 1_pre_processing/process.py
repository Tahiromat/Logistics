import pandas
import numpy 
from sklearn.model_selection import train_test_split

DATA_SOURCE = "/home/tahir/Projects/Logistic/0_data/SCMS_Delivery_History_Dataset.csv"

data = pandas.read_csv(DATA_SOURCE)

print(data.info())
print("\n")


def preprocess_inputs(df):

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
    df["First Line Designation"] = df["First Line Designation"].replace({"No": 0, "Yes": 1})

    # One-Hot encoding for remaining categorical values except for the target column
    for column in df.select_dtypes("object").columns.drop("Shipment Mode"):
        dummies = pandas.get_dummies(df[column], prefix=column)
        df = pandas.concat([df, dummies], axis=1)
        df = df.drop(column, axis=1)



    # Split df into X and y
    y = df["Shipment Mode"]
    X = df.drop("Shipment Mode", axis=1)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)

    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = preprocess_inputs(data)

# print(X.isna().mean())
# print("\n")

# # Dictionary columns name and unique values count for that column
# dict = {column: len(X[column].unique()) for column in X.select_dtypes("object").columns}

"""date_features = [
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

print(dict)
print("\n")

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


print(X_train)


