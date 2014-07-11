"""Proxy interfaces and mocks for the XLS library.

This module contains interfaces to the XLS library and mocks, which will allow
switching the underlying implementation if necessary.
"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


import xlsxwriter


def new_workbook(filename):
  return _WorkbookImpl(filename)


class Workbook(object):
  """A XLS workbook."""

  def add_worksheet(self, name):
    """Adds a new sheet to the workbook and returns it."""
    pass

  def get_worksheet(self, index):
    """Returns a worksheet with the given index."""
    pass

  def add_format(self):
    """Returns a new format."""
    pass

  def close(self):
    """Closes the workbook after all editing is complete."""
    pass


class MockWorkbook(Workbook):
  """A mock implementation of the Workbook."""

  def __init__(self):
    self.sheets = []
    self.formats = []

  def add_worksheet(self, name):
    sheet = MockSheet(name)
    self.sheets.append(sheet)
    return sheet

  def get_worksheet(self, index):
    return self.sheets[index]

  def add_format(self):
    fmt = MockFormat()
    self.formats.append(fmt)
    return fmt

  def close(self):
    pass


class _WorkbookImpl(Workbook):
  """Implementation of a workbook using the XlsxWriter library."""

  def __init__(self, filename):
    self._wb = xlsxwriter.Workbook(filename)

  def add_worksheet(self, name):
    sheet = self._wb.add_worksheet(name)
    return _SheetImpl(sheet)

  def get_worksheet(self, index):
    sheet = _wb.worksheets()[index]
    return _SheetImpl(sheet)

  def add_format(self):
    return _FormatImpl(self._wb)

  def close(self):
    self._wb.close()


class Format(object):
  """A format used in a workbook to determine cell appearance."""
  pass


class MockFormat(Format):
  """A mock implementation of the Format."""

  def __init__(self):
    self.properties = {}

  def set_bg_color(self, bg_color):
    self.properties['bg_color'] = bg_color

  def num_properties(self):
    return len(self.properties)

  def get_property(self, property_name):
    return self.properties[property_name]


class _FormatImpl(Format):
  """Implementation of a format using the XlsxWriter library."""

  def __init__(self, workbook):
    self._fmt = workbook.add_format()

  def set_bg_color(self, bg_color):
    self._fmt.set_bg_color(bg_color)


class Sheet(object):
  """A sheet in a XLS report."""

  def get_name(self):
    """Returns the name of the sheet."""
    pass

  def set_default_row(self, hide_unused_rows=False):
    """Sets properties for the default row."""
    pass

  def set_column(self, first_col, last_col, width=None, format=None,
                 options=None):
    """Sets properties of the column."""
    pass

  def write(self, row, column, value, format=None):
    """Writes a value in the given row and column cell using the given format.
    """
    pass


class MockSheet(Sheet):
  """A mock implementation of the Sheet."""

  def __init__(self, name):
    self.name = name
    self.cell_contents = {}
    self.cell_formats = {}
    self.properties = {}

  def get_name(self):
    return self.name

  def set_default_row(self, hide_unused_rows=False):
    self.properties['hide_unused_rows_by_default'] = hide_unused_rows

  def set_column(self, first_col, last_col, width=None, format=None,
                 options=None):
    # TODO(tordable): Consider storing per-column attributes.
    self.properties['column_options'] = \
        [first_col, last_col, width, format, str(options)]

  def get_property(self, property_name):
    return self.properties[property_name]

  def write(self, row, column, value, format=None):
    position = (row, column)
    self.cell_contents[position] = value
    self.cell_formats[position] = format

  def read(self, row, column):
    """Reads a value in the cell.

    This method is not in the Sheet interface.
    """
    position = (row, column)
    if position in self.cell_contents:
      return self.cell_contents[position]
    else:
      return None

  def __str__(self):
    ret = ''
    for position, value in self.cell_contents.items():
      ret += '(' + str(position[0]) + ',' + str(position[1]) + ') = '
      ret += str(value) + '\n'
    return ret


class _SheetImpl(Sheet):
  """Implementation of a sheet using the XlsxWriter library."""

  def __init__(self, sheet):
    self._sh = sheet

  def get_name(self):
    return self._sh.get_name()

  def set_default_row(self, hide_unused_rows=False):
    self._sh.set_default_row(hide_unused_rows=hide_unused_rows)

  def set_column(self, first_col, last_col, width=None, format=None,
                 options=None):
    if format is not None:
      column_format = format._fmt
    else:
      column_format = None
    self._sh.set_column(first_col, last_col, width, column_format, options)

  def write(self, row, column, value, format=None):
    # TODO(tordable): Use the proper type if possible.
    if value is not None and format is not None:
      # The actual format passed to the XlsxWriter library is the inner format
      # of the _FormatImpl.
      self._sh.write(row, column, value, format._fmt)
    elif value is not None and format is None:
      self._sh.write(row, column, value)
    else:
      self._sh.write_blank(row, column, None)
