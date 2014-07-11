"""Tests for style.py"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from style import EmptyStyle, FixedStyle, TableStyle
from table import Table
from xls import MockWorkbook

import unittest


BLUE = '#0000FF'


class EmptyStyleTest(unittest.TestCase):
  """Tests for EmptyStyle."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.style = EmptyStyle(self.workbook)

  def test_get_cell_content(self):
    self.assertIsNone(self.style.get_cell_content(0, 0))

  def test_get_cell_format(self):
    self.assertEquals(0, self.style.get_cell_format(0, 0).num_properties())


class FixedStyleTest(unittest.TestCase):
  """Tests for FixedStyle."""

  def setUp(self):
    self.workbook = MockWorkbook()

  def test_get_cell_content(self):
    style = FixedStyle(self.workbook, None, BLUE)
    self.assertIsNone(style.get_cell_content(0, 0))
    style = FixedStyle(self.workbook, 0, BLUE)
    self.assertEquals(0, style.get_cell_content(0, 0))

  def test_get_cell_format(self):
    style = FixedStyle(self.workbook, None, BLUE)
    self.assertEquals(BLUE,
                      style.get_cell_format(0, 0).get_property('bg_color'))


class TableStyleTest(unittest.TestCase):
  """Tests for TableStyle."""

  def setUp(self):
    self.table = Table('Table', ['Column1', 'Column2'])
    self.table.add_row(['a', 'b'])
    self.table.add_row(['c', 1])

    self.workbook = MockWorkbook()
    self.style = TableStyle(self.workbook, self.table)

  def test_get_cell_content(self):
    self.assertEqual('Column1', self.style.get_cell_content(0, 0))
    self.assertEqual('a', self.style.get_cell_content(0, 1))
    self.assertEqual('c', self.style.get_cell_content(0, 2))
    self.assertEqual('Column2', self.style.get_cell_content(1, 0))
    self.assertEqual('b', self.style.get_cell_content(1, 1))
    self.assertEqual(1, self.style.get_cell_content(1, 2))


if __name__ == '__main__':
  unittest.main()
