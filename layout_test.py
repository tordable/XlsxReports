"""Tests for layout.py"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from layout import ColumnLayout
from layout import FixedSizeLayout
from layout import HideOutsideLayout
from layout import PaddingLayout
from layout import TableLayout
from layout import RowLayout
from style import FixedStyle, TableStyle
from table import Table
from xls import MockSheet
from xls import MockWorkbook

import unittest


GREEN = '#00FF00'
BLUE = '#0000FF'


class FixedSizeLayoutTest(unittest.TestCase):
  """Tests for FixedSizeLayout."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.style = FixedStyle(self.workbook, 'FixedContent', GREEN)

  def test_no_style(self):
    self.assertRaises(ValueError, FixedSizeLayout, None, 1, 1)

  def test_invalid_dimensions(self):
    self.assertRaises(ValueError, FixedSizeLayout, self.style, None, 1)
    self.assertRaises(ValueError, FixedSizeLayout, self.style, 1, None)
    self.assertRaises(ValueError, FixedSizeLayout, self.style, 0, 1)
    self.assertRaises(ValueError, FixedSizeLayout, self.style, 1, -1)

  def test_size(self):
    layout = FixedSizeLayout(self.style, 1, 1)
    self.assertEquals((1, 1), layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (1, 1)
    layout = FixedSizeLayout(self.style, 2, 2)
    layout.draw(sheet, start_position)

    self.assertIsNone(sheet.read(0, 0))  # Before start_position.
    self.assertEquals('FixedContent', sheet.read(1, 1))  # Start position.
    self.assertEquals('FixedContent', sheet.read(1, 2))  # Next cell.
    self.assertIsNone(sheet.read(1, 3))  # Out of boundaries.
    self.assertEquals('FixedContent', sheet.read(2, 1))  # Lower row.
    self.assertEquals('FixedContent', sheet.read(2, 2))  # Next cell.
    self.assertIsNone(sheet.read(3, 1))  # Out of boundaries.
    self.assertIsNone(sheet.read(3, 3))


class TableLayoutTest(unittest.TestCase):
  """Tests for TableLayout"""

  def setUp(self):
    # Create a table with 3 columns and 2 rows.
    self.table = Table('Table', ['Col1', 'Col2', 'Col3'])
    self.table.add_row(['a', 'b', 'c'])
    self.table.add_row(['d', 'e', 'f'])

    self.workbook = MockWorkbook()
    self.style = TableStyle(self.workbook, self.table)

  def test_no_style(self):
    self.assertRaises(ValueError, TableLayout, None, self.table)

  def test_null_table(self):
    self.assertRaises(ValueError, TableLayout, self.style, None)

  def test_size(self):
    layout = TableLayout(self.style, self.table)
    # The height of the layout includes 1 extra for the headers.
    self.assertEquals((3, 3), layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (0, 0)
    layout = TableLayout(self.style, self.table)
    layout.draw(sheet, start_position)

    # Expect a 3 x 3 grid of cells with the table data.
    self.assertEquals('Col1', sheet.read(0, 0))
    self.assertEquals('Col2', sheet.read(0, 1))
    self.assertEquals('Col3', sheet.read(0, 2))
    self.assertIsNone(sheet.read(0, 3))
    self.assertEquals('a', sheet.read(1, 0))
    self.assertEquals('b', sheet.read(1, 1))
    self.assertEquals('c', sheet.read(1, 2))
    self.assertIsNone(sheet.read(1, 3))
    self.assertEquals('d', sheet.read(2, 0))
    self.assertEquals('e', sheet.read(2, 1))
    self.assertEquals('f', sheet.read(2, 2))
    self.assertIsNone(sheet.read(2, 3))
    self.assertIsNone(sheet.read(3, 0))
    self.assertIsNone(sheet.read(3, 1))
    self.assertIsNone(sheet.read(3, 2))
    self.assertIsNone(sheet.read(3, 3))


class PaddingLayoutTest(unittest.TestCase):
  """Tests for PaddingLayout."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.child_style = FixedStyle(self.workbook, 'Child', GREEN)
    self.padding_style = FixedStyle(self.workbook, 'Padding', BLUE)
    self.fixed_layout = FixedSizeLayout(self.child_style, 2, 7)

  def test_no_style(self):
    self.assertRaises(ValueError, PaddingLayout, None, self.fixed_layout,
                      1, 1, 1, 1)

  def test_invalid_padding(self):
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      self.fixed_layout, -1, 0, 0, 0)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      self.fixed_layout, 1, -1, 0, 0)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      self.fixed_layout, 0, 0, -1, 0)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      self.fixed_layout, 1, 1, 1, -1)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      self.fixed_layout, 0, 0, 0, 0)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      None, 1, 1, 1, 1)
    self.assertRaises(ValueError, PaddingLayout, self.padding_style,
                      [self.fixed_layout], 1, 1, 1, 1)

  def test_size(self):
    layout = PaddingLayout(self.padding_style, self.fixed_layout, 0, 1, 2, 3)
    self.assertEquals((2 + 1 + 3, 7 + 0 + 2), layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (1, 0)  # Start on second column.
    layout = PaddingLayout(self.padding_style, self.fixed_layout, 1, 0, 1, 0)
    layout.draw(sheet, start_position)

    # First row.
    self.assertIsNone(sheet.read(0, 0))
    self.assertEquals('Padding', sheet.read(0, 1))
    self.assertEquals('Padding', sheet.read(0, 2))
    self.assertIsNone(sheet.read(0, 3))

    # Second row.
    self.assertIsNone(sheet.read(1, 0))
    self.assertEquals('Child', sheet.read(1, 1))
    self.assertEquals('Child', sheet.read(1, 2))
    self.assertIsNone(sheet.read(1, 3))

    # One to last row.
    self.assertIsNone(sheet.read(7, 0))
    self.assertEquals('Child', sheet.read(7, 1))
    self.assertEquals('Child', sheet.read(7, 2))
    self.assertIsNone(sheet.read(7, 3))

    # Last padding row.
    self.assertIsNone(sheet.read(8, 0))
    self.assertEquals('Padding', sheet.read(8, 1))
    self.assertEquals('Padding', sheet.read(8, 2))
    self.assertIsNone(sheet.read(8, 3))


class RowLayoutTest(unittest.TestCase):
  """Tests for RowLayout."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.child_style = FixedStyle(self.workbook, 'Child', GREEN)
    self.parent_style = FixedStyle(self.workbook, 'Parent', BLUE)

    # 3 layouts in a row. Total width is 11, max height is 3.
    layout1 = FixedSizeLayout(self.child_style, 4, 2)
    layout2 = FixedSizeLayout(self.child_style, 2, 3)
    layout3 = FixedSizeLayout(self.child_style, 5, 2)
    self.layout_list = [layout1, layout2, layout3]
    self.layout = RowLayout(self.parent_style, self.layout_list)

  def test_no_style(self):
    self.assertRaises(ValueError, RowLayout, None, self.layout_list)

  def test_no_layouts(self):
    self.assertRaises(ValueError, RowLayout, self.parent_style, None)
    self.assertRaises(ValueError, RowLayout, self.parent_style,
                      FixedSizeLayout(self.child_style, 1, 1))
    self.assertRaises(ValueError, RowLayout, self.parent_style, [])

  def test_size(self):
    self.assertEquals((11, 3), self.layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (0, 0)
    self.layout.draw(sheet, start_position)

    # The cell in row 1 column 3 should be filled. But the cell below should be
    # filled with the parent style. End of the element 1.
    self.assertEquals('Child', sheet.read(1, 3))
    self.assertEquals('Parent', sheet.read(2, 3))
    self.assertIsNone(sheet.read(3, 3))

    # Same for the next element, but this one is not covered by the parent.
    self.assertEquals('Child', sheet.read(2, 5))
    self.assertIsNone(sheet.read(3, 5))

    # And the last element.
    self.assertEquals('Child', sheet.read(1, 10))
    self.assertEquals('Parent', sheet.read(2, 10))
    self.assertIsNone(sheet.read(3, 10))
    self.assertIsNone(sheet.read(1, 11))


class ColumnLayoutTest(unittest.TestCase):
  """Tests for ColumnLayout."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.child_style = FixedStyle(self.workbook, 'Child', GREEN)
    self.parent_style = FixedStyle(self.workbook, 'Parent', BLUE)

    # 3 layouts in a column. Max width is 5, total height is 7.
    layout1 = FixedSizeLayout(self.child_style, 4, 2)
    layout2 = FixedSizeLayout(self.child_style, 2, 3)
    layout3 = FixedSizeLayout(self.child_style, 5, 2)
    self.layout_list = [layout1, layout2, layout3]
    self.layout = ColumnLayout(self.parent_style, self.layout_list)

  def test_no_style(self):
    self.assertRaises(ValueError, ColumnLayout, None, self.layout_list)

  def test_no_layouts(self):
    self.assertRaises(ValueError, ColumnLayout, self.parent_style, None)
    self.assertRaises(ValueError, ColumnLayout, self.parent_style,
                      FixedSizeLayout(self.child_style, 1, 1))
    self.assertRaises(ValueError, ColumnLayout, self.parent_style, [])

  def test_size(self):
    self.assertEquals((5, 7), self.layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (0, 0)
    self.layout.draw(sheet, start_position)

    # The cell in row 2 column 4 should be filled, but column 5 should be
    # filled by the parent.
    self.assertEquals('Child', sheet.read(1, 3))
    self.assertEquals('Parent', sheet.read(1, 4))
    self.assertIsNone(sheet.read(1, 5))

    # Same for the element below.
    self.assertEquals('Child', sheet.read(4, 1))
    self.assertEquals('Parent', sheet.read(4, 2))

    # And the element at the bottom.
    self.assertEquals('Child', sheet.read(6, 4))
    self.assertIsNone(sheet.read(6, 5))
    self.assertIsNone(sheet.read(7, 4))


class HideOutsideLayoutTest(unittest.TestCase):
  """Tests for HideOutsideLayout."""

  def setUp(self):
    self.workbook = MockWorkbook()
    self.child_style = FixedStyle(self.workbook, 'Child', GREEN)
    self.parent_style = FixedStyle(self.workbook, 'Parent', BLUE)

    self.child_layout = FixedSizeLayout(self.child_style, 3, 2)
    self.layout = HideOutsideLayout(self.parent_style, self.child_layout)

  def test_no_style(self):
    self.assertRaises(ValueError, HideOutsideLayout, None, self.child_layout)

  def test_no_child_layout(self):
    self.assertRaises(ValueError, HideOutsideLayout, self.parent_style, None)
    self.assertRaises(ValueError, HideOutsideLayout, self.parent_style, [])

  def test_size(self):
    self.assertEquals((3, 2), self.layout.size())

  def test_draw(self):
    sheet = MockSheet('Sheet1')
    start_position = (0, 0)
    self.layout.draw(sheet, start_position)

    # All cells inside the layout have the format of the child.
    self.assertEquals('Child', sheet.read(0, 0))
    self.assertEquals('Child', sheet.read(0, 1))
    self.assertEquals('Child', sheet.read(0, 2))
    self.assertEquals('Child', sheet.read(1, 0))
    self.assertEquals('Child', sheet.read(1, 1))
    self.assertEquals('Child', sheet.read(1, 2))

    # The cells outside don't have any value.
    self.assertIsNone(sheet.read(0, 3))
    self.assertIsNone(sheet.read(1, 3))
    self.assertIsNone(sheet.read(2, 0))
    self.assertIsNone(sheet.read(2, 1))
    self.assertIsNone(sheet.read(2, 2))
    self.assertIsNone(sheet.read(2, 3))

    # Check the default row and column properties for the hidden cells.
    self.assertTrue(sheet.get_property('hide_unused_rows_by_default'))
    self.assertEquals([3,  # First column.
                       16383,  # Last column.
                       None,  # Width.
                       None,  # Style.
                       "{'hidden': True}"],  # Options.
                      sheet.get_property('column_options'))


  def test_draw_invalid_start_position(self):
    sheet = MockSheet('Sheet1')
    start_position = (0, 1)
    self.assertRaises(ValueError, self.layout.draw, sheet, start_position)
    start_position = (1, 0)
    self.assertRaises(ValueError, self.layout.draw, sheet, start_position)


if __name__ == '__main__':
  unittest.main()
