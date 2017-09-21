import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import bokeh
from bokeh.plotting import figure, output_file, save
from bokeh.models import Span #, Range1d
import datetime
import time
from scipy import stats
import numpy as np

SCOPE = ["https://spreadsheets.google.com/feeds"]
SECRETS_FILE = r"QuickTracker.json"
SPREADSHEET = "Weight tracker"

# Authenticate using the signed key
credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE , SCOPE)


gc = gspread.authorize(credentials)

weight_data = gc.open('Weight tracker')
sheet = weight_data.sheet1

data = pd.DataFrame(sheet.get_all_records())
data['Timestamp'] = pd.to_datetime(data['Timestamp'],format = "%d/%m/%Y %H:%M:%S")
goals = data[:2]
weights = data[2:]
del weights['Goal']
del weights['Rate']
del weights['Predictor']

now = datetime.datetime.now()
flight_datetime = datetime.datetime(2017, 10, 7,7,00,00)
trend_start_time = now-datetime.timedelta(days=30)
date_in_date_range = weights[(weights['Timestamp'] > trend_start_time)].copy()
date_in_date_range['since'] = (date_in_date_range['Timestamp'] - pd.to_datetime(trend_start_time))
date_in_date_range['since'] = (date_in_date_range['since'].astype(np.int64)/10**9).astype(np.int64)
date_in_date_range['Weight (kg)'].astype(np.float32)
since = list(date_in_date_range['since'])
kg_weight = list(date_in_date_range['Weight (kg)'])
slope, intercept, r_value, p_value, std_err = stats.linregress(since, kg_weight)


time_to_flight = flight_datetime - trend_start_time
ttf_seconds = time_to_flight.total_seconds() 
flight_weight = (slope*(ttf_seconds))+intercept


print('Time to Flight: {}'.format(flight_datetime - now))
print('Predicted weight: {}'.format(flight_weight))
print('Weight lost: {}'.format(max(weights['Weight (kg)'])-date_in_date_range['Weight (kg)'].iloc[-1]))
print("r-squared:", r_value**2)


output_file(r"weight.html")
source = bokeh.models.ColumnDataSource(weights)

# What pops up on hover?


# Make the hover tool


#left, right, bottom, top =  time.mktime((now-datetime.timedelta(days=28)).timetuple())*1000 , time.mktime((now+datetime.timedelta(days=21)).timetuple())*1000, 95, 117
s1 = figure(plot_width=1500, plot_height=750, title='Weight', x_axis_type='datetime')#, x_range=Range1d(left, right), y_range=Range1d(bottom, top))
s1.axis.axis_label_text_font_style = 'bold'
s1.yaxis.axis_label_text_font_style = 'bold'
s1.xaxis.axis_label_text_font_style = 'bold'
s1.xgrid.grid_line_color = 'white'
s1.ygrid.grid_line_color = 'white'
s1.xaxis.axis_label = 'Time'
s1.yaxis.axis_label = 'Weight (kg)'

# Vertical line
target_date = time.mktime(flight_datetime.timetuple())*1000
target_vline = Span(location = target_date, dimension='height', line_color='blue', line_width=2)
now_date = time.mktime(now.timetuple())*1000
now_vline = Span(location = now_date, dimension='height', line_color='black', line_width=2)

# Horizontal line
target_hline = Span(location=100, dimension='width', line_color='blue', line_width=2)
obese_hline = Span(location=106.5, dimension='width', line_color='orange', line_width=2)
future_weight_top = Span(location=88.7, dimension='width', line_color='green', line_width=2)
future_weight_bottom = Span(location=65.4, dimension='width', line_color='green', line_width=2)
s1.renderers.extend([now_vline, target_vline, target_hline, obese_hline, future_weight_top, future_weight_bottom])
s1.circle(x='Timestamp', y='Weight (kg)',source=source,size=3)
s1.line(x=[time.mktime(trend_start_time.timetuple())*1000, time.mktime(flight_datetime.timetuple())*1000],y=[intercept,flight_weight],line_dash='dotted')

save(s1)
