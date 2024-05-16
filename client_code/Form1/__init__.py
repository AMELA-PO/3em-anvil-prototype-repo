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
    #media = anvil.server.call('render_chart_scatter')
    #self.iframe_chart_scatter.url = media.get_url(True)
      
    #media = anvil.server.call('render_chart_heatbar')
    #self.iframe_chart_heatbar.url = media.get_url(True)

    #Dit is een quick fix. We laden nu al de data in voordat de gebruiker op de "gain insight" knop druk.
    #Deze functionaliteit hoor bij de submit_button_click()
    gas_data = anvil.server.call('get_data', 'Gas')  
    electricity_data = anvil.server.call('get_data', 'Electricity')  
    self.configure_energy_plot(gas_data, self.plot_1, 'Gas','orange')
    self.configure_energy_plot(electricity_data, self.plot_2, 'Electricity','blue')
    # Roep de serverfunctie aan om de plot te genereren
    plot_json = anvil.server.call('generate_scatter_plot')
    # Zet de JSON-plot om in een Plotly-figuur en toon deze
    self.plot_3.figure = plot_json

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
      self.submit_button_click()
    else:
      self.ErrorNoConsumptionData()

  def TEMPUPLOAD(self, **event_args):
    self.submit_button_click()

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
    self.ClearData.visible = True
    pass

  #This method is called when a new file is loaer in to ProductionFileLoader
  def Production_FileLoader_change(self, file, **event_args):
    self.ProductionUploadlabel.text = self.Production_FileLoader.file.name
    self.ProductionUploadlabel.bold = False
    self.ProductionUploadlabel.foreground = 'theme:On Surface'
    self.ClearData.visible = True
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
    self.ClearData.visible = False
    pass

  def submit_button_click(self, **event_args):    
    # gas_data = anvil.server.call('get_data', 'Gas')  
    # electricity_data = anvil.server.call('get_data', 'Electricity')  
    # self.configure_energy_plot(gas_data, self.plot_1, 'Gas','orange')
    # self.configure_energy_plot(electricity_data, self.plot_2, 'Electricity','blue')
    self.DataContentPanel.visible = False
    self.VisualisatiePanel.visible = True
    self.ResetButton.visible = True

  def configure_energy_plot(self, plot_data, plot_object, plot_name, plot_color): 
    # Create a Plotly figure
    fig = go.Figure(data=[go.Scatter(
        x=[item['Timestamp'] for item in plot_data],
        y=[item['Consumption'] for item in plot_data],
        mode='lines',
        line=dict(
        color=plot_color,  # Set line color to orange
        width=2  # Optional: Set line width
        ),
        name='Consumption'
    )])
    
    # Update layout
    fig.update_layout(
        title=plot_name+' Consumption Over Time',
        xaxis_title='Time',
        yaxis_title='Consumption',
        xaxis=dict(
          tickformat='%Y-%m-%d %H',
          type='date',  # Ensure the x-axis is treated as date
          #range=[0, 500],  # Set the initial zoom range
        ),
        yaxis=dict(
          autorange=True,  # Enable automatic scaling based on the data
          constrain='domain',
          constraintoward='center'
        )
    )
    
    # Display the figure in Anvil's Plot component
    plot_object.figure = fig
    
  def Resetpage(self, **event_args):
    self.DataContentPanel.visible = True
    self.VisualisatiePanel.visible = False
    self.ResetButton.visible = False

  def GotoDashboard(self, **event_args):
      open_form('Dashboard')
      pass

  