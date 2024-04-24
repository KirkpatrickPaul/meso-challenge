from flask import Flask
from dash import Dash, dcc, html, Input, Output, State, callback, ctx
from graph import create_graph
from table import create_table
from data import toggle_meso
server = Flask (__name__)

@server.route('/')
def hello_world():
  return 'Hello MesoAI!'
 
app = Dash(server=server, routes_pathname_prefix='/dash/')
table = create_table()
graph = create_graph()
tableTitle = html.H2('Predicted Companies Performance Raw Data', style={'font-family': 'sans-serif', 'padding-left': '5px'})
yearOptions = (
  {'label': '3 Years', 'value': '3'},
  {'label': '6 Years', 'value': '6'},
  {'label': '10 Years', 'value': '10'},  
  )
buttonText = {'conservative': 'Use Hopeful Estimate', 'hopeful': 'Use Conservative Estimate'}

app.layout = html.Div([
  dcc.Graph(figure=graph, id='ai-graph'), 
  html.Hr(), 
  html.Div(style={'display':'flex', 'justify-content': 'space-around'},
    children=[html.Div([
      html.Label(['Forecast Time:'], htmlFor='year-dropdown', style={'font': '18px sans-serif'}),
      dcc.Dropdown(options=yearOptions, value='10', id='year-dropdown', style={'max-width': '20vw', 'font': '18px sans-serif'}, clearable = False),
      html.Button('Use Conservative Estimate', id='estimate-button', n_clicks=0, 
                  style={':hover':{'backgroundColor': '#6a3ba8'}, 'margin-top': '5px', 'padding': '10px 14px', 'background-color': '#8f50e2', 'color': 'white', 'font': '18px sans-serif semibold', 'border': 'none', 'border-radius': '8px', 'box-shadow': '0 6px 12px #444444'})]),
      html.Div([
        tableTitle, 
        html.Table(children=table, style={'font': '18px sans-serif', 'border-collapse': 'collapse'}, id='ai-table')], 
        style={'max-width': 'fit-content', 'margin-inline': 'auto'})
    ])
  ])

@callback(
  [Output('estimate-button', 'children'),
  Output('ai-graph', 'figure'),
  Output('ai-table', 'children')],
  [Input('estimate-button', 'n_clicks'),
  Input('year-dropdown', 'value')],
  )
def toggle_estimate(n_clicks, value):
  input_id = ctx.triggered[0]["prop_id"].split(".")[0]
  if input_id == 'estimate-button': 
    toggle_meso()
  newEstimate = 'conservative' if n_clicks % 2 else 'hopeful'
  year = int(value)
  return buttonText[newEstimate], create_graph(year), create_table(year)

if __name__ == "__main__":
  app.run_server(debug=True)