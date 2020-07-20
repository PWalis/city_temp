import pandas as pd
import plotly.graph_objects as go

class vis():
    '''
    Creates a visualization from given data
    '''
    
    def __init__(self, df):
        self.df = df
    
    def create_vis(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['AvgTemperature'], mode='markers', name='data', line={'color':'black'}))
        fig.update_layout(plot_bgcolor='white')
        return fig