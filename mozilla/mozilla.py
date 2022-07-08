import falcon

from mozilla.errors import ErrorHandler
from mozilla.resources.accounts import AccountResource, AccountV2Resource, \
    AccountCollectionResource
from mozilla.resources.transactions import TransactionResource, TransactionDepositResource, \
    TransactionWithdrawalResource, TransactionV2CollectionResource


api = falcon.API()

api.add_error_handler(Exception, ErrorHandler.unexpected)
api.add_error_handler(falcon.HTTPError, ErrorHandler.http)
api.add_error_handler(falcon.HTTPStatus, ErrorHandler.http)

api.add_route(AccountResource.route, AccountResource())
api.add_route(AccountV2Resource.route, AccountV2Resource())
api.add_route(AccountCollectionResource.route, AccountCollectionResource())
api.add_route(TransactionResource.route, TransactionResource())
api.add_route(TransactionV2CollectionResource.route, TransactionV2CollectionResource())
api.add_route(TransactionDepositResource.route, TransactionDepositResource())
api.add_route(TransactionWithdrawalResource.route, TransactionWithdrawalResource())
