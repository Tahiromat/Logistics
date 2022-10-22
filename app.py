""" Summary_:
        The app will be start from here.
"""

import ui
import streamlit
from streamlit_option_menu import option_menu

with streamlit.sidebar:
    selected_page = option_menu("Main Menu", ["Home", 'Analytics', 'Algorithms'], 
        icons=['house', 'list-task', 'gear'], menu_icon="cast", default_index=0, orientation="vertical")

if selected_page == "Home":
        ui.HomePage(streamlit).home()
elif selected_page == "Analytics":
        ui.AnalyticsPage(streamlit).analytics()
else:
        ui.AlgorithmPage(streamlit).algorithm()

