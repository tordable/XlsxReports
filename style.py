"""A style is a set of configuration to draw a layout.

This module contains the base style as well as a variety of example styles.
"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


class Style(object):
  """A style contains configuration for drawing a layout."""

  def __init__(self, workbook):
    self._format = workbook.add_format()

  def get_cell_content(self, column_index, row_index):
    pass

  def get_cell_format(self, column_index, row_index):
    return self._format


class EmptyStyle(Style):
  """A style which doesn't have any content or format data."""

  def __init__(self, workbook):
    super(EmptyStyle, self).__init__(workbook)


class FixedStyle(Style):
  """A style which uses the given content and color for all cells."""

  def __init__(self, workbook, content, background_color=None):
    """Builds a FixedStyle using the given parameters.

    @param background_color: The background color of the cell in #RRGGBB
    format.
    """
    super(FixedStyle, self).__init__(workbook)

    self.content = content

    if background_color:
      self._format.set_bg_color(background_color)

  def get_cell_content(self, column_index, row_index):
    return self.content


class TableStyle(Style):
  """A style with configuration for drawing a table in a layout."""

  def __init__(self, workbook, table):
    super(TableStyle, self).__init__(workbook)

    self.table = table

  def get_cell_content(self, column_index, row_index):
    if row_index == 0:
      # Return the header value.
      return self.table.column_names[column_index]
    else:
      return self.table.get_by_index(column_index, row_index - 1)
