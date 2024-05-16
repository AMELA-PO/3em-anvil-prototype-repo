from ._anvil_designer import Sustainability_optionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Sustainability_options(Sustainability_optionsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.Sustainability_Dropdown.items = [
            ("Electric heating", "electric_heating"),
            ("Electric heating + solar panel", "electric_heating_solar"),
            ("Electric heating + solar panel + battery storage", "electric_heating_solar_battery")
        ]

    def Proceed_Button_click(self, **event_args):
        selected_option = self.Sustainability_Dropdown.selected_value
        if selected_option:
            # Store the selected option or pass it to the main form
            get_open_form().selected_option = selected_option
            self.raise_event('x-close-popup')
