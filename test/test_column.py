from unittest import *
from pyoink.values.column import Column, Box, Direction

class TestColumn(TestCase):
  def setUp(self) -> None:
    pass

  def tearDown(self) -> None:
    pass

  def test_add_box(self):
    column = Column(Direction.down, 1.0)
    box1 = Box(4.0, Direction.down, 1.0)
    box2 = Box(1.0, Direction.down, 1.0)

    column.addBox(box1)
    column.addBox(box2)

    self.assertEqual(column.amount, 4)

  def test_add_box_up(self):
    column = Column(Direction.up, 1.0)
    box1 = Box(1.0, Direction.up, 1.0)
    box2 = Box(4.0, Direction.up, 1.0)

    column.addBox(box1)
    column.addBox(box2)
    
    self.assertEqual(column.amount, 4)

  def test_box_range(self):
    column = Column(Direction.up, 1.0)
    box1 = Box(1.0, Direction.up, 1.0)
    box2 = Box(4.0, Direction.up, 1.0)

    box_range: list[Box] = column.getRange(box1, box2)
    self.assertEqual(box_range[0].price, 2.0)
    self.assertEqual(box_range[1].price, 3.0)




