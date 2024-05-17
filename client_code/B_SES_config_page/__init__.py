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
        data = {'option1_electric_heating': {'total_electricity_cons': 972975.3530000005, 'total_electricity_cons_new': 2998725.3529999945, 'electricity_savings_percentage': -208.20157404336564, 'total_gas_cons': 650476.8999999997, 'total_gas_cons_new': 450933.17712096334, 'gas_savings_percentage': 30.676527157080663, 'total_co2': 1557718.3428457067, 'total_co2_new': 1561141.7331428458, 'co2_savings_percentage': -0.2197695310491797, 'total_energy_cost': 486487.67650000023, 'total_energy_cost_new': 1499362.6764999973, 'energy_cost_savings': -1012874.999999997, 'energy_cost_savings_percentage': -208.20157404336564, 'capex': 500600.0, 'opex_old': 5058358.205305002, 'opex_new': 5321137.428546509, 'tco': 5821737.428546509, 'irr': "nan", 'roi': -0.5249285322443201}, 'option2_electric_heating_solarpv': {'total_electricity_cons': 972975.3530000005, 'total_electricity_cons_new': 2215822.4968110346, 'electricity_savings_percentage': -127.73675509651203, 'total_gas_cons': 650476.8999999997, 'total_gas_cons_new': 450933.17712096334, 'gas_savings_percentage': 30.676527157080663, 'total_co2': 1557718.3428457067, 'total_co2_new': 1399026.0387117905, 'co2_savings_percentage': 10.187483819700702, 'total_energy_cost': 486487.67650000023, 'total_energy_cost_new': 1107911.2484055173, 'energy_cost_savings': -621423.571905517, 'energy_cost_savings_percentage': -127.73675509651203, 'capex': 1602400.0, 'opex_old': 12645895.513262505, 'opex_new': 16075237.515219942, 'tco': 17677637.51521994, 'irr': "nan", 'roi': -2.140128558385821}, 'option3_electric_heating_solarpv_battery': {'total_electricity_cons': 972975.3530000005, 'total_electricity_cons_new': 2193081.83869737, 'electricity_savings_percentage': -125.39952650757115, 'total_gas_cons': 650476.8999999997, 'total_gas_cons_new': 450933.17712096334, 'gas_savings_percentage': 30.676527157080663, 'total_co2': 1557718.3428457067, 'total_co2_new': 1394317.1306361938, 'co2_savings_percentage': 10.489779038680677, 'total_energy_cost': 486487.67650000023, 'total_energy_cost_new': 1096540.919348685, 'energy_cost_savings': -610053.2428486848, 'energy_cost_savings_percentage': -125.39952650757115, 'capex': 1930400.0, 'opex_old': 12645895.513262505, 'opex_new': 17786946.785409465, 'tco': 19717346.785409465, 'irr': "nan", 'roi': -2.66320517620543}}
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
        

