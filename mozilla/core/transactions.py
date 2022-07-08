from decimal import Decimal
from typing import List

from mozilla.constants import MZ_MAX_OVERDRAFT
from mozilla.core.accounts import get_account_by_name, update_account_balance
from mozilla.data import Transaction
from mozilla.errors import ResourceNotAvailableError
from mozilla.mediatypes import TransactionDto, TransactionCollectionDto, \
    TransactionCreationDto, TransactionTypes
from mozilla.utils import generate_uuid, get_timestamp


def transaction_to_dto(transaction: Transaction):
  return TransactionDto(
    id=transaction.id,
    account=str(transaction.account),
    type=transaction.type,
    amount=transaction.amount,
    created=transaction.created)


def transactions_to_collection_dto(transactions: List[Transaction]):
  return TransactionCollectionDto(
      count=len(transactions),
      items=[transaction_to_dto(t) for t in transactions])


def get_transaction_by_id(id: str):
  return Transaction.get_by_id(id)


def get_transactions_by_account(account: str):
  return Transaction.select().where(Transaction.account == account)


def create_transaction(name: str, type: str, amount: float):
  account = get_account_by_name(name)
  amount = float(format(Decimal(amount), '.2f'))
  if type == TransactionTypes.WITHDRAWAL and amount > 0:
    amount *= -1
  if type == TransactionTypes.DEPOSIT and amount < 0:
    raise ResourceNotAvailableError(f'Attempting to deposit invalid value.')
  balance = account.balance + amount
  if balance < MZ_MAX_OVERDRAFT:
    raise ResourceNotAvailableError(
      f'Resource is not available,'
      ' account "{name}" balance cannot process the requested transaction of {amount}')
  update_account_balance(account, amount)
  transaction = Transaction.create(
    id=generate_uuid(),
    account=account.id,
    type=type,
    amount=amount,
    created=get_timestamp())
  return transaction

