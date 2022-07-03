from abc import ABC, abstractmethod

class DimentionBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        return None

    @abstractmethod
    def __sub__(self, other):
        return None

    @abstractmethod
    def __repr__(self, other):
        return None

class DimentionValueBase(DimentionBase):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if type(other) == type(self):
            return Pixel(self.value + other.value)
        raise TypeError(f"Pixel cannot add with {type(other).__name__}")

    def __sub__(self, other):
        if type(other) == type(self):
            return Pixel(self.value - other.value)
        raise TypeError(f"Pixel cannot sub with {type(other).__name__}")

class Pixel(DimentionValueBase):
    def __repr__(self):
        return f"{self.value}px"

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

class Percentage(DimentionValueBase):
    def __repr__(self):
        return f"{self.value}%"

print(Pixel(5) + Percentage(6))