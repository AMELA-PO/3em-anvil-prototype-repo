from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go


class Dashboard(DashboardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.LoadAreaChart(self.Plot_AreaChart)

        # Any code you write here will run before the form opens.
    def LoadAreaChart(self, plot_object, **event_args):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy',
                            mode='none' # override default markers+lines
                            ))
        fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[3, 5, 1, 7], fill='tonexty',
                            mode= 'none'))
        
        #fig.show()
        # Display the figure in Anvil's Plot component
        plot_object.figure = fig
