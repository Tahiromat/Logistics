import pandas
import classes
import helpers


class HomePage:
    def __init__(self, streamlit):
        self.streamlit = streamlit

    def home(self):

        DATA_PATH = helpers.Constants().get_data_path()
        PPC = classes.PreProcessingClass(DATA_PATH)
        HF = helpers.HelperFunctions(self.streamlit)

        self.streamlit.title("HOME PAGE")

        data = PPC.read_data()
        data = PPC.add_date_features(data, "Scheduled Delivery Date")

        # option = HF.select_box_for_filter_country(data, "Country")

        # data = data[data["Country"] == option]

        self.streamlit.write(data)

        dct = PPC.get_unique_values_and_count_for_column(data, "Country")

        df = pandas.DataFrame()
        df["UniqueCountries"] = dct.keys()
        df["CountriesCounts"] = dct.values()


        for key in dct.keys():
            latitude, longitude = HF.get_latitude_and_longitude(key)
            df["Latitude"] = latitude
            df["Longitude"] = longitude

        self.streamlit.write(df)

        # helpers.HelperFunctions(self.streamlit).get_map(latitude, longitude)


        # Add all locations in to map and cretae popup for each country and show some of them also in graphs down of map
        # popup should include 
        #   - percantage per all countries (Yapılan işin toplan işe oranı her bir ülke bazında)
        #   - number of shipment and  distrubition of shipment categories
        #   - distrubition of shipment date based on quarters
        #   - min, max, average freight cost for specified date 
         