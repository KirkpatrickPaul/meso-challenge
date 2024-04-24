from plotly import graph_objects as go
from data import getYears, companies

def create_graph(limitYears = None):
  fig = go.Figure()
  years = getYears(companies, limitYears)
  def getValueForYear(year):
    for p in company.performance:
      if p.date.year == year: 
        return p.value
  for company in companies:
    performanceByYear = list(map(getValueForYear, years))
    
    fig.add_trace(go.Bar(x=years,
                        y=performanceByYear,
                        name=company.name,
                        marker_color=company.color,
                        visible=True if company.visible else 'legendonly'
      ))

  fig.update_layout(
    title='Predicted Companies Performance Compared to Total Market',
    xaxis_tickfont_size=14,
    yaxis=dict(
      title='Percent of Total Market',
      titlefont_size=16,
      tickfont_size=14,
    ),
    legend=dict(
      x=0,
      y=1.0,
      bgcolor='rgba(255, 255, 255, 0)',
      bordercolor='rgba(255, 255, 255, 0)',
      borderwidth=3
    ),
    barmode='group',
    bargap=0.25,
    bargroupgap=0,
  )
  return fig