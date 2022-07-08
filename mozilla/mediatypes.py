from dataclasses import dataclass
from r2dto import fields, validators, Serializer
from typing import List

from mozilla.utils.serializers import CharLenValidator, InValidator


class HttpMethods:
  GET = 'GET'
  POST = 'POST'
  PUT = 'PUT'
  DELETE = 'DELETE'


class TransactionTypes:
  WITHDRAWAL = 'WITHDRAWAL'
  DEPOSIT = 'DEPOSIT'


name_validator = CharLenValidator(min=1, max=20)
transaction_type_validator = InValidator(values=[TransactionTypes.WITHDRAWAL, TransactionTypes.DEPOSIT])


@dataclass
class AccountCreationDto:
  name: str = None


class AccountCreationDtoSerializer(Serializer):
  name = fields.StringField(required=True, validators=[name_validator])

  class Meta:
    model = AccountCreationDto


@dataclass
class AccountDto:
  id: str = None
  name: str = None
  balance: float = None
  updated: int = None
  created: int = None
  is_deleted: bool = False
  deleted: int = None


class AccountDtoSerializer(Serializer):
  id = fields.StringField()
  name = fields.StringField(validators=[name_validator])
  balance = fields.FloatField()
  updated = fields.IntegerField()
  created = fields.IntegerField()
  is_deleted = fields.BooleanField(name='isDeleted')
  deleted = fields.IntegerField()

  class Meta:
    model = AccountDto


@dataclass
class TransactionCreationDto:
  amount: float = 0.0


class TransactionCreationDtoSerializer(Serializer):
  amount = fields.FloatField()

  class Meta:
    model = TransactionCreationDto


@dataclass
class TransactionDto:
  id: str = None
  account: str = None
  type: str = None
  amount: float = 0
  created: str = None


class TransactionDtoSerializer(Serializer):
  id = fields.StringField()
  account = fields.StringField()
  type = fields.StringField(validators=[transaction_type_validator])
  amount = fields.FloatField()
  created = fields.IntegerField()

  class Meta:
    model = TransactionDto


@dataclass
class TransactionCollectionDto:
  count: int = 0
  items: List[TransactionDto] = None


class TransactionCollectionDtoSerializer(Serializer):
  count = fields.IntegerField()
  items = fields.ListField(fields.ObjectField(TransactionDtoSerializer))

  class Meta:
    model = TransactionCollectionDto

