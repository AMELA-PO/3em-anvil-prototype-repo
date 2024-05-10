import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.files import data_files

from datetime import datetime
from plotly import graph_objects as go
import pandas as pd
import altair as alt


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
def render_chart_heatbar():
    df = load_data_prodcon()

    brush = alt.selection_interval(encodings=['x'])

    base = alt.Chart(df).mark_bar().encode(
        # alt.X("timestamp:T", bin=alt.Bin(step=0.5)),
        x="timestamp:T",
        y="production:Q",
        color=alt.Color("consumption:Q", scale=alt.Scale(scheme="viridis"), title="Consumption"),
    ).properties(
        title="Production vs Consumption",
        width=800,
        height=400
    )

    upper = base.encode(alt.X('timestamp:T').scale(domain=brush))

    lower = base.properties(
        height=60
    ).add_params(brush)

    chart = alt.vconcat(upper, lower)

    chart.save('/tmp/chart_heatbar.html')
    
    return anvil.media.from_file('/tmp/chart_heatbar.html', 'text/html')

def load_data_prodcon():
    file = data_files['gas_consumption_production.csv']
    return pd.read_csv(file)

@anvil.server.callable
def render_chart_scatter():
    df = load_data_prodcon()
    
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x='consumption:Q',
        y='production:Q',
    )

    chart.save('/tmp/chart_scatter.html')
    
    return anvil.media.from_file('/tmp/chart_scatter.html', 'text/html')