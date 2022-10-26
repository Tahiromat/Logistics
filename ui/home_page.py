import classes
import helpers




class HomePage:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    def home(self):

        DATA_PATH = helpers.Constants().get_data_path()
        MAP_DATA_PATH = helpers.Constants().get_map_data_path()

        self.streamlit.title("HOME PAGE")

        map_data = classes.PreProcessingClass(MAP_DATA_PATH).read_data()
        helpers.HelperFunctions(self.streamlit).get_map(map_data, "Latitude", "Longitude")



