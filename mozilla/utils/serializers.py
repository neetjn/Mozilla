import json
from r2dto import Serializer, ValidationError
from typing import List


def to_json(serializer: Serializer, dto: object):
  base = serializer(object=dto)
  base.validate()
  return json.dumps(base.data)


def from_json(serializer: Serializer, payload: str):
  base = serializer(data=json.loads(payload))
  base.validate()
  return base.object


class LengthValidator:

  def __init__(self, min: int, max: int):
    self.min = min
    self.max = max

  def validate(self, field, data):
    size = len(data)
    if size < self.min or size > self.max:
      raise ValidationError(
          f'Field "{field.name}" must be greater than or equal to {self.min}'
          ' or less than or equal to {self.max} in length')


class CharLenValidator(LengthValidator):
  pass


class InValidator:

  def __init__(self, values: List[object]):
    self.values = values

  def validate(self, field, data):
    if data not in self.values:
      raise ValidationError(
          f'Expected field "{field.name}" of value "{data}" to be of value {self.values}')
