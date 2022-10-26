import pandas
import numpy
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class PreProcessingClass:

    """
    The method purpose is the pre-processing data from the given data source
    """

    def __init__(self, data_path):
        self.data_path = data_path

    def __change_dtype_from_object_to_datetime(self, dataframe, param):
        return pandas.to_datetime(dataframe[param])

    def find_unique_values(self, dataframe, param):
        return dataframe[param].unique()

    def __find_unique_counts(self, dataframe, param, unique):
        return list(dataframe[param]).count(unique)

    def read_data(self):
        return pandas.read_csv(self.data_path)

    def drop_unused_columns(self, columns: list = []):
        data = self.read_data()
        return data.drop(columns, axis=1)

    def drop_missign_rows(self, missing_target_rows):
        data = self.read_data()
        return data.drop(missing_target_rows, axis=0).reset_index(drop=True)

    def drop_missing_target_rows(self, target_column):
        data = self.read_data()
        missing_target_rows = data[data[target_column].isna()].index
        return self.drop_missign_rows(missing_target_rows)

    def check_number_of_missing_dates(self, date_features: list = []):
        data = self.read_data()
        columns_should_delete = []

        for column in date_features:
            col_name_missing_rate_list = [
                column,
                pandas.to_datetime(data[column], errors="coerce").isna().mean(),
            ]

            if col_name_missing_rate_list[1] > 0.2:
                columns_should_delete.append(column)
        return self.drop_unused_columns(columns_should_delete)

    def get_unique_values_and_count_for_column(self, dataframe, param):
        dct = {}
        unique_values = self.find_unique_values(dataframe, param)
        for unique in unique_values:
            count_of_unique_value = self.__find_unique_counts(dataframe, param, unique)
            dct[str(unique)] = count_of_unique_value
        return dct

    def add_date_features(self, dataframe, param):
        dataframe[param] = self.__change_dtype_from_object_to_datetime(dataframe, param)
        dataframe["YEAR"] = dataframe[param].apply(lambda x: x.year)
        dataframe["MONTH"] = dataframe[param].apply(lambda x: x.month)
        dataframe["QUARTER"] = dataframe[param].apply(lambda x: x.quarter)
        dataframe["DAY"] = dataframe[param].apply(lambda x: x.day)
        return dataframe

    def drop_numeric_columns_with_too_many_missing_values(
        self, date_features: list = []
    ):
        data = self.read_data()
        columns_should_delete = []

        for column in date_features:
            col_name_missing_rate = (
                data[column]
                .apply(lambda x: numpy.NaN if not x.isnumeric() else x)
                .isna()
                .mean()
            )

            if col_name_missing_rate > 0.25:
                columns_should_delete.append(column)
        return self.drop_unused_columns(columns_should_delete)

    def find_high_cardinality_columns(self) -> dict:
        data = self.read_data()
        dict = {
            column: len(data[column].unique())
            for column in data.select_dtypes("object").columns
        }
        mean = sum(list(dict.values())) / len(list(dict.values()))
        columns_should_delete = []

        for k, v in zip(list(dict.keys()), list(dict.values())):
            if v > mean * 4:
                columns_should_delete.append(k)

        print(
            f"\n\n You should drop {columns_should_delete} columns because of high cardinality for model \n\n"
        )
        return dict

    def fill_categorical_columns_missing_values(self):
        pass

    def fill_numerical_columns_missing_values(self):
        pass

    def transform_binary_encoding(self):
        pass

    def transform_on_hot_encoding(self, target_column):
        data = self.read_data()
        for column in data.select_dtypes("object").columns.drop(target_column):
            dummies = pandas.get_dummies(data[column], prefix=column)
            data = pandas.concat([data, dummies], axis=1)
            return data.drop(column, axis=1)

    def split_data_into_x_and_y(self, target_column):
        data = self.read_data()
        y = data[target_column]
        X = data.drop(target_column, axis=1)
        return X, y

    def split_data_into_train_and_test(self, target_column):
        X, y = self.split_data_into_x_and_y(target_column)
        return train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)

    def normalize_all_numeric_values(self, target_column):
        X_train, X_test, y_train, y_test = self.split_data_into_train_and_test(
            target_column
        )
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = pandas.DataFrame(
            scaler.transform(X_train), index=X_train.index, columns=X_train.columns
        )
        X_test = pandas.DataFrame(
            scaler.transform(X_test), index=X_test.index, columns=X_test.columns
        )
        return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    PPC = PreProcessingClass(
        "/home/tahir/Projects/Logistic/data/SCMS_Delivery_History.csv"
    )

    data = PPC.read_data()

    print(data.isna().mean())
    # data.to_csv("/home/tahir/Projects/Logistic/data/SCMS_Delivery_History.csv", index=False)
