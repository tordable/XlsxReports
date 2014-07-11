"""A layout for a XLS report.

Each sheet in a report contains a single layout. The layout describes how the
different elements are organized and can contain child layouts inside.
"""

__author__ = 'jt@javiertordable.com'
__copyright__ = "Copyright (C) 2014 Javier Tordable"


from style import TableStyle


MAX_EXCEL_COLUMN = 16383


class Layout(object):
  """A layout is a container for a group of report tables and other layouts.

  A layout can be embedded inside of another layout. Normally there will be a
  single layout which contains all other layouts.
  """

  def __init__(self, style):
    self.style = None
    self.children = None

  def style(self):
    """The style of the layout."""
    return self.style

  def children(self):
    """A list with the child layouts of this layout."""
    return self.children

  def size(self):
    """The size of the layout, in cells, given as (width, height)"""
    return None

  def draw(self, output_sheet, start_position):
    """Draw the layout on the output_table, starting at start_position."""
    (start_column, start_row) = start_position
    (width, height) = self.size()
    for row in range(start_row, start_row + height):
      for column in range(start_column, start_column + width):
        cell_value = self.style.get_cell_content(column, row)
        cell_format = self.style.get_cell_format(column, row)
        output_sheet.write(row, column, cell_value, cell_format)


class FixedSizeLayout(Layout):
  """A layout with a fixed size in cells. but no table content."""

  def __init__(self, style, width, height):
    if style is None:
      raise ValueError('Please give a valid style')
    if width < 1 or height < 1:
      raise ValueError('Please give positive dimensions')

    self.style = style
    self.width = width
    self.height = height

  def size(self):
    return (self.width, self.height)


class TableLayout(Layout):
  """A layout to render a table."""

  def __init__(self, style, table):
    if style is None or not isinstance(style, TableStyle):
      raise ValueError('Please use a TableSytle to draw a TableLayout')
    if table is None:
      raise ValueError('Plase give a valid table.')

    self.style = style
    self.table = table

  def size(self):
    return (self.table.num_columns,
            self.table.num_rows + 1) # Add one row for the header.

  def draw(self, output_sheet, start_position):
    (start_column, start_row) = start_position
    (width, height) = self.size()

    for output_row in range(start_row, start_row + height):
      data_row_index = output_row - start_row
      for output_column in range(start_column, start_column + width):
        data_column_index = output_column - start_column
        cell_value = self.style.get_cell_content(data_column_index,
                                                 data_row_index)
        cell_format = self.style.get_cell_format(data_column_index,
                                                 data_row_index)
        output_sheet.write(output_row, output_column, cell_value, cell_format)


class PaddingLayout(Layout):
  """A layout which adds a padding of cells to another layout.

  The parameters of this layout are in the same order as the CSS parameters
  for padding.
  """

  def __init__(self, style, child_layout, top, right, bottom, left):
    if style is None:
      raise ValueError('Please give a valid style')
    if top < 0 or right < 0 or bottom < 0 or left < 0 or \
          (top == 0 and right == 0 and bottom == 0 and left == 0):
      raise ValueError('Please use valid padding sizes')
    if child_layout is None or not isinstance(child_layout, Layout):
      raise ValueError('Please pass a valid child layout')

    self.style = style
    self.top = top
    self.right = right
    self.bottom = bottom
    self.left = left
    self.children = [child_layout]

  def size(self):
    (child_width, child_height) = self.children[0].size()
    return (child_width + self.left + self.right,
            child_height + self.top + self.bottom)

  def draw(self, output_sheet, start_position):
    # First apply the style of the PaddingLayout.
    super(PaddingLayout, self).draw(output_sheet, start_position)

    # Now draw the child in the correct position, inside of the padding.
    (start_column, start_row) = start_position
    (start_column, start_row) = (start_column + self.left, start_row + self.top)
    self.children[0].draw(output_sheet, (start_column, start_row))


class RowLayout(Layout):
  """A layout which contains other layouts in a single row."""

  def __init__(self, style, row_layouts):
    if style is None:
      raise ValueError('Please give a valid style')
    if row_layouts is None or not isinstance(row_layouts, list) or \
          len(row_layouts) < 1:
      raise ValueError('Please pass a non-empty list of layouts')

    self.style = style
    self.children = row_layouts

  def size(self):
    total_width = 0
    max_height = 0
    for layout in self.children:
      (width, height) = layout.size()
      total_width += width
      max_height = max(max_height, height)
    return (total_width, max_height)

  def draw(self, output_sheet, start_position):
    # First apply the style of the RowLayout.
    super(RowLayout, self).draw(output_sheet, start_position)

    # Draw all layouts, one at a time, from left to right.
    (start_column, start_row) = start_position
    for child_layout in self.children:
      child_layout.draw(output_sheet, (start_column, start_row))

      # Move the start position for the next layout, but only horizontally.
      (added_width, added_height) = child_layout.size()
      (start_column, start_row) = (start_column + added_width, start_row)


class ColumnLayout(Layout):
  """A layout which contains other layouts in a single column."""

  def __init__(self, style, column_layouts):
    if style is None:
      raise ValueError('Please give a valid style')
    if column_layouts is None or not isinstance(column_layouts, list) or \
          len(column_layouts) < 1:
      raise ValueError('Please pass a non-empty list of layouts')

    self.style = style
    self.children = column_layouts

  def size(self):
    max_width = 0
    total_height = 0
    for layout in self.children:
      (width, height) = layout.size()
      max_width = max(max_width, width)
      total_height += height
    return (max_width, total_height)

  def draw(self, output_sheet, start_position):
    # First apply the style of the ColumnLayout.
    super(ColumnLayout, self).draw(output_sheet, start_position)

    # Draw all layouts, one at a time, from top to bottom.
    (start_column, start_row) = start_position
    for child_layout in self.children:
      child_layout.draw(output_sheet, (start_column, start_row))

      # Move the start position for the next layout, but only vertically.
      (added_width, added_height) = child_layout.size()
      (start_column, start_row) = (start_column, start_row + added_height)


class HideOutsideLayout(Layout):
  """A layout which hides the cells beyond the layout size.

  WARNING: The HideOutsideLayout should normally be the outermost layout in
  a sheet. It will hide any other layout outside of it's dimensions.
  """

  def __init__(self, style, child_layout):
    if style is None:
      raise ValueError('Please give a valid style')
    if child_layout is None or not isinstance(child_layout, Layout):
      raise ValueError('Please pass a valid child layout')

    self.style = style
    self.children = [child_layout]

  def size(self):
    return self.children[0].size()

  def draw(self, output_sheet, start_position):
    # The start position has to be (0, 0)
    (start_column, start_row) = start_position
    if start_column is not 0 or start_row is not 0:
      raise ValueError('The start position for this layout must be (0, 0)')

    # Hide all rows without data (below the layout).
    output_sheet.set_default_row(hide_unused_rows=True)

    # Hide all columns to the right of the layout.
    output_sheet.set_column(first_col=self.size()[0], last_col=MAX_EXCEL_COLUMN,
                            width=None, format=None, options={'hidden': True})

    # Apply the style of the HideOutsideLayout and then draw the child.
    super(HideOutsideLayout, self).draw(output_sheet, start_position)
    self.children[0].draw(output_sheet, start_position)
