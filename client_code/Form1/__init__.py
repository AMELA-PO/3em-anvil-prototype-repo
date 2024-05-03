from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


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
      self.submit_button_click()
    elif self.ProdDataToggle.checked and self.Consumption_FileLoader.file:
      self.ErrorNoProductionData()
    elif self.ProdDataToggle.checked and self.Production_FileLoader.file:
      self.ErrorNoConsumptionData()
    elif self.ProdDataToggle.checked:
      self.ErrorNoConsumptionData()
      self.ErrorNoProductionData()
    elif self.Consumption_FileLoader.file is not None:
      print('ONLY UPLOAD CONSUMPTION DATA')
      self.submit_button_click()
    else:
      self.ErrorNoConsumptionData()

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

  def submit_button_click(self, **event_args):    
    data = anvil.server.call('get_data', 'Gas')    
    self.configure_energy_plot(data)

  def configure_energy_plot(self, plot_data):
    # Create a Plotly figure
    for item in plot_data:
      print(item["Consumption"])
    #print(plot_data)
    # Create a Plotly figure
    fig = go.Figure(data=[go.Scatter(
        x=[item['Timestamp'] for item in plot_data],
        y=[item['Consumption'] for item in plot_data],
        mode='lines+markers',
        name='Consumption'
    )])
    
    # Update layout
    fig.update_layout(
        title='Energy Consumption Over Time',
        xaxis_title='Time',
        yaxis_title='Consumption',
        xaxis=dict(tickformat="%Y-%m-%d %H:%M:%S")
    )
    
    # Display the figure in Anvil's Plot component
    self.plot_1.figure = fig

  