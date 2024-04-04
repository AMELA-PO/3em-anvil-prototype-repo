import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import anvil.media
import pydantic
from typing import Optional
import pandas as pd



class Stroom(pydantic.BaseModel):
  kWU: Optional[float] #Optional maakt dit veld niet verplicht voor de class
  Gas: Optional[float]
  Stroomleverancier: str

@anvil.server.callable #makes it so you can call this function at client side
def getData(file):
  with anvil.media.TempFile(file) as filename:
    print(filename)
    Userdata = filename
  print(Userdata) 
  #df = pd.read_csv("file")
  df = pd.read_excel(Userdata, sheet_name="Sheet1") #Read the xlsx file and put it in a variable
  print(df.head(10)) #print the variable.

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
