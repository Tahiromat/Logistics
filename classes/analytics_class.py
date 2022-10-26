import pandas
import plotly.express


class AnalyticsClass:
    def __init__(self, streamlit, dataframe):
        self.streamlit = streamlit
        self.dataframe = dataframe

    def __plotly_chart(self, figure):
        self.streamlit.plotly_chart(figure)

    def create_line_chart(self, x_axis, y_axis: list = [], title: str = ""):
        figure = plotly.express.line(self.dataframe, x=x_axis, y=y_axis, title=title)
        self.__plotly_chart(figure)

    def create_scatter_chart(self, x_axis, y_axis):
        pass

    def create_pie_chart(self, values, names):
        figure = plotly.express.pie(
            values=self.dataframe[values], names=self.dataframe[names]
        )
        self.__plotly_chart(figure)

    def create_histogram_chart(self, x_axis):
        figure = plotly.express.histogram(self.dataframe, x=x_axis)
        self.__plotly_chart(figure)
