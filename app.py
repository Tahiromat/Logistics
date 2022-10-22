""" Summary_:
        The app will be start from here.
"""

import ui
import streamlit
from streamlit_option_menu import option_menu

streamlit.set_page_config(page_title="Air Quality", page_icon="❗", layout="wide")
streamlit.markdown(
    """ <style> [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;} </style> """,
    unsafe_allow_html=True,
)
hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)

with streamlit.sidebar:
    selected_page = option_menu(
        "Main Menu",
        ["Home", "Analytics", "Algorithms"],
        icons=["house", "list-task", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )


def main():

    if selected_page == "Home":
        ui.HomePage(streamlit).home()
    elif selected_page == "Analytics":
        ui.AnalyticsPage(streamlit).analytics()
    else:
        ui.AlgorithmPage(streamlit).algorithm()


if __name__ == "__main__":
    main()
