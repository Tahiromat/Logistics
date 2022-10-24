import ui
import folium
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





    def get_map(self, latitude, longitude):
        map = folium.Map(location=[latitude,longitude], zoom_start=14, tiles='OpenStreetMap',control_scale=True)
        popup = folium.Popup(f"""<br/> This is a new line<br/>""",height= 200, width= 400)
        map.add_child(folium.Marker(location= [latitude,longitude], popup=popup, icon=folium.Icon(color="blue", icon="home")))
        st_folium(map, width=400, height=400)
 
       
