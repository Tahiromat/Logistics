import streamlit
import classes
import helpers


class HomePage:
    def __init__(self):
        pass

    streamlit.title("HOME PAGE")

    data = classes.PreProcessingClass(helpers.Constants().get_data_path()).read_data()

    streamlit.write(data.head())
