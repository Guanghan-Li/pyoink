from src.pyoink.values.chart import Chart, Column, Box, Direction

simple_chart_data = [
  {'h': 15.50, 'l': 12.90},
  {'h': 12.20, 'l': 11.70},
  {'h': 12.60, 'l': 10.90},
  {'h': 14.10, 'l': 11.95},
  {'h': 15.99, 'l': 13.80},
  {'h': 15.10, 'l': 12.00}
]

chart = Chart("TST", 1.0, 3)

simple_chart: Chart = chart.generate(simple_chart_data)
simple_chart.print()