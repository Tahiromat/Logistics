import pandas


class PreProcessingMethod:
    def __init__(self, data: pandas.DataFrame):
        self.data = data

    # create a method check if missing values percentage is too many then drop the row or columns based on their percentages

    def drop_unused_columns(self):
        pass

    def drop_columns_with_too_many_missing_values(self):
        pass

    def drop_high_cardinality_columns(self):
        pass

    def fill_categorical_columns_missing_values(self):
        pass

    def fill_numerical_columns_missing_values(self):
        pass

    def transform_binary_encoding(self):
        pass 


    

    def transform_on_hot_encoding(self):
        pass

    def normalize_all_numeric_values():
        pass

    def split_data_into_x_and_y(self):
        pass

    def split_data_into_train_and_test(self):
        pass
