from falcon import before, after, Request, Response

from mozilla.core.transactions import get_transaction_by_id, create_transaction, \
    get_transactions_by_account, transaction_to_dto, transactions_to_collection_dto
from mozilla.hooks.responders import auto_respond, request_body, response_body
from mozilla.mediatypes import TransactionDtoSerializer, TransactionTypes, \
    TransactionCreationDtoSerializer, TransactionCollectionDtoSerializer


class TransactionResource:

  route = '/transaction/{id}'

  @before(auto_respond)
  @after(response_body, TransactionDtoSerializer)
  def on_get(self, req: Request, res: Response, id: str):
    res.body = transaction_to_dto(get_transaction_by_id(id))


class TransactionV2CollectionResource:

  route = '/v2/accounts/{id}/transactions'

  @before(auto_respond)
  @after(response_body, TransactionCollectionDtoSerializer)
  def on_get(self, req: Request, res: Response, id: str):
    res.body = transactions_to_collection_dto(
        get_transactions_by_account(id))


class TransactionDepositResource:

  route = '/accounts/{name}/deposit'

  @before(auto_respond)
  @before(request_body, TransactionCreationDtoSerializer)
  @after(response_body, TransactionDtoSerializer)
  def on_post(self, req: Request, res: Response, name: str):
    res.body = transaction_to_dto(create_transaction(
      name, TransactionTypes.DEPOSIT, req.payload.amount))


class TransactionWithdrawalResource:

  route = '/accounts/{name}/withdraw'

  @before(auto_respond)
  @before(request_body, TransactionCreationDtoSerializer)
  @after(response_body, TransactionDtoSerializer)
  def on_post(self, req: Request, res: Response, name: str):
    res.body = transaction_to_dto(create_transaction(
      name, TransactionTypes.WITHDRAWAL, req.payload.amount))

