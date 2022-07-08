import falcon
from mozilla.mediatypes import HttpMethods
from mozilla.utils.serializers import from_json, to_json


StatusMethodMap = {
  HttpMethods.GET: falcon.HTTP_200,
  HttpMethods.POST: falcon.HTTP_201,
  HttpMethods.PUT: falcon.HTTP_204,
  HttpMethods.DELETE: falcon.HTTP_204,
}


def auto_respond(req, res, resource, params):
  res.status = StatusMethodMap.get(req.method, StatusMethodMap.get(HttpMethods.GET))


def request_body(req, res, resource, params, serializer_class):
  req.payload = from_json(serializer_class, req.stream.read())


def response_body(req, res, resource, serializer_class, content_type='application/json'):
  print(serializer_class)
  print(res.body)
  if res.body:
    res.body = to_json(serializer_class, res.body)
  res.content_type = content_type
