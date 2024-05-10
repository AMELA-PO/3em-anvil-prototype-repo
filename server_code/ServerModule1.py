import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.files import data_files

from datetime import datetime
from plotly import graph_objects as go
import pandas as pd


@anvil.server.callable
def get_data(sheet_name='Electricity'):
  #file = anvil.server.get_asset('3-EM_consumption_data_template_Coatinc_voorbeeld.xlsx')
  file = data_files['3-EM_consumption_data_template_Coatinc_voorbeeld.xlsx']
    
  # Read the CSV file into a pandas DataFrame
  df = pd.read_excel(file, sheet_name=sheet_name)
    
  # Optionally, perform any data manipulation here if needed
  # For example, you might want to convert dates, fill NaNs, etc.
  df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
  for i in range(len(df)):
    df["Unit"].iat[i] = df["Unit"].iat[0]
    
  # Return the DataFrame to the client
  return df.to_dict('records')
  
  # address = house_number + ' ' + street_name + ' ' + city
    
  # pv_output = anvil.server.call('calculate_solar_radiation_1year', address, roof_area)
  # yearly_pv_output = pv_output[0][0]
  # monthly_pv_output = pv_output[1]
  # energy_calc_output_text = "Your yearly solar energy potential: " \
  #                         + str(int(yearly_pv_output)) + " kWh" \
  #                         + "\n \n" + "Check out your expected monthly electricity production below!"
  
  # return [energy_calc_output_text, monthly_pv_output]


@anvil.server.callable
def render_chart_prodcon():
    import altair as alt

    df = load_data_prodcon()

    chart = alt.Chart(df).mark_bar().encode(
        x="datetime:T",
        y="production:Q",
        color=alt.Color("consumption:Q", scale=alt.Scale(scheme="viridis"), title="Consumption"),
    ).properties(
        title="Production vs Consumption",
        width=800,
        height=400
    )

    chart.save('/tmp/altair.html')
    
    return anvil.media.from_file('/tmp/altair.html', 'text/html')

def load_data_prodcon():
    file = data_files['production_consumption-2.csv']
    return pd.read_csv(file)