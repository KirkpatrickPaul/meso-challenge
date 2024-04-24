from dash import Dash, html
from data import getVisibleCompanies, getYears

def create_table(limitYears = None):
  dataRows = []
  visibleCompanies = getVisibleCompanies()
  years = getYears(visibleCompanies, limitYears)
  # initialize yearCells with a label for the company names so that the years line up with the data
  yearCells = [html.Th('Company Name', style={'padding': '0 5px 0 10px'}, className='company-name')]
  for year in years:
    yearCells.append(html.Th(year, style={'padding': '0 10px 0 10px'}))
  dataRows.append(html.Tr(yearCells, className='year-cells'))

  for company in visibleCompanies:
    dataCells = [html.Th(company.name, className='company-name')]
    for idx, p in enumerate(company.performance):
      if idx + 1 > len(years): break
      i = idx
      while i + 1 < len(years) and years[i] != p.date.year:
        dataCells.append(html.Td('-'))
        i += 1

      dataCells.append(html.Td(p.value))
    
    # 1 is added to years to acount for the Company Name cell
    while len(years) + 1 > len(dataCells):
      dataCells.append(html.Td('-'))
    dataRows.append(html.Tr(dataCells, style={'background-color': company.color}))

  return dataRows