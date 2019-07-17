import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as ps
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt
from datetime import datetime, timedelta


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


dts = [dt for dt in datetime_range(datetime(2019, 2, 1,), datetime(2019, 2, 15),
                                   timedelta(minutes=1))]


conn = ps.connect(host="0.0.0.0", database='a', user='a', password='a',)
cursor = conn.cursor()
cursor.execute('select datetime, count( * ) from ttdestinationlog group by datetime order by datetime;')

rows = cursor.fetchall()



year = []
month = []
day = []
time = []

df = pd.DataFrame(rows, columns=['datetime', 'No:Transaction'])
datetime = df['datetime']
b =((df['No:Transaction'].where(df['datetime'] == '1902031002')).dropna()).tolist()
print(b[0])
# for i in range(len(datetime)):
#     year.append(datetime[i][:2])
#     month.append(datetime[i][2:4])
#     day.append(datetime[i][4:6])
#     time.append(datetime[i][6:8] + ":" + datetime[i][6:8])
timestamp = []
for i in range(len(datetime)):
    timestamp.append(datetime[i][:2] + "-" + datetime[i][2:4] + "-" + datetime[i][4:6] +
                     " " + datetime[i][6:8] + ":" + datetime[i][8:])



times = []

for i in range(len(timestamp)):
    times.append(dt.strptime(timestamp[i], "%y-%m-%d %H:%M"))

df['datetime'] = times

count = []
for dt in dts:
    b =((df['No:Transaction'].where(df['datetime'] == dt)).dropna()).tolist()
    if len(b) == 0:
        count.append(None)
    else:
        count.append(b[0])

raw_data = zip(dts, count)
data = pd.DataFrame(raw_data,columns=['datetime', 'No:Transaction'])


print(type(dts[0].time()))

#
# # df['Year']= year
# # df['Month'] = month
data['Day'] = [time.day for time in dts]
data['Times'] = dts
data['Time'] = [time.time() for time in dts]




#
#
#
#
days = list(set(data['Day']))
# print(type(days[0]))
#
#
#
group_by_day = data.groupby('Day')
# print(list(group_by_day.get_group(13)['Time']))


# for d in days:
#     print(list(group_by_day.get_group(d)['Time']),list(group_by_day.get_group(d)['No:Transaction']))


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('X SMS TRANSACTION'),
    dcc.Graph(id='sms',
              figure={
                  'data': [
                      go.Scatter(
                          x=list(group_by_day.get_group(d)['Times']),
                          y=list(group_by_day.get_group(d)['No:Transaction']),
                          text=str(d),
                          mode='markers',
                          opacity=0.7,
                          marker={
                              'size': 3,
                              'line': {'width': 0.1, 'color': 'white'}
                                },
                          name=str(d)
                ) for d in days

            ],
                  'layout': go.Layout(
                    xaxis=dict(title='Time in Days',
                               type='date',
                               nticks= 30
                               ),
                    yaxis={'title': 'Frequency of Transaction'},
                    hovermode='closest'
            )

              }),
    dcc.Graph(id='sms2',
              figure={
                  'data': [
                      go.Scatter(
                          x=list(group_by_day.get_group(d)['Time']),
                          y=list(group_by_day.get_group(d)['No:Transaction']),
                          text=str(d),
                          mode='lines',
                          opacity=0.7,
                          marker={
                              'size': 3,
                              'line': {'width': 0.1, 'color': 'white'}
                          },
                          name=str(d)

                      ) for d in days

                  ],
                  'layout': go.Layout(
                      xaxis=dict(title='Time in Hour',
                                 nticks=24,
                                 tickangle=45,),

                      yaxis={'title': 'Frequency of Transaction'},
                      hovermode='closest'
                  )

              }),
dcc.Graph(id='smsmarkers',
              figure={
                  'data': [
                      go.Scatter(
                          x=list(group_by_day.get_group(d)['Time']),
                          y=list(group_by_day.get_group(d)['No:Transaction']),
                          text=str(d),
                          mode='markers',
                          opacity=0.7,
                          marker={
                              'size': 3,
                              'line': {'width': 0.1, 'color': 'white'}
                          },
                          name=str(d)

                      ) for d in days

                  ],
                  'layout': go.Layout(
                      xaxis=dict(title='Time in Hour',
                                 nticks= 27),
                      yaxis={'title': 'Frequency of Transaction'},
                      hovermode='closest'
                  )

              })



])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
