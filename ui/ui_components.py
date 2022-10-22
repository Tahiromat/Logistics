import streamlit
from streamlit_option_menu import option_menu


class UIComponents:
    def __init__(self):
        pass

    def create_title(self, title: str = ""):
        return streamlit.title(title)

    def create_subtitle(self, subtitle: str = ""):
        return streamlit.subtitle(subtitle)

    def create_sidebar(self):
        sidebar = streamlit.sidebar.title("Sidebar Title")
        return sidebar
