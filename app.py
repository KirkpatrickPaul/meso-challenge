from flask import Flask
from dash import Dash, dcc, html, Input, Output, State, callback, ctx
from graph import create_graph
from table import create_table
from data import toggle_meso, companies
server = Flask (__name__)

@server.route('/')
def hello_world():
  return 'Hello MesoAI!'
 
app = Dash(server=server, routes_pathname_prefix='/dash/')
table = create_table()
graph = create_graph()
tableTitle = html.H2('Predicted Companies Performance Raw Data', style={'padding-left': '5px'})
yearOptions = (
  {'label': '3 Years', 'value': '3'},
  {'label': '6 Years', 'value': '6'},
  {'label': '10 Years', 'value': '10'},  
  )
buttonText = {'conservative': 'Use Hopeful Estimate', 'hopeful': 'Use Conservative Estimate'}

app.layout = html.Div([
  dcc.Graph(figure=graph, id='ai-graph'), 
  html.Hr(), 
  html.Div(className='flex-div',
    children=[html.Div([
      html.Label(['Forecast Time:'], htmlFor='year-dropdown'),
      dcc.Dropdown(options=yearOptions, value='10', id='year-dropdown', className='dropdown', clearable = False),
      html.Button('Use Conservative Estimate', id='estimate-button', n_clicks=0)]),
      html.Div([
        tableTitle, 
        html.Table(children=table, id='ai-table')], 
        style={'max-width': 'fit-content', 'margin-inline': 'auto'})
    ])
  ])

@callback(
  [Output('estimate-button', 'children'),
  Output('ai-graph', 'figure'),
  Output('ai-table', 'children')],
  [Input('estimate-button', 'n_clicks'),
  Input('year-dropdown', 'value'),
  Input('ai-graph', 'restyleData'),
  State('ai-graph', 'figure')],
  )
def update_data(n_clicks, value, restyleData, figure):
  input_id = ctx.triggered[0]["prop_id"].split(".")[0]
  newEstimate = 'conservative' if n_clicks % 2 else 'hopeful'
  year = int(value)
  if input_id == 'estimate-button': toggle_meso()
  graph = figure
  if input_id == 'ai-graph':
    # This extracts the index of the company that was clicked
    idx = restyleData[1][0]
    graphCompany = figure['data'][idx]
    company = next(c for c in companies if c.name == graphCompany['name'])
    if 'visible' in graphCompany.keys() and graphCompany['visible'] == 'legendonly': company.hide()
    else: company.makeVisible()
  else: graph = create_graph(year)
  return buttonText[newEstimate], graph, create_table(year)

if __name__ == "__main__":
  app.run_server(debug=True)