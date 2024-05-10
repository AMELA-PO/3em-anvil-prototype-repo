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

        self.drop_down_kpi.selected_value = self.drop_down_kpi.placeholder

        self.Energy_Performance_Panel.visible = True
        self.Toggle_Preformance.icon = "fa:caret-down"
        self.Financial_Performance_Panel.visible = True
        self.Toggle_Financials.icon = "fa:caret-down"
        # Any code you write here will run before the form opens.

    def Toggle_Preformance_click(self, **event_args):
        if self.Energy_Performance_Panel.visible:
            self.Energy_Performance_Panel.visible = False
            self.Toggle_Preformance.icon = "fa:caret-right"
        else:
            self.Energy_Performance_Panel.visible = True
            self.Toggle_Preformance.icon = "fa:caret-down"
        pass

    def Toggle_Financials_click(self, **event_args):
        if self.Financial_Performance_Panel.visible:
            self.Financial_Performance_Panel.visible = False
            self.Toggle_Financials.icon = "fa:caret-right"
        else:
            self.Financial_Performance_Panel.visible = True
            self.Toggle_Financials.icon = "fa:caret-down"
        pass
