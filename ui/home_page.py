import classes
import helpers


class HomePage:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    def home(self):

        self.streamlit.title("HOME PAGE")

        data = classes.PreProcessingClass(helpers.Constants().get_data_path()).read_data()

        self.streamlit.write(data.head())
