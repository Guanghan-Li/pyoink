from unittest import *
from pyoink.values.box import Box, Direction

class TestBox(TestCase):
  def setUp(self) -> None:
    pass

  def tearDown(self) -> None:
    pass

  def test_box_up(self):
    box = Box(1.01, Direction.up, box_size=1.0)
    self.assertEqual(box.price, 1.0)

    box = Box(1.99, Direction.up, box_size=1.0)
    self.assertEqual(box.price, 1.0)
  
  def test_box_down(self):
    box = Box(1.01, Direction.down, box_size=1.0)
    self.assertEqual(box.price, 2.0)

    box = Box(1.99,Direction.down, box_size=1.0)
    self.assertEqual(box.price, 2.0)
  
  def test_box_size(self):
    box = Box(1.01, Direction.down, box_size=0.50)
    self.assertEqual(box.price, 1.50)

    box = Box(1.99, Direction.up, box_size=0.50)
    self.assertEqual(box.price, 1.50)

    box = Box(1.00, Direction.down, box_size=0.12)
    self.assertEqual(box.price, 1.08)
    
    box = Box(1.00, Direction.up, box_size=0.12)
    self.assertEqual(box.price, 0.96)
  
  def test_box_difference(self):
    box1 = Box(1.00, Direction.down, box_size=1.00)
    box2 = Box(4.00, Direction.down, box_size=1.00)

    result = box2.distance(box1)
    self.assertEqual(result, 3)

    result2 = box1.distance(box2)
    self.assertEqual(result2, 3)

    box1 = Box(1.08, Direction.down, box_size=0.12)
    box2 = Box(0.60, Direction.down, box_size=0.12)
    result = box2.distance(box1)
    self.assertEqual(result, 4)
  
  def test_box_next_down(self):
    box = Box(4.00, Direction.down, box_size=1.00)
    next_box = box.next()

    self.assertEqual(next_box.price, 3.0)

  def test_box_next_up(self):
    box = Box(4.00, Direction.up, box_size=1.00)
    next_box = box.next()

    self.assertEqual(next_box.price, 5.0)
  
  def test_price_dictionary(self):
    price = {"h": 1.99, "l": 1.01}
    box1 = Box(price, Direction.down, box_size=1.00)
    box2 = Box(price, Direction.up, box_size = 1.00)
  
  def test_next_box_negative(self):
    box = Box(1.00, Direction.down, box_size=1.00)
    box2 = box.next()
    box3 = box2.next()

    self.assertEqual(box2.price, 0.0)
    self.assertEqual(box3.price, 0.0)


    