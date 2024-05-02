from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Form1(Form1Template):  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  #This method is called when the button is clicked
  def UploadData_Click(self, **event_args):
    if self.ProdDataToggle.checked and self.Consumption_FileLoader.file and self.Production_FileLoader.file:
      # Code to execute if the checkbox is checked and both file uploaders are not empty
      print("UPLOAD CONSUMPTION AND PRODUCTION DATA")
      self.UploadData()
    elif self.ProdDataToggle.checked and self.Consumption_FileLoader.file:
      self.ErrorNoProductionData()
    elif self.ProdDataToggle.checked and self.Production_FileLoader.file:
      self.ErrorNoConsumptionData()
    elif self.ProdDataToggle.checked:
      self.ErrorNoConsumptionData()
      self.ErrorNoProductionData()
    elif self.Consumption_FileLoader.file != None:
      print('ONLY UPLOAD CONSUMPTION DATA')
      self.UploadData()

  def UploadData(self):
    result = alert(content="Wilt u doorgaan naar de visualisatie?",
               title="Data succesvol geupload!",
               large=True,
               buttons=[
                 ("Ga door", "Load_Visualisatie"),
                 ("Stop", "Doe niks")
               ])
    print(f"The user chose {result}")
    #anvil.server.call('getData', self.Consumption_FileLoader.file)
    #anvil.server.call('emit_server_ip', self.Consumption_FileLoader.file)

  def ErrorNoConsumptionData(self):
      self.ConsumptionUploadlabel.foreground = 'theme:Error'
      self.ConsumptionUploadlabel.bold = True

  def ErrorNoProductionData(self):
      self.ProductionUploadlabel.foreground = 'theme:Error'
      self.ProductionUploadlabel.bold = True

  def DefaultLabelState(self):
    self.ConsumptionUploadlabel.bold = False
    self.ConsumptionUploadlabel.foreground = 'theme:On Surface'
    self.ProductionUploadlabel.bold = False
    self.ProductionUploadlabel.foreground = 'theme:On Surface'

  #This method is called when a new file is loaded into ConsumptionFileLoader
  def Consumption_FileLoader_change(self, file, **event_args):
    self.ConsumptionUploadlabel.text = self.Consumption_FileLoader.file.name
    self.ConsumptionUploadlabel.bold = False
    self.ConsumptionUploadlabel.foreground = 'theme:On Surface'
    pass

  #This method is called when a new file is loaer in to ProductionFileLoader
  def Production_FileLoader_change(self, file, **event_args):
    self.ProductionUploadlabel.text = self.Production_FileLoader.file.name
    self.ProductionUploadlabel.bold = False
    self.ProductionUploadlabel.foreground = 'theme:On Surface'
    pass

  #This method is called when the ProdDataToggle checkbox is changed
  def ProdDataToggle_change(self, **event_args):
    self.ProductionContentPanel.visible = self.ProdDataToggle.checked
    self.DefaultLabelState()
    pass

  def ClearData_click(self, **event_args):
    self.Production_FileLoader.clear()
    self.Consumption_FileLoader.clear()
    self.ProdDataToggle.checked = False
    self.ProdDataToggle.raise_event('change')
    self.ProductionUploadlabel.text = '* .csv of .xlsx bestanden.'
    self.ConsumptionUploadlabel.text = '* .csv of .xlsx bestanden.'
    self.DefaultLabelState()
    pass


  