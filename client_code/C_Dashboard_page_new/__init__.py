from ._anvil_designer import C_Dashboard_page_newTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class C_Dashboard_page_new(C_Dashboard_page_newTemplate):
    def __init__(self, option_data=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_option = None
        self.option_data = option_data
        self.fill_labels()        
        self.drop_down_kpi.selected_value = self.drop_down_kpi.placeholder

        self.Energy_Performance_Panel.visible = True
        self.Toggle_Preformance.icon = "fa:caret-down"
        self.Financial_Performance_Panel.visible = True
        self.Toggle_Financials.icon = "fa:caret-down"
        # Any code you write here will run before the form opens.

        # #Plot the data
        # gas_data_old = anvil.server.call('get_data', 'Gas') 
        # electricity_data_old = anvil.server.call('get_data', 'Electricity')  
        # gas_data_new = anvil.server.call('get_new_data', 'salestool_gas_consumption_new.xlsx')  
        # electricity_data_new = anvil.server.call('get_new_data', 'salestool_electricity_consumption_new.xlsx') 
        # self.configure_energy_plot(gas_data_old, gas_data_new, self.Plot_LineChart_Gas_Old_Nieuw, 'Gas', 'orange', 'green')
        # self.configure_energy_plot(electricity_data_old, electricity_data_new, self.Plot_LineChart_Electricity_Old_Nieuw, 'Electricity', 'blue', 'orange')

    def fill_labels(self):
        labels = [
            "total_electricity_cons",
            "total_electricity_cons_new",
            "electricity_savings_percentage",
            "total_gas_cons",
            "total_gas_cons_new",
            "gas_savings_percentage",
            "total_co2",
            "total_co2_new",
            "co2_savings_percentage",
            "total_energy_cost",
            "total_energy_cost_new",
            "energy_cost_savings",
            "energy_cost_savings_percentage",
            "capex",
            "opex_old",
            "opex_new",
            "tco",
            "irr",
            "roi"
        ]
        for label in labels:
            value = self.option_data.get(label, "N/A")
            label_obj = getattr(self, label)
            label_obj.text = str(value)

    
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

    def configure_energy_plot(self, plot_data_old, plot_data_new, plot_object, plot_name, plot_data_old_color, plot_data_new_color): 
        # Create a Plotly figure
        fig = go.Figure(data=[go.Scatter(
            x=[item['Timestamp'] for item in plot_data_old],
            y=[item['Consumption'] for item in plot_data_old],
            mode='lines',
            line=dict(
            color=plot_data_old_color,  # Set line color to orange
            width=2  # Optional: Set line width
            ),
            name='Old Consumption'
            
        ),
        go.Scatter(
            x=[item['Timestamp'] for item in plot_data_new],
            y=[item['Consumption'] for item in plot_data_new],
            mode='lines',
            line=dict(
            color=plot_data_new_color,  # Set line color to orange
            width=2  # Optional: Set line width
            ),
            name='New Consumption')])
        
        # Update layout
        fig.update_layout(
            title=plot_name+' Consumption Over Time',
            xaxis_title='Time',
            yaxis_title='Consumption',
            xaxis=dict(
            tickformat='%Y-%m-%d %H',
            type='date',  # Ensure the x-axis is treated as date
            #range=[start_timestamp, end_timestamp]  # Set the initial zoom range
            ),
            yaxis=dict(
            autorange=True  # Enable automatic scaling based on the data
            )
        )
        plot_object.figure = fig

    def values_invisible(self):
        self.capex.visible = False
        self.opex_old.visible = False
        self.opex_new.visible = False
        self.tco.visible = False
        self.irr.visible = False
        self.roi.visible = False
        self.before_label.visible = False
        self.after_label.visible = False
    
    def drop_down_kpi_change(self, **event_args):
        self.values_invisible()
        if self.drop_down_kpi.selected_value == "CAPEX":
            self.capex.visible = True
        if self.drop_down_kpi.selected_value == "OPEX":
            self.before_label.visible = True
            self.after_label.visible = True
            self.opex_old.visible = True
            self.opex_new.visible = True
        if self.drop_down_kpi.selected_value == "TCO":
            self.tco.visible = True
        if self.drop_down_kpi.selected_value == "IRR":
            self.irr.visible = True
        if self.drop_down_kpi.selected_value == "ROI":
            self.roi.visible = True
        # if self.drop_down_kpi.selected_value == "Terugverdientijd":
        #     self.outlined_1.text = "15 Years"
        #     self.outlined_1_label.visible = False
        #     self.outlined_2_label.visible = False
        #     self.outlined_2.visible = False
        pass

    def Resetpage(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('A_Upload_data_page')
