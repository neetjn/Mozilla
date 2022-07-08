from mozilla.data import Account
from mozilla.errors import ResourceNotAvailableError, ResourceNotFoundError
from mozilla.mediatypes import AccountCreationDto, AccountDto
from mozilla.utils import generate_uuid, get_timestamp


def account_to_dto(account: Account):
  return AccountDto(
    id=account.id,
    name=account.name,
    balance=account.balance,
    updated=account.updated,
    created=account.created,
    is_deleted=account.is_deleted,
    deleted=account.deleted)


def get_account_by_name(name: str):
  try:
    return Account.get(Account.name == name)
  except Account.DoesNotExist:
    raise ResourceNotFoundError


def get_account_by_id(id: str):
  try:
    return Account.get_by_id(id)
  except Account.DoesNotExist:
    raise ResourceNotFoundError


def create_account(account_creation_dto: AccountCreationDto):
  name = account_creation_dto.name
  try:
    get_account_by_name(name)
  except ResourceNotFoundError:
    account = Account.create(
      id=generate_uuid(),
      name=name,
      created=get_timestamp())
    return account
  raise ResourceNotAvailableError(f'Account with name "{name}" already exists.')


def delete_account(account: Account):
  account.is_deleted = True
  account.deleted = get_timestamp()
  account.save()


def delete_account_by_name(name: str):
  account = get_account_by_name(name)
  delete_account(account)


def delete_account_by_id(id: str):
  account = get_account_by_id(id)
  delete_account(account)


def update_account_balance(account: Account, amount: float):
  account.balance += amount
  account.updated = get_timestamp()
  account.save()


def update_account_balance_by_name(name: str, amount: float):
  account = get_account_by_name(name)
  update_account_balance(account, amount)


def update_account_balance_by_id(id: str, amount: float):
  account = get_account_by_id(id)
  update_account_balance(account, amount)
