from unittest import *
from src.pyoink.values.chart import Chart, Column, Box, Direction, Price, Prices
from test.data import simple_chart_data
import json

class TestChart(TestCase):
  def setUp(self) -> None:
    pass

  def tearDown(self) -> None:
    pass

  def test_add_price(self):
    chart = Chart("TST", 1.0, 3)
    price = {"h": 4.0, 'l': 3.0}
    chart.addPrice(price)
    self.assertEqual(len(chart.columns), 1)
    self.assertEqual(chart.columns[0].boxes[0].price, 4.0)


    price = {"h" : 4.0, "l": 1.0}
    chart.addPrice(price)
    self.assertEqual(len(chart.columns[0].boxes), 4)
    boxes = chart.columns[0].boxes
    self.assertGreater(boxes[0].price, boxes[-1].price)

  def test_reversal(self):
    chart = Chart("TST", 1.0, 3)
    price = {"h" : 6.0, "l": 1.0}
    chart.addPrice(price)

    price = {'h': 5.0, "l": 4.0}
    chart.addPrice(price)

    self.assertEqual(len(chart.columns), 2)
    self.assertEqual(chart.last_column.boxes[0].price, 2.0)
    self.assertEqual(chart.last_box.price, 5.0)

  def test_simple_chart(self):
    chart = Chart("TST", 1.0, 3)

    simple_chart: Chart = chart.generate(simple_chart_data)

    self.assertEqual(len(simple_chart.columns), 3)
    self.assertEqual(simple_chart.columns[0].amount, 5)
    self.assertEqual(simple_chart.columns[1].amount, 4)
    self.assertEqual(simple_chart.columns[2].amount, 3)
  
  def test_find_highest_column(self):
    chart = Chart("TST", 1.0, 3)

    simple_chart: Chart = chart.generate(simple_chart_data)
    index = simple_chart.findHighestColumn([0,1,2])
    self.assertEqual(index, 1)

  def test_find_lowest_column(self):
    chart = Chart("TST",1.0,3)
    simple_chart: Chart = chart.generate(simple_chart_data)
    index = simple_chart.findLowestColumn([0,1,2])
    self.assertEqual(index,0)

  def test_trends(self):
    chart = Chart("TST",1.0,3)
    simple_chart: Chart = chart.generate(simple_chart_data)
    simple_chart.generateTrends()
    self.assertEqual(len(simple_chart.trends), 2)
  
  def test_real(self):
    with open("test/ABIO.json", 'r') as f:
      dig_chart_data = json.load(f)
    
    prices = Prices.fromDict("ABIO", dig_chart_data)
    box_size = Chart.getBoxSizeATR(prices)
    print(box_size)
    chart = Chart("LINC", box_size, 3)
    dig_chart: Chart = chart.generate(dig_chart_data)
    dig_chart.generateTrends()
    dig_chart.toHtml("linc.html")
    
    # trend = dig_chart.trends[0]
    # box = chart.columns[0].lowest_box
    # print(trend.boxes[0].distance(box))
    # print(dig_chart.columns[-1].amount)
    # print(dig_chart.trends[-1].direction)

