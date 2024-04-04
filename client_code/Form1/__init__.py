from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  #This method is called when the button is clicked
  def button_1_click(self, **event_args):
    print("the button was clicked")
    if self.file_loader_1.file != None: #Check if the button has a file in it
      print(self.file_loader_1.file.name) #Display file name
    else:
      print("no file selected")
      self.Uploadlabel.foreground = 'theme:Error'
    pass
  #This method is called when a new file is loaded into this FileLoader
  def file_loader_1_change(self, file, **event_args):
    self.Uploadlabel.text = self.file_loader_1.file.name
    self.Uploadlabel.bold = True
    pass
  