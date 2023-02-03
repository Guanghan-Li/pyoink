from datetime import datetime
from dateutil import relativedelta
import pytz, itertools

class Price:
  def __init__(self, symbol, date: datetime, open, close, high, low):
    self.symbol = symbol
    self.date = datetime.fromtimestamp(date.timestamp(), tz=pytz.UTC)
    self.open = open
    self.close = close
    self.high = high
    self.low = low

  def __str__(self):
    date = self.date.strftime("%Y-%m-%d")
    return f"{self.symbol} -> date: {date} | o: {self.open} | c: {self.close} | h: {self.high} | l: {self.low}"
  
  def simpleDict(self):
    return {
      'o': self.open,
      'c': self.close,
      'h': self.high,
      'l': self.low
    }

  def toDict(self):
    return {
      "date": self.date,
      "open": self.open,
      "close": self.close,
      "high": self.high,
      "low": self.low
    }
  
  def toDict2(self):
    return {
      "date": self.date.strftime("%Y-%m-%d"),
      "open": self.open,
      "close": self.close,
      "high": self.high,
      "low": self.low
    }

  @staticmethod
  def get_either(d: dict, key1: str, key2: str):
    option1 = d.get(key1, None)
    option2 = d.get(key2, None)

    if option1:
      return option1
    
    if option2:
      return option2

  @staticmethod
  def fromDict(symbol, data):
    data.setdefault("date", datetime.now())
    o = Price.get_either(data, "o", "open")
    c = Price.get_either(data, "c", "close")
    h = Price.get_either(data, "h", "high")
    l = Price.get_either(data, "l", "low")
    return Price(
      symbol,
      data["date"],
      o,
      c,
      h,
      l
    )
  
  def stockSplit(self, new_rate, old_rate):
    self.open = round(self.open*new_rate/old_rate, 3)
    self.close = round(self.close*new_rate/old_rate, 3)
    self.high = round(self.high*new_rate/old_rate, 3)
    self.low = round(self.low*new_rate/old_rate, 3)
    return self

  def stockReverseSplit(self, new_rate, old_rate):
    self.open = round(self.open*old_rate/new_rate, 3)
    self.close = round(self.close*old_rate/new_rate, 3)
    self.high = round(self.high*old_rate/new_rate, 3)
    self.low = round(self.low*old_rate/new_rate, 3)
    return self