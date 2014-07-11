#!/usr/bin/python2

"""Small tool to generate example reports."""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from layout import ColumnLayout
from layout import FixedSizeLayout
from layout import HideOutsideLayout
from layout import PaddingLayout
from layout import RowLayout
from layout import TableLayout
from style import EmptyStyle, FixedStyle, TableStyle
from table import Table
import xls


RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'


def main():
  workbook = xls.new_workbook('my_file.xlsx')

  # Styles used for the tables below.
  EMPTY_STYLE = EmptyStyle(workbook)
  RED_STYLE = FixedStyle(workbook, 'Red', RED)
  GREEN_STYLE = FixedStyle(workbook, 'Green', GREEN)
  BLUE_STYLE = FixedStyle(workbook, 'Blue', BLUE)

  # First, one sheet with static data.
  sheet = workbook.add_worksheet('FixedData')
  layout = FixedSizeLayout(GREEN_STYLE, 2, 2)
  start_position = (0, 0)
  layout.draw(sheet, start_position)

  # Now another sheet with table data.
  table = Table('Table', ['Col1', 'Col2', 'Col3'])
  table.add_row(['a', 'b', 'c'])
  table.add_row(['d', 'e', 'f'])
  sheet = workbook.add_worksheet('TableData')
  style = TableStyle(workbook, table)
  layout = TableLayout(style, table)
  start_position = (1, 1)  # Leave an empty column and row.
  layout.draw(sheet, start_position)

  # Now a complicated layout, with two rows.

  # Row 1 has three fixed layouts.
  layout_1_1 = FixedSizeLayout(RED_STYLE, 2, 2)
  layout_1_2 = FixedSizeLayout(RED_STYLE, 2, 3)
  layout_1_3 = FixedSizeLayout(RED_STYLE, 4, 2)
  layout_1 = RowLayout(EMPTY_STYLE, [layout_1_1, layout_1_2, layout_1_3])

  # Row 2 has a fixed layout and a column layout. The column has 2 elements.
  layout_2_2_1 = FixedSizeLayout(BLUE_STYLE, 1, 1)
  layout_2_2_2 = FixedSizeLayout(BLUE_STYLE, 4, 1)
  layout_2_2 = ColumnLayout(EMPTY_STYLE, [layout_2_2_1, layout_2_2_2])
  layout_2_1 = FixedSizeLayout(GREEN_STYLE, 3, 3)
  layout_2 = RowLayout(EMPTY_STYLE, [layout_2_1, layout_2_2])

  sheet = workbook.add_worksheet('Layouts')
  layout = ColumnLayout(EMPTY_STYLE, [layout_1, layout_2])
  start_position = (0, 0)
  layout.draw(sheet, start_position)

  # A sheet with a single visible layout and hidden cells outside.
  sheet = workbook.add_worksheet('Hidden')
  child_layout = FixedSizeLayout(GREEN_STYLE, 4, 4)
  padding_layout = PaddingLayout(RED_STYLE, child_layout, 1, 1, 1, 1)
  layout = HideOutsideLayout(EMPTY_STYLE, padding_layout)
  start_position = (0, 0)
  layout.draw(sheet, start_position)

  workbook.close()


if __name__ == '__main__':
  main()
