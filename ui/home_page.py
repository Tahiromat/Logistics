import classes
import helpers




class HomePage:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    def home(self):

        DATA_PATH = helpers.Constants().get_data_path()
        MAP_DATA_PATH = helpers.Constants().get_map_data_path()

        self.streamlit.title("HOME PAGE")

        original_data = classes.PreProcessingClass(DATA_PATH).read_data()
        map_data = classes.PreProcessingClass(MAP_DATA_PATH).read_data()


        helpers.HelperFunctions(self.streamlit).get_map(map_data, "Latitude", "Longitude")


        column1, column2 = self.streamlit.columns(2)
        with column1:
            classes.AnalyticsClass(self.streamlit, original_data).create_histogram_chart(x_axis = "Shipment Mode")
        with column2:
            classes.AnalyticsClass(self.streamlit, map_data.iloc[:10]).create_pie_chart(values="TotalNumberofShipment", names="UniqueCountries")


        self.streamlit.write(original_data)

