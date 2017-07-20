# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 07:31:51 2017

@author: s140146
"""
import pandas
import bokeh
from bokeh.plotting import figure, output_file, save



data_file = r'Historic Strengths figures.xlsx'

personnel_data = pandas.read_excel(data_file,header=2,na_values=['-'])
personnel_data = personnel_data.set_index(['Year'])

categories = ['Navy','Army','RAF']

output_file('historicStrength.html')
source = bokeh.models.ColumnDataSource(personnel_data)

# What pops up on hover?
tooltips = [('Year', '@Year'),
           ('Navy Qty', '@Navy'),
           ('Army Qty', '@Army'),
           ('RAF Qty', '@RAF'),
           ('Total Qty', '@TOTAL')]

# Make the hover tool
hover = bokeh.models.HoverTool(tooltips=tooltips)
TOOLS = "box_select,lasso_select,help"

s1 = figure(tools=TOOLS, plot_width=1500, plot_height=750, title='Historic Service Strength', y_axis_type='log')
s1.axis.axis_label_text_font_style = 'bold'
s1.yaxis.axis_label_text_font_style = 'bold'
s1.xaxis.axis_label_text_font_style = 'bold'
s1.xgrid.grid_line_color = 'white'
s1.ygrid.grid_line_color = 'white'
s1.xaxis.axis_label = 'Year'
s1.yaxis.axis_label = 'Personnel Qty'
s1.add_tools(hover)
s1.line(x='Year', y='TOTAL',source=source)

# create a new plot and share both ranges
s2 = figure(tools=TOOLS, plot_width=1500, plot_height=750, x_range=s1.x_range, title='Strength Change', y_axis_type='log')
s2.axis.axis_label_text_font_style = 'bold'
s2.yaxis.axis_label_text_font_style = 'bold'
s2.xaxis.axis_label_text_font_style = 'bold'
s2.xgrid.grid_line_color = 'white'
s2.ygrid.grid_line_color = 'white'
s2.xaxis.axis_label = 'Year'
s2.yaxis.axis_label = 'Personnel Qty Change'
s2.add_tools(hover)
s2.line()

p = bokeh.gridplot([[s1, s2]], toolbar_location=None)

save(p)