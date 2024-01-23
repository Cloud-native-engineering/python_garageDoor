from enum import Enum


class GarageDoorState(Enum):
    CLOSED = 1,
    OPEN = 2,
    UNKNOWN = 3

    def __str__(self):
      if self.value == GarageDoorState.OPEN.value:
        return "open"
      elif self.value == GarageDoorState.CLOSED.value:
        return "closed"
      elif self.value == GarageDoorState.UNKNOWN.value:
        return "unknown"


def split_into_axis(raw_sensor_value: str):
    return [float(value) for value in raw_sensor_value.split(',')]


def eval_garage_door_state(raw_sensor_value: str) -> GarageDoorState:
    x, y, z = split_into_axis(raw_sensor_value)
    if y > 0.8:
        return GarageDoorState.CLOSED
    elif z < -0.8:
        return GarageDoorState.OPEN
    else:
        return GarageDoorState.UNKNOWN
