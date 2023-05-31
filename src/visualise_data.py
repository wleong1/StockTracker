from bokeh.plotting import figure, show
import numpy as np
from process_data import read_data_from_csv
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.resources import CDN
from bokeh.embed import file_html

PLOT_HEIGHT = 700
PLOT_WIDTH = 1100


class VisualiseData:
    """Converts csv file into plots"""

    # Create Plot/Figure
    @staticmethod
    def plotting_data(filename):
        dates = np.array(filename["date"], dtype=np.datetime64)
        source = ColumnDataSource(data=dict(date=dates, close=filename["close"]))

        p = figure(height=PLOT_HEIGHT, width=PLOT_WIDTH, tools="xpan, hover", toolbar_location=None, #TODO:CHANGE THE HOVER TO MAKE IT ONLY SHOW DATE AND PRICE
                   x_axis_type="datetime", x_axis_location="below", x_range=(dates[250], dates[-1]),
                   background_fill_color="#efefef")

        p.line("date", "close", source=source)
        p.yaxis.axis_label = "Price"

        html = file_html(p, CDN, "my_plot")

        return html

