import classes
import helpers
# import streamlit

DATA_PATH = helpers.Constants().get_data_path()

class HomePage:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    def home(self):

        self.streamlit.title("HOME PAGE")

        data = classes.PreProcessingClass(
            DATA_PATH
        ).read_data()
        data = classes.PreProcessingClass(DATA_PATH).add_date_features(data, "Scheduled Delivery Date")

        option = helpers.HelperFunctions(self.streamlit).select_box_for_filter_country(data, "Country")


        data = data[data["Country"] == option]

        self.streamlit.write(data)

        dct = classes.PreProcessingClass(DATA_PATH).get_unique_values_and_count_for_column(data, "Country")
        
        self.streamlit.write(dct)

        for key in dct.keys():
            latitude, longitude = helpers.HelperFunctions(self.streamlit).get_latitude_and_longitude(key)
            
            self.streamlit.write(key, latitude, longitude)