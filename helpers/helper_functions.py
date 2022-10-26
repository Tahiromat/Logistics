from helpers.constants import Constants
import ui
import folium
import pandas
import classes
import requests
import urllib.parse
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu


class HelperFunctions:
    def __init__(self, streamlit) -> None:
        self.streamlit = streamlit

    def page_configuration(self):
        self.streamlit.set_page_config(
            page_title="Air Quality", page_icon="❗", layout="wide"
        )
        self.streamlit.markdown(
            """ <style> [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;} </style> """,
            unsafe_allow_html=True,
        )
        hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
        self.streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)

    def __select_current_page(self):
        with self.streamlit.sidebar:
            selected_page = option_menu(
                "Main Menu",
                ["Home", "Analytics", "Algorithms"],
                icons=["house", "list-task", "gear"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
        return selected_page

    def sidebar_route(self):
        selected_page = self.__select_current_page()

        if selected_page == "Home":
            ui.HomePage(self.streamlit).home()
        elif selected_page == "Analytics":
            ui.AnalyticsPage(self.streamlit).analytics()
        else:
            ui.AlgorithmPage(self.streamlit).algorithm()

    def select_box_for_filter_country(self, dataframe, param):
        option = self.streamlit.selectbox(
            f"Filter by {param}",
            classes.PreProcessingClass(self.streamlit).find_unique_values(
                dataframe, param
            ),
        )
        return option

    def get_latitude_and_longitude(self, address):
        url = (
            "https://nominatim.openstreetmap.org/search/"
            + urllib.parse.quote(address)
            + "?format=json"
        )
        response = requests.get(url).json()
        return response[0]["lat"], response[0]["lon"]
       
    # CREATING DATAFRAMEs
    def create_dataframe_for_map(self, dataframe, param):
        dct = classes.PreProcessingClass(Constants().get_data_path()).get_unique_values_and_count_for_column(dataframe, param)
        new_dataframe = pandas.DataFrame()
        lat = []
        lon = []
        for key in dct.keys():
            latitude, longitude = self.get_latitude_and_longitude(key)
            lat.append(latitude)
            lon.append(longitude)
        
        new_dataframe["UniqueCountries"] = dct.keys()
        new_dataframe["TotalNumberofShipment"] = dct.values()
        new_dataframe["Latitude"] = lat
        new_dataframe["Longitude"] = lon
        new_dataframe.to_csv("data/dataframe_for_map.csv", index=False)


    def get_map(self, dataframe, latitude, longitude):
        total_shipment = list(dataframe["TotalNumberofShipment"])
        lat = list(dataframe[latitude])
        lon = list(dataframe[longitude])
        map = folium.Map(location=[dataframe[latitude].mean(), dataframe[longitude].mean()], zoom_start=6, tiles='OpenStreetMap',control_scale=True)
        
        for la, lo, to in zip(lat, lon, total_shipment):
            popup = folium.Popup(f"Total Shipments: {to}")
            map.add_child(folium.Marker(location=[la, lo], popup=popup, icon=folium.Icon(color="blue", icon="!")))        
        st_folium(map, width=1800, height=800)