import pandas as pd
import plotly.graph_objects as go

class vis():
    '''
    Creates a visualization from given data
    '''
    
    def __init__(self, df):
        self.df = df
        self.location = list(df[['Region', 'Country', 'State', 'City']].iloc[0])

    def loc_string(self, location):
        country = location[1]
        state = location[2]
        city = location[3]
        if state is not '' :
            return f'{city}, {state}, {country}'
        else:
            return f'{city}, {country}'

    def create_vis(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df['Date'], y=self.df['AvgTemperature'], mode='markers', name='data', line={'color':'black'}))
        fig.update_layout(plot_bgcolor='white',
                          annotations=[
                              dict(
                                  x=0.5,
                                  y=-0.15,
                                  showarrow=False,
                                  text='Date',
                                  font_size=20,
                                  xref='paper',
                                  yref='paper'
                              ),
                              dict(
                                  x=-0.04,
                                  y=0.5,
                                  showarrow=False,
                                  text='Avg Temp (Fahrenheit)',
                                  textangle=-90,
                                  font_size=20,
                                  xref='paper',
                                  yref='paper'
                              ),
                              dict(
                                  x=0.03,
                                  y=1.2,
                                  showarrow=False,
                                  text=self.loc_string(self.location),
                                  font_size=20,
                                  xref='paper',
                                  yref='paper'
                              )
                          ],
                          autosize=False,
                          margin=dict(
                              b=60
                          )
                          )
        return fig

