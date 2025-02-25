# Import required libraries
import pandas as pd
import dash
from dash import dcc
import dash_html_components as html
#import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('C://Users//EMV//Desktop//IBM Assignments//Module 10 - Capstone//spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# create dropdown options dictionary
data = {'label': spacex_df['Launch Site'].unique(), 
        'value': spacex_df['Launch Site'].unique()}
df = pd.DataFrame(data)

list_of_dicts = df.to_dict(orient='records')
dropdown_options=[{'label': 'All Sites', 'value': 'ALL'}] + list_of_dicts

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                                options=dropdown_options,
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart'),style={'display': 'flex'}),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div([dcc.RangeSlider(min=0, max=10000, step=1000, marks={0: '0', 10000: '10,000'}, value=[min_payload,max_payload], id='payload-slider'),
                                ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'), style={'display': 'flex'}),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig1 = px.pie(spacex_df, values='class', names='Launch Site', title='Lauch Total for All Launch Sites')
        return fig1
    else:
        fig1 = px.pie(filtered_df, values='class', names='Launch Site', title= f'Lauch Total for {entered_site}')
        return fig1

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])


def get_scatter(entered_site, payload):
    # Select data
    if entered_site == 'ALL':
        filtered_data2 = spacex_df[(spacex_df['Payload Mass (kg)']>=payload[0])&(spacex_df['Payload Mass (kg)']<=payload[1])]
        fig2 = px.scatter(data_frame=filtered_data2, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig2
    else:
        specific_df=spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_data2 = specific_df[(specific_df['Payload Mass (kg)']>=payload[0])&(specific_df['Payload Mass (kg)']<=payload[1])]
        fig2 = px.scatter(data_frame=filtered_data2, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig2
            
# Run the app
if __name__ == '__main__':
    app.run_server()
