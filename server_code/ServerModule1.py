import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.files import data_files

from datetime import datetime
from plotly import graph_objects as go
from plotly import express as px
import pandas as pd
import altair as alt


@anvil.server.callable
def get_data(sheet_name='Electricity'):
  #file = anvil.server.get_asset('3-EM_consumption_data_template_Coatinc_voorbeeld.xlsx')
  file = data_files['3-EM_consumption_data_template_Coatinc_voorbeeld.xlsx']
  # Read the xlsx file into a pandas DataFrame
  df = pd.read_excel(file, sheet_name=sheet_name)
  # Optionally, perform any data manipulation here if needed
  # For example, you might want to convert dates, fill NaNs, etc.
  df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
  df['Timestamp'] = pd.to_datetime(df['Timestamp'])
  # Set the timestamp column as the index
  df.set_index('Timestamp', inplace=True)
  for i in range(len(df)):
    df["Unit"].iat[i] = df["Unit"].iat[0]
  # Resample the data to daily frequency
  df_daily = df.resample('D').sum()
  df_daily.reset_index(inplace=True)
  # Return the DataFrame to the client
  return df_daily.to_dict('records')

@anvil.server.callable
def get_new_data(file):
  #file = anvil.server.get_asset('3-EM_consumption_data_template_Coatinc_voorbeeld.xlsx')
  file = data_files[file]
  # Read the CSV file into a pandas DataFrame
  df = pd.read_excel(file)
  # Optionally, perform any data manipulation here if needed
  # For example, you might want to convert dates, fill NaNs, etc.
  df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
  df['Timestamp'] = pd.to_datetime(df['Timestamp'])
  # Set the timestamp column as the index
  df.set_index('Timestamp', inplace=True)
  for i in range(len(df)):
    df["Unit"].iat[i] = df["Unit"].iat[0]
  # Resample the data to daily frequency
  df_daily = df.resample('D').sum()
  df_daily.reset_index(inplace=True)
  # Return the DataFrame to the client
  return df_daily.to_dict('records')

@anvil.server.callable
def get_plot_data():
    # Lees het CSV-bestand
    file = data_files['gas_consumption_production.csv']
    df = pd.read_csv(file)
    #Ensure the 'Datetime' column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Set the timestamp column as the index
    df.set_index('timestamp', inplace=True)
    # Bereken de verhouding productie/consumptie
    df['Consumption/Production'] = df['consumption'] / df['production']
    # Resample the data to daily frequency
    df = df.resample('W').sum()
    df.reset_index(inplace=True)
    scatter = gen_scatterplot(df)
    bar = gen_bar_plot(df)
    return scatter, bar

@anvil.server.callable
def gen_scatterplot(dataframe):
    df = dataframe
    # Maak de scatterplot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['production'],
        y=df['consumption'],
        mode='markers',
        marker=dict(size=10,
                    color=df['Consumption/Production'],# Gebruik de ratio voor de kleur zet hier productie per consumptie unit
                    colorscale='aggrnyl',
                    showscale=True,
                    colorbar=dict(
                        title=dict(
                            text='Production per Consumption Unit',  # Titel van de kleurenschaal
                            side='top'  # Locatie van de titel
                        )
                    )),  # Toon een kleurenschaal
        text=df['timestamp'],  # Voeg datums toe als hover-text
        hovertemplate='Production: %{x}<br>Consumption: %{y}<br>Timestamp: %{text}<extra></extra>',
    ))
    # Pas de layout aan
    fig.update_layout(
        title='Production/Consumption rate on weekly basis.',
        xaxis_title='Production',
        yaxis_title='Gas Consumption',
        xaxis=dict(type='linear'),
        yaxis=dict(type='linear')
    )
    # Converteer de figuur naar een dictionary
    plot_dict1 = fig.to_dict()
    return plot_dict1

@anvil.server.callable
def gen_bar_plot(dataframe):
    fig = px.bar(dataframe, x='timestamp', y='production', color='consumption',
             color_continuous_scale='aggrnyl', hover_name='timestamp')
 
    # Update layout to set bargap to 0 and y-axis minimum value to 0
    fig.update_layout(bargap=0, yaxis=dict(minallowed=0))
    
    plot_dict1 = fig.to_dict()
    return plot_dict1

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
    file = data_files['gas_consumption_production-2.csv']
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