import math
from pyoink.values.direction import Direction

class Box:
  def __init__(self, price_data, direction: str, box_size: float=1.0):
    self.direction = direction
    self.box_size: float = box_size

    if isinstance(price_data, float):
      raw_price = price_data
    elif self.direction == Direction.down:
      raw_price = price_data["l"]
    else:
      raw_price = price_data["h"]

    self.raw_price = raw_price

    if direction == Direction.up:
      self.price: float = Box.roundDown(raw_price, self.box_size)
    elif direction == Direction.down:
      self.price: float = Box.roundUp(raw_price, self.box_size)

  def __str__(self):
    return f"Box -> direction: {self.direction} | box_size: {self.box_size} | raw_price: {self.raw_price} | price: {self.price}"

  def __eq__(self, other: 'Box') -> bool:
    if other == None:
      return False
    
    return self.price == other.price
  
  def __gt__(self, other: 'Box'):
    if other is None:
      return False
    
    return self.price > other.price

  def __lt__(self, other: 'Box'):
    if other == None:
      return False
    
    return self.price < other.price

  def __le__(self, other: 'Box'):
    if other == None:
      return False
    
    return self.price <= other.price

  def __ge__(self, other: 'Box'):
    if other == None:
      return False
    
    return self.price >= other.price
  
  def __mul__(self, other: 'Box'):
    if isinstance(other, int):
      return Box(self.price*other, self.direction, self.box_size)
    
    return Box(self.price*other.price, direction=self.direction, box_size=self.box_size)

  def next(self) -> 'Box':
    if self.direction == Direction.down and self.price == 0:
      raw_price = 0.0
    elif self.direction == Direction.down:
      raw_price = self.price - self.box_size
    else:
      raw_price = self.price + self.box_size
    
    return Box(raw_price, self.direction, box_size = self.box_size)

  def prev(self) -> 'Box':
    if self.direction == Direction.up and self.price == 0:
      raw_price = 0.0
    elif self.direction == Direction.down:
      raw_price = self.price + self.box_size
    else:
      raw_price = self.price - self.box_size
    
    return Box(raw_price, self.direction, box_size=self.box_size)
  
  def inc(self) -> 'Box':
    raw_price = self.price + self.box_size
    return Box(raw_price, self.direction, box_size=self.box_size)

  def dec(self) -> 'Box':
    if self.price == 0:
      raw_price = 0.0
    else:
      raw_price = self.price - self.box_size
    
    return Box(raw_price, self.direction, box_size=self.box_size)

  @staticmethod
  def round(value):
    return round(value, 2)

  @staticmethod
  def getBoxes(raw_price, box_size):
    count = 0
    raw_price = Box.round(raw_price)
    while count <= raw_price:
      count = count + box_size

    high = Box.round(count)
    low = Box.round(high - box_size)

    if low == raw_price:
      high = low
    elif high == raw_price:
      low = high
  
    return [low, high]

  @staticmethod
  def roundDown(price, box_size):
    boxes = Box.getBoxes(price, box_size)
    return boxes[0]

  @staticmethod
  def roundUp(price, box_size):
    boxes = Box.getBoxes(price, box_size)
    return boxes[1]

  def distance(self, other_box: 'Box') -> int:
    if other_box == None:
      return 0

    price = int(self.price * 100)
    other_price = int(other_box.price * 100)
    box_size = int(self.box_size * 100)

    difference = abs(price - other_price) // box_size

    return difference