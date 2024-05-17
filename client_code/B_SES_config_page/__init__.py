from ._anvil_designer import B_SES_config_pageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..C_Dashboard_page import C_Dashboard_page

class B_SES_config_page(B_SES_config_pageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.Sustainability_Dropdown.items = [
            ("Electric heating", "electric_heating"),
            ("Electric heating + solar panel", "electric_heating_solarpv"),
            ("Electric heating + solar panel + battery storage", "electric_heating_solarpv_battery")
        ]
        self.option_data = {}


    def Proceed_Button_click(self, **event_args):
        selected_option = self.Sustainability_Dropdown.selected_value
        if selected_option:
            print('even wachten....')
            print(self.option_data)
            dashboard_page = C_Dashboard_page(option_data=self.option_data)
            open_form(dashboard_page)

    def get_option_data(self, selected_option):
        print(selected_option)
        data = {'option1_electric_heating': {'total_electricity_cons': '972975.35 kWh', 'total_electricity_cons_new': '2998725.35 kWh', 'electricity_savings_percentage': '-208.2 %', 'total_gas_cons': '650476.9 m³', 'total_gas_cons_new': '450933.18 m³', 'gas_savings_percentage': '30.68 %', 'total_co2': '1557718.34 kg', 'total_co2_new': '1561141.73 kg', 'co2_savings_percentage': '-0.22 %', 'total_energy_cost': '€486487.68', 'total_energy_cost_new': '€1499362.68', 'energy_cost_savings': '€-1012875.0', 'energy_cost_savings_percentage': '-208.2 %', 'capex': '€500600.0', 'opex_old': '€5058358.21', 'opex_new': '€5321137.43', 'tco': '€5821737.43', 'irr': 'nan %', 'roi': '-0.52 %'}, 'option2_electric_heating_solarpv': {'total_electricity_cons': '972975.35 kWh', 'total_electricity_cons_new': '2215822.5 kWh', 'electricity_savings_percentage': '-127.74 %', 'total_gas_cons': '650476.9 m³', 'total_gas_cons_new': '450933.18 m³', 'gas_savings_percentage': '30.68 %', 'total_co2': '1557718.34 kg', 'total_co2_new': '1399026.04 kg', 'co2_savings_percentage': '10.19 %', 'total_energy_cost': '€486487.68', 'total_energy_cost_new': '€1107911.25', 'energy_cost_savings': '€-621423.57', 'energy_cost_savings_percentage': '-127.74 %', 'capex': '€1602400.0', 'opex_old': '€12645895.51', 'opex_new': '€16075237.52', 'tco': '€17677637.52', 'irr': 'nan %', 'roi': '-2.14 %'}, 'option3_electric_heating_solarpv_battery': {'total_electricity_cons': '972975.35 kWh', 'total_electricity_cons_new': '2193081.84 kWh', 'electricity_savings_percentage': '-125.4 %', 'total_gas_cons': '650476.9 m³', 'total_gas_cons_new': '450933.18 m³', 'gas_savings_percentage': '30.68 %', 'total_co2': '1557718.34 kg', 'total_co2_new': '1394317.13 kg', 'co2_savings_percentage': '10.49 %', 'total_energy_cost': '€486487.68', 'total_energy_cost_new': '€1096540.92', 'energy_cost_savings': '€-610053.24', 'energy_cost_savings_percentage': '-125.4 %', 'capex': '€1930400.0', 'opex_old': '€12645895.51', 'opex_new': '€17786946.79', 'tco': '€19717346.79', 'irr': 'nan %', 'roi': '-2.66 %'}}
        self.option_data = data[selected_option]


    
    def Sustainability_Dropdown_change(self, **event_args):
        """This method is called when an item is selected"""
        option_map = {
            "electric_heating": "option1_electric_heating",
            "electric_heating_solarpv": "option2_electric_heating_solarpv",
            "electric_heating_solarpv_battery": "option3_electric_heating_solarpv_battery"
        }
        selected_option = option_map.get(self.Sustainability_Dropdown.selected_value)
        self.get_option_data(selected_option)
        

