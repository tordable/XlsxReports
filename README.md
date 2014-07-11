# XLSX Reports

This is a simple Python library to create Excel reports.

## Introduction

Many times an Excel report is just a group of tables and charts with some
basic data, normally with a common style. It would be great if there was a way
to directly generate the Excel report from the data and some simple
configuration.

## Design

There are 3 basic elements:

* A _data table_ contains the data for the report
* A _style_ indicates how a single table is formatted
* A _layout_ indicates how different tables are formatted. Layouts are
structured as a tree. The layout references the data and style

A report is built from a single layout. A parent layout may contain child
layouts. Some of these may be table layouts which apply a table sytle to the
data to build the actual cells that are added to the spreadsheet.

The data table merely contains a list of columns and corresponding data rows,
with one value per column. The list of columns is used for the table headers
and each row is added as a row to the report table. Each data value in the
table is added to an individual cell.

The style contains information such as background and font color, as well
as any other visual information in the spreadsheet.

The layout can be one of a variety of types, for example, it can contain a
series of reports in the same row, structured in a column, with a fixed size, or
automatically expanding to include the full report.

## TO DO

Remaining style features:

  - Hide gridlines
  - Borders (in different color)
  - Set row and column width
  - Set fonts (different for headers and rows)
  - Set font color
  - Set bold font
  - Set color for numbers (conditional formatting?)
  - Table style with extra padding between columns
  - Zebra striping
