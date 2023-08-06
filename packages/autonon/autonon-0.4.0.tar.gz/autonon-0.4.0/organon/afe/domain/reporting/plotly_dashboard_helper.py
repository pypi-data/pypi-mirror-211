"""This module includes helper function for creating dashboards with plotly."""
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Tuple

import pandas as pd
import plotly.graph_objects as go
import six
from plotly.basedatatypes import BaseTraceType
from plotly.subplots import make_subplots

ORG_COLOR_HEX = "#2D1A44"


def open_html_in_browser(html, using=None, new=0, autoraise=True):
    """
    Display html in a web browser without creating a temp file.

    Instantiates a trivial http server and uses the webbrowser module to
    open a URL to retrieve html from that server.

    Parameters
    ----------
    html: str
        HTML string to display
    using, new, autoraise:
        See docstrings in webbrowser.get and webbrowser.open
    """
    if isinstance(html, six.string_types):
        html = html.encode("utf8")

    class OneShotRequestHandler(BaseHTTPRequestHandler):
        """Simple http request handler"""
        def do_GET(self):   # pylint: disable=invalid-name
            """Returns html string as response"""
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            buffer_size = 1024 * 1024
            for i in range(0, len(html), buffer_size):
                self.wfile.write(html[i: i + buffer_size])

        def log_message(self, _format, *args):  # pylint: disable=arguments-differ
            """Silence stderr logging"""

    server = HTTPServer(("127.0.0.1", 0), OneShotRequestHandler)
    webbrowser.get(using).open(f"http://127.0.0.1:{server.server_port}", new=new, autoraise=autoraise)
    server.handle_request()


def figures_to_html(figs):
    """Merge figure html strings in single html string"""
    html_str = "<html><head></head><body>\n"
    for fig in figs:
        html_str += fig.to_html().split('<body>')[1].split('</body>')[0]
    html_str += "</body></html>\n"
    return html_str


def get_line_scatter_plot(x_vals, y_vals, title: str = None) -> go.Scatter:
    """
    Creates a line plot where data points are marked
    :param y_vals: Y axis values of data points
    :param x_vals: X axis values of data points
    :param title: Title of plot
    :return: Plotly Scatter object with given values
    """
    trace = go.Scatter(x=x_vals, y=y_vals, name=title, mode="markers+lines")
    return trace


def get_data_table_plot(data_frame: pd.DataFrame) -> go.Table:
    """
    Creates plotly table from given data frame
    :param data_frame:
    :return:
    """
    columns = list(data_frame.columns)

    row_even_color = 'lightgrey'
    row_odd_color = 'white'

    table = go.Table(
        header=dict(
            values=[f"<b>{col}</b>" for col in columns],
            line_color='darkslategray',
            fill_color=ORG_COLOR_HEX,
            align=['left', 'center'],
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[data_frame[col] for col in columns],
            line_color='darkslategray',
            # 2-D list of colors for alternating rows
            fill_color=[[row_odd_color, row_even_color, row_odd_color, row_even_color,
                         row_odd_color] * len(data_frame.index)],
            align=['left', 'center'],
            font=dict(color='darkslategray', size=10)
        )

    )

    return table


def get_bar_chart(x_vals: List, y_vals: List) -> go.Bar:
    """
    Creates a bar chart with given bar names and values
    :param x_vals: Names of bars
    :param y_vals: Values of bars
    :return: Plotly Bar object with given values
    """
    bar_chart = go.Bar(x=x_vals, y=y_vals)
    return bar_chart


def get_bar_chart_with_width(sorted_bin_limits: List[float], sorted_bin_values: List[float]) \
        -> Tuple[go.Bar, Tuple[float, float], Tuple[float, float]]:
    """Creates bar chart with adjacent bars
    :param sorted_bin_limits: upper limits of bars
    :param sorted_bin_values: values of bars
    :return: Plotly Bar object with given values
    """
    widths = []
    x_vals = []
    y_vals = []
    customdata = []

    for i, limit in enumerate(sorted_bin_limits):
        if i == 0:
            continue
        width = limit - sorted_bin_limits[i - 1]
        widths.append(width)
        y_vals.append(sorted_bin_values[i - 1])
        x_vals.append(limit - width / 2)
        customdata.append(f"({sorted_bin_limits[i - 1]}, {limit})")

    # y_vals = [(-1) ** i * val for i, val in enumerate(y_vals)]

    # calculate y range
    maxy = max(y_vals)
    miny = min(y_vals)
    gap = maxy - miny
    y_min_range = min(0.0, miny - 0.1 * gap)
    y_max_range = max(0.0, maxy + 0.1 * gap)
    y_range = (y_min_range, y_max_range)

    if len(widths) < 3:
        scale_width = min(widths)
    else:
        scale_width = max(widths[1:-1])

    allowed_max_width = scale_width * 100

    x_min_range = sorted_bin_limits[0]
    x_max_range = sorted_bin_limits[-1]

    if widths[0] > allowed_max_width:
        widths[0] = allowed_max_width
        second_bin_start = x_vals[1] - widths[1] / 2
        x_vals[0] = second_bin_start - allowed_max_width / 2
        x_min_range = second_bin_start - scale_width * 2
    if widths[-1] > allowed_max_width:
        widths[-1] = allowed_max_width
        prev_last_bin_end = x_vals[-2] + widths[-2] / 2
        x_vals[-1] = prev_last_bin_end + allowed_max_width / 2
        x_max_range = prev_last_bin_end + scale_width * 2

    extra_space_length = 0.1 * (x_max_range - x_min_range)
    x_min_range -= extra_space_length
    x_max_range += extra_space_length
    x_range = (x_min_range, x_max_range)

    bar_chart = go.Bar(
        x=x_vals,
        y=y_vals,
        customdata=customdata,
        width=widths,
        hovertemplate=
        '%{customdata}' +
        '<extra><b>%{y}</b></extra>'
    )
    return bar_chart, x_range, y_range

    # return show_plot([bar], title, x_axis_title, y_axis_title, x_range, y_range)


# pylint: disable=too-many-arguments
def create_figure(traces: List[BaseTraceType], title=None, x_axis_title=None, y_axis_title=None, x_range=None,
                  y_range=None) -> go.Figure:
    """
    Creates a plotly figure with given traces
    :param traces: plotly objects to be included in figure
    :param title: title of figure
    :param x_axis_title:  x axis label
    :param y_axis_title: y axis label/s
    :param x_range: x axis range to be shown
    :param y_range: y axis range to be shown
    :return:
    """
    if len(traces) == 2:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            traces[0],
            secondary_y=False
        )
        fig.add_trace(
            traces[1],
            secondary_y=True
        )
    else:
        fig = go.Figure()
        for trace in traces:
            fig.add_trace(trace)
    if title:
        fig.update_layout(title=title)
    if x_axis_title:
        fig.update_layout(xaxis_title=x_axis_title)
    if y_axis_title:
        if isinstance(y_axis_title, list):
            fig.update_yaxes(title_text=y_axis_title[0], secondary_y=False)
            fig.update_yaxes(title_text=y_axis_title[1], secondary_y=True)
        else:
            fig.update_layout(yaxis_title=y_axis_title)
    if x_range:
        fig.update_layout(xaxis={"range": x_range})
    if y_range:
        fig.update_layout(yaxis={"range": y_range})

    return fig
