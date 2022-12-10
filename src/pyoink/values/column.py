from pyoink.values.box import Box, Direction

class Column:
  def __init__(self, direction: Direction, box_size: float, boxes: list[Box] = None):
    if boxes == None:
      self.boxes: list[Box] = []
    else:
      self.boxes: list[Box] = boxes
    self.direction: Direction = direction
    self.box_size: float = box_size
  
  def __str__(self):
    start = None
    end = None
    if self.amount > 0:
      start = self.boxes[0].price
      end = self.boxes[0].price
    
    if self.amount > 1:
      end = self.boxes[-1].price

    return f"Column -> direction: {self.direction} | box_size: {self.box_size} | amount: {self.amount} | start: {start} | end: {end}"

  @property
  def last_box(self) -> Box:
    if len(self.boxes) < 1:
      return None
    return self.boxes[-1]

  @property
  def first_box(self) -> Box:
    if len(self.boxes) < 1:
      return None
    return self.boxes[0]
  
  @property
  def highest_box(self) -> Box:
    if len(self.boxes) < 1:
      return None
    if self.first_box > self.last_box:
      return self.first_box
    else:
      return self.last_box

  @property
  def lowest_box(self) -> Box:
    if len(self.boxes) < 1:
      return None
    if self.first_box < self.last_box:
      return self.first_box
    else:
      return self.last_box

  @property
  def first_box(self) -> Box:
    if len(self.boxes) < 1:
      return None
    return self.boxes[0]

  @property
  def amount(self) -> int:
    return len(self.boxes)
  
  def addBox(self, box: Box):
    boxes = [box]
    for col_box in self.boxes:
      if box == col_box:
        return

    if self.amount > 0:
      boxes += self._getMiddleBoxes(box)

    self.boxes += boxes
    is_down = self.direction == Direction.down
    self.boxes = sorted(self.boxes, key=lambda box: box.price, reverse=is_down)

  def boxInColumn(self, box: Box):
    for col_box in self.boxes:
      if box == col_box:
        return True
    return False

  def getRange(self, box1: Box, box2: Box):
    if box1 > box2:
      big_box = box1
      small_box = box2
    else:
      big_box = box2
      small_box = box1

    big_price = int(big_box.price * 100)
    small_price = int(small_box.price * 100)
    box_size = int(self.box_size * 100)
    
    boxes = []
    for i in range(small_price+box_size, big_price, box_size):
      price = i/100
      box = Box(price, self.direction, self.box_size)
      boxes.append(box)
    
    return boxes


  def _getMiddleBoxes(self, current_box: Box) -> list[Box]:
    last_box = self.last_box
    boxes = []

    if len(self.boxes)<1:
      return [current_box]

    if self.boxInColumn(current_box):
      return []
  
    r = self.getRange(current_box, self.boxes[-1])
    return r