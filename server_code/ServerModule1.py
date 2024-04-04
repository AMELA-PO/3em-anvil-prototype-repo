import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import pydantic
from typing import Optional



class Stroom(pydantic.BaseModel):
  kWU: Optional[float] #Optional maakt dit veld niet verplicht voor de class
  Gas: Optional[float]
  Stroomleverancier: str

@anvil.server.callable
def getData(file):
  Userdata = file

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
