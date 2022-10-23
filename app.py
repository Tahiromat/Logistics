""" Summary_:
        The app will be start from here.
"""

import helpers
import streamlit


def main():

    helpers.HelperFunctions(streamlit).page_configuration()
    helpers.HelperFunctions(streamlit).sidebar_route()


if __name__ == "__main__":
    main()
