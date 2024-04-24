from datetime import date
class AIData:
  def __init__(self, performance, name, color):
    self.performance = performance
    self.name = name
    self.color = color
    self.visible = True
    self.altPerformance = None

  def hide(self):
    self.visible = False

  def makeVisible(self):
    self.visible = True

  def setAltPerformance(self, performance):
    self.altPerformance = performance

  def togglePerformance(self):
    a = self.performance
    self.performance = self.altPerformance
    self.altPerformance = a

class Performance:
  def __init__(self, date, value):
    self.date = date
    self.value = value

def createPerformance(years, performanceData):
  if len(years) != len(performanceData): raise Exception('Years and performanceData must be the same length!')
  performance = []
  for i, year in enumerate(years):
    performance.append(Performance(
      date = date(year, 12, 31),
      value = performanceData[i]
    ))
  return performance

_years = [*range(2025,2035)]

meso = AIData(createPerformance(_years, [2, 3, 5, 6, 8, 11, 14, 15, 17, 20]), 'MesoAI', '#8f50e2')
meso.setAltPerformance(createPerformance(_years, [2, 3, 4, 5, 6, 9, 11, 12, 13, 14]))

copilot = AIData(createPerformance(_years, [8, 8, 9, 10, 10, 11, 9, 9, 8, 9]), 'Github Copilot', '#030330')
synthesia = AIData(createPerformance(_years, [6, 8, 11, 14, 16, 17, 15, 14, 14, 13]), 'Synthesia', '#bc0055')
gemini = AIData(createPerformance([*range(2025,2032)], [12, 10, 9, 7, 3, 1, 1]), 'Gemini', '#82700d')

companies = [meso, copilot, synthesia, gemini]

def getVisibleCompanies():
  return list(filter(lambda c : c.visible, companies))

def getYears(companies, limit = None):
  years = []
  for company in companies:
    for p in company.performance:
      if p.date.year in years: continue
      else: years.append(p.date.year)
  years.sort()
  if limit != None and len(years) > limit: years = years[:limit]
  return years

def toggle_meso():
  meso.togglePerformance()