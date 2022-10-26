class UpdateDataframes:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    # UPDATE ORIGINAL DATAFRAME
    def update_origial_dataframe(self):
        self.streamlit.write("UPDATING ORIGINAL DATAFRAME")

    # UPDATE DATAFRAME FOR MAP
    def update_map_dataframe(self):
        self.streamlit.write("UPDATING MAP DATAFRAME")

    # UPDATE DATAFRAME FOR PIE CHART
    def update_pie_chart_dataframe(self):
        self.streamlit.write("UPDATING PIE CHART DATAFRAME")
