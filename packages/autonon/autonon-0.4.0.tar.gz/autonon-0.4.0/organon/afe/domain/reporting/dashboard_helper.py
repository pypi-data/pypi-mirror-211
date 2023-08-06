"""This module includes helper function for creating dashboards with plotly."""
import math
import textwrap
from typing import List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes, BarContainer
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.table import Table
from matplotlib.widgets import Button

ORG_COLOR_HEX = "#2D1A44"


# ax kıslatması bir convention
# pylint: disable=invalid-name

def get_bar_chart(x_vals: List[str], y_vals: List[int or float], label="", ax: Axes = None) -> BarContainer:
    """
    Creates a bar chart with given bar names and values
    :param x_vals: Names of bars
    :param y_vals: Values of bars
    :param label: Bar chart title
    :param ax: Axes object where bar chart will be added
    :return: Matplotlib bar container with given values
    """
    ax = ax or plt.gca()
    bar_container = ax.bar(x_vals, y_vals, label=label)
    for index_elem in enumerate(ax.get_xticks()):
        i = index_elem[0]
        ax.text(i, y_vals[i] / 2, y_vals[i], horizontalalignment='center',
                verticalalignment='center', color='white')
    return bar_container


def get_line_scatter_plot(x_vals: List[int or float], y_vals: List[int or float], title: str = None,
                          ax: Axes = None, color=None) -> Line2D:
    """
    Creates a line plot where data points are marked
    :param x_vals: X axis values of data points
    :param y_vals: Y axis values of data points
    :param title: Title of plot
    :param ax: Axes object where bar chart will be added
    :param color: color of plot
    :return: Line2D object with given values
    """
    ax = ax or plt.gca()
    if color is None:
        plot = ax.plot(x_vals, y_vals, label=title, marker=".")
    else:
        plot = ax.plot(x_vals, y_vals, label=title, marker=".", color=color)
    return plot


class TablePagination:
    """Converts a matplotlib table to a paginated table"""

    def __init__(self, ax: Axes, table: Table, data=List[List[str or int or float]], rows_per_page=8):
        self.current_page_index = 0
        self.table = table
        self.ax = ax or plt.gca()
        self.data = data
        self.num_rows = len(data)
        self.rows_per_page = rows_per_page
        self.current_data = []
        self.num_pages = math.ceil(self.num_rows / self.rows_per_page)
        self.cells = table.get_celld()
        self.pages_text = ax.annotate(f"Page 1/{self.num_pages}", xy=(0, 0),
                                      xycoords='axes fraction', fontsize=self.cells[(0, 0)].get_fontsize(),
                                      weight='bold', )
        self.btn_prev = None
        self.btn_next = None

    def next(self, event):  # pylint: disable=unused-argument
        """This method should be called for passing to next page of table.
        Can be used as a callback in button on_clicked methods."""
        if self.current_page_index < self.num_pages - 1:
            self.current_page_index += 1
            self._update_rows()
            self._update_texts()
            plt.draw()

    def prev(self, event):  # pylint: disable=unused-argument
        """This method should be called for returning to previous page of table.
        Can be used as a callback in button on_clicked methods."""
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self._update_rows()
            self._update_texts()
            plt.draw()

    def _update_texts(self):
        """Updates texts in table cells according to values in current page"""
        col_num = len(self.data[0])
        for i in range(1, len(self.current_data) + 1):
            for j in range(col_num):
                txt = _wrap_text_for_table(self.current_data[i - 1][j])
                self.cells[(i, j)].set_text_props(text=txt)
        for i in range(len(self.current_data) + 1, self.rows_per_page + 1):
            for j in range(col_num):
                self.cells[(i, j)].set_text_props(text="")
        self.pages_text.set_text(f"Page {self.current_page_index + 1}/{self.num_pages}")

    def _update_rows(self):
        """Sets currently shown data according to page number"""
        lower = self.current_page_index * self.rows_per_page
        upper = min((self.current_page_index + 1) * self.rows_per_page, self.num_rows)
        self.current_data = self.data[lower:upper]

    def add_buttons(self, fig: Figure, btn_width=0.05, btn_height=0.035):
        """Adds prev/next buttons under the table"""
        bbox = self.ax.get_position()

        prev_left = bbox.x1 - 3 * btn_width
        prev_bottom = bbox.y0 - 1 * btn_height
        axprev = fig.add_axes([prev_left, prev_bottom, btn_width, btn_height])

        next_left = prev_left + 1.3 * btn_width
        next_bottom = prev_bottom
        axnext = fig.add_axes([next_left, next_bottom, btn_width, btn_height])

        self.btn_prev = Button(axprev, "Previous")
        self.btn_next = Button(axnext, "Next")

        self.btn_prev.on_clicked(self.prev)
        self.btn_next.on_clicked(self.next)


def get_data_table_plot(data_frame: pd.DataFrame, ax: Axes = None, rows_per_page=10):
    """
    Creates a paginated data table from given data frame
    :param data_frame: Data to be demonstrated as table
    :param ax: Axes object where bar chart will be added
    :param rows_per_page: Rows to be shown in 1 page
    :return:
    """
    ax = ax or plt.gca()

    rows = data_frame.values.tolist()

    headers = data_frame.columns

    cell_texts = [[_wrap_text_for_table(txt) for txt in txts] for txts in rows[0:rows_per_page]]

    table = ax.table(
        cellText=cell_texts,
        colLabels=headers,
        colColours=[ORG_COLOR_HEX] * len(headers),
        loc='center',
        cellLoc='left')
    table.PAD = 0
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(data_frame.columns))))
    header_cell_indices = [(0, i) for i in range(len(data_frame.columns))]
    cells = table.get_celld()
    table.scale(1, 2)
    for cell in cells.values():
        cell.PAD = 0.03
    for header_cell in header_cell_indices:
        cells[header_cell].set_text_props(color="white")

    pagin_table = TablePagination(ax, table, rows, rows_per_page=rows_per_page)

    return pagin_table


def set_date_ticker(ax: Axes):
    """Adjusts x-axis ticks for time series plots"""
    ax = ax or plt.gca()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = ['%Y',
                         '%b',
                         '%d',
                         '%H:%M',
                         '%H:%M:%S',
                         '%H:%M:%S.%f',
                         ]

    formatter.zero_formats = [''] + formatter.formats[:-1]

    formatter.zero_formats[3] = '%d-%b'

    formatter.offset_formats = ['',
                                '%Y',
                                '%b %Y',
                                '%d %b %Y',
                                '%d %b %Y',
                                '%d %b %Y']
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')


def _wrap_text_for_table(txt: str, max_line_length=30) -> str:
    return '\n'.join(textwrap.wrap(txt, max_line_length, break_long_words=True))


def wrap_labels(ax, width, break_long_words=False, axis="x"):
    """Wraps text labels in given axis"""
    labels = []
    if axis == "x":
        for label in ax.get_xticklabels():
            text = label.get_text()
            labels.append(textwrap.fill(text, width=width,
                                        break_long_words=break_long_words))
        ax.set_xticklabels(labels, rotation=0)
    if axis == "y":
        y_labels = []
        for label in ax.get_yticklabels():
            text = label.get_text()
            y_labels.append(textwrap.fill(text, width=width,
                                          break_long_words=break_long_words))
        ax.set_yticklabels(y_labels, rotation=0)
