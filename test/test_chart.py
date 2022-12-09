from unittest import *
from src.pyoink.values.chart import Chart, Column, Box, Direction
from test.data import simple_chart_data

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
