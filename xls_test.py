"""Tests for xls.py"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from xls import MockFormat, MockSheet, MockWorkbook

import unittest


class MockWorkbookTest(unittest.TestCase):
  """Tests for MockWorkbook."""

  def test_add_worksheet(self):
    wb = MockWorkbook()
    wb.add_worksheet('A')
    wb.add_worksheet('B')
    self.assertEquals('A', wb.get_worksheet(0).get_name())
    self.assertEquals('B', wb.get_worksheet(1).get_name())


class MockFormatTest(unittest.TestCase):
  """Tests for MockFormat."""

  def test_set_bg_color(self):
    fmt = MockFormat()
    self.assertEquals(0, fmt.num_properties())
    BLUE = '#0000FF'
    fmt.set_bg_color(BLUE)
    self.assertEquals(1, fmt.num_properties())
    self.assertEquals(BLUE, fmt.get_property('bg_color'))


class MockSheetTest(unittest.TestCase):
  """Tests for MockSheet."""

  def test_get_name(self):
    sheet = MockSheet('A')
    self.assertEquals('A', sheet.get_name())

  def test_write(self):
    sheet = MockSheet('A')
    sheet.write(0, 0, 'a')
    sheet.write(0, 1, 'b')
    sheet.write(3, 3, 'c')
    self.assertEquals('a', sheet.read(0, 0))
    self.assertEquals('b', sheet.read(0, 1))
    self.assertEquals('c', sheet.read(3, 3))

  def test_set_default_row(self):
    sheet = MockSheet('B')
    sheet.set_default_row(hide_unused_rows=False)
    self.assertFalse(sheet.get_property('hide_unused_rows_by_default'))
    sheet.set_default_row(hide_unused_rows=True)
    self.assertTrue(sheet.get_property('hide_unused_rows_by_default'))

  def test_set_column(self):
    sheet = MockSheet('B')
    options = {'hidden': False}
    cell_format = MockFormat()
    sheet.set_column(1, 2, 123.0, cell_format, options)
    self.assertEquals([1, 2, 123.0, cell_format, "{'hidden': False}"],
                      sheet.get_property('column_options'))


if __name__ == '__main__':
  unittest.main()
