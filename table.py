"""A table which holds the data of the report."""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


class Table(object):
  """A table which holds the data of the report.

  The table has a series of rows and columns, the columns have to be defined on
  construction and the rows can be added one at a time.
  """

  def __init__(self, name, column_names):
    if len(column_names) < 1:
      raise ValueError('Table needs at least one column name.')

    self._name = name
    self._column_names = column_names
    self._rows = []

  @property
  def name(self):
    return self._name

  @property
  def column_names(self):
    return self._column_names

  @property
  def num_columns(self):
    return len(self._column_names)

  def add_row(self, row):
    if len(row) != len(self._column_names):
      raise ValueError(
        'Invalid number of arguments in row. Has %d, should have %d'
        .format(len(row, len(column_names))))
    self._rows.append(row)

  @property
  def num_rows(self):
    return len(self._rows)

  def get_by_index(self, column_index, row_index):
    return self._rows[row_index][column_index]

  def get(self, column_name, row_index):
    column_index = self._column_names.index(column_name)
    return self._rows[row_index][column_index]

  def __str__(self):
    ret = ','.join(self._column_names)
    for row in self._rows:
      ret += '\n'
      row_values = [str(item) for item in row]
      ret += ','.join(row_values)
    return ret
