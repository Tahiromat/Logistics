import streamlit

from ui.home_page import HomePage
from ui.analytics_page import AnalyticsPage
from ui.algorithm_page import AlgorithmPage

def app():

   HomePage()
   AnalyticsPage()
   AlgorithmPage()
   


if __name__ == "__main__":
    app()
    