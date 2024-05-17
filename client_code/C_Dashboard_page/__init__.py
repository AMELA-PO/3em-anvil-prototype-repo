from ._anvil_designer import C_Dashboard_pageTemplate
from ..B_SES_config_page import B_SES_config_page
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class C_Dashboard_page(C_Dashboard_pageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_option = None
        self.show_popup()
        
        self.drop_down_kpi.selected_value = self.drop_down_kpi.placeholder

        self.Energy_Performance_Panel.visible = True
        self.Toggle_Preformance.icon = "fa:caret-down"
        self.Financial_Performance_Panel.visible = True
        self.Toggle_Financials.icon = "fa:caret-down"
        # Any code you write here will run before the form opens.
    
    def show_popup(self):
        popup = B_SES_config_page()
        popup.set_event_handler('x-close-popup', self.on_popup_close)
        alert(popup, large=True, dismissible=False)

    def on_popup_close(self, **event_args):
        print('should close')
        if self.selected_option:
            # Proceed with the main content
            self.label_1.text = f"Selected option: {self.selected_option}"
        #Plot the data
        gas_data_old = anvil.server.call_s('get_data', 'Gas') 
        print('silent loading data')
        electricity_data_old = anvil.server.call_s('get_data', 'Electricity')  
        gas_data_new = anvil.server.call_s('get_new_data', 'salestool_gas_consumption_new.xlsx')  
        electricity_data_new = anvil.server.call_s('get_new_data', 'salestool_electricity_consumption_new.xlsx') 
        self.configure_energy_plot(gas_data_old, gas_data_new, self.Plot_LineChart_Gas_Old_Nieuw, 'Gas', 'orange', 'green')
        self.configure_energy_plot(electricity_data_old, electricity_data_new, self.Plot_LineChart_Electricity_Old_Nieuw, 'Electricity', 'blue', 'orange')

    
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
    
    def drop_down_kpi_change(self, **event_args):
        if self.drop_down_kpi.selected_value == "CAPEX":
            self.outlined_1.text = "€ 1.000.000"
            self.outlined_1_label.visible = False
            self.outlined_2_label.visible = False
            self.outlined_2.visible = False
        if self.drop_down_kpi.selected_value == "OPEX":
            self.outlined_1.text = "€ 550.000"
            self.outlined_2.text = "€ 500.000"
            self.outlined_1_label.visible = True
            self.outlined_2_label.visible = True
            self.outlined_2.visible = True
        if self.drop_down_kpi.selected_value == "TCO":
            self.outlined_1.text = "€ 1.500.000"
            self.outlined_1_label.visible = False
            self.outlined_2_label.visible = False
            self.outlined_2.visible = False
        if self.drop_down_kpi.selected_value == "IRR":
            self.outlined_1.text = "10.72 %"
            self.outlined_1_label.visible = False
            self.outlined_2_label.visible = False
            self.outlined_2.visible = False
        if self.drop_down_kpi.selected_value == "ROI":
            self.outlined_1.text = "15 Years"
            self.outlined_1_label.visible = False
            self.outlined_2_label.visible = False
            self.outlined_2.visible = False
        # if self.drop_down_kpi.selected_value == "Terugverdientijd":
        #     self.outlined_1.text = "15 Years"
        #     self.outlined_1_label.visible = False
        #     self.outlined_2_label.visible = False
        #     self.outlined_2.visible = False
        pass