from falcon import before, after, Request, Response

from mozilla.core.accounts import get_account_by_id, get_account_by_name, \
    delete_account_by_name, delete_account_by_id, account_to_dto, create_account
from mozilla.hooks.responders import auto_respond, request_body, response_body
from mozilla.mediatypes import AccountDtoSerializer, AccountCreationDtoSerializer


class AccountResource:

  route = '/accounts/{name}'

  @before(auto_respond)
  @after(response_body, AccountDtoSerializer)
  def on_get(self, req: Request, res: Response, name: str):
    res.body = account_to_dto(get_account_by_name(name))

  @before(auto_respond)
  def on_delete(self, req: Request, res: Response, name: str):
    delete_account_by_name(name)


class AccountV2Resource:

  route = '/v2/accounts/{id}'

  @before(auto_respond)
  @after(response_body, AccountDtoSerializer)
  def on_get(self, req: Request, res: Response, id: str):
    res.body = account_to_dto(get_account_by_id(id))

  @before(auto_respond)
  def on_delete(self, req: Request, res: Response, id: str):
    delete_account_by_id(id)


class AccountCollectionResource:

  route = '/accounts'

  @before(auto_respond)
  @before(request_body, AccountCreationDtoSerializer)
  @after(response_body, AccountDtoSerializer)
  def on_post(self, req: Request, res: Response):
    res.body = account_to_dto(
        create_account(req.payload))

