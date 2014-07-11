"""Tests for table.py"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from table import Table
import unittest


class TableTest(unittest.TestCase):
  """Tests for Table."""

  def setUp(self):
    self.table = Table('Table', ['Column1', 'Column2'])
    self.table.add_row(['a', 'b'])
    self.table.add_row(['c', 1])

  def test_name(self):
    self.assertEquals('Table', self.table.name)

  def test_column_names(self):
    self.assertEquals(['Column1', 'Column2'], self.table.column_names)

  def test_num_columns(self):
    self.assertEquals(2, self.table.num_columns)

  def test_add_rows(self):
    self.table.add_row(['d', 2])
    self.assertEquals('d', self.table.get('Column1', 2))
    self.assertEquals(2, self.table.get('Column2', 2))

  def test_num_rows(self):
    self.assertEquals(2, self.table.num_rows)

  def test_get_by_index(self):
    self.assertEquals('c', self.table.get_by_index(0, 1))
    self.assertEquals('b', self.table.get_by_index(1, 0))

  def test_get(self):
    self.assertEquals('a', self.table.get('Column1', 0))
    self.assertEquals(1, self.table.get('Column2', 1))

  def test_get_invalid_column(self):
    self.assertRaises(ValueError, self.table.get, 'InvalidColumn', 0)

  def test_get_invalid_row(self):
    self.assertRaises(IndexError, self.table.get, 'Column1', 5)

  def test_str(self):
    self.assertEquals('Column1,Column2\n' +
                      'a,b\n' +
                      'c,1',
                      str(self.table))


if __name__ == '__main__':
  unittest.main()
