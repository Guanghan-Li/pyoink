from enum import Flag

class Direction(Flag):
  down = False
  up = True

  def opposite(self):
    return Direction(not self)
