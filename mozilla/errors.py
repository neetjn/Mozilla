import traceback

from falcon import HTTPNotFound, HTTPConflict, HTTPUnauthorized, HTTPForbidden, \
    HTTPBadRequest, HTTPInternalServerError


class ErrorHandler:

  @staticmethod
  def http(ex, req, res, params):
    raise

  @staticmethod
  def unexpected(ex, req, res, params):
    ex_msg = ''.join(traceback.format_tb(ex.__traceback__))
    print(ex_msg)
    raise HTTPInternalServerError(ex.__class__.__name__, ex_msg)


class ResourceNotAvailableError(HTTPForbidden):

  def __init__(self, desc=None):
    super().__init__(
      description=desc or 'Resource is not available. '
                          'Try again at a later time.')


class ResourceNotFoundError(HTTPNotFound):

  def __init__(self, desc=None):
    super().__init__(description=desc or 'Resource was not found or was not available.')

