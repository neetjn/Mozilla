import argparse
import json
import os
import gunicorn.app.base

from mozilla.constants import MZ_HOST, MZ_PORT, MZ_WORKERS
from mozilla.data import drop_database
from mozilla.mozilla import api


class MzStandalone(gunicorn.app.base.BaseApplication):

  def __init__(self, app, options=None):
    self.options = options or {}
    self.application = app
    super(MzStandalone, self).__init__()

  def load_config(self):
    config = dict(
      [(key, value) for key, value in self.options.items() if key in self.cfg.settings and value is not None])
    for key, value in config.items():
      self.cfg.set(key.lower(), value)

  def load(self):
    return self.application


if __name__ == '__main__':
  a = argparse.ArgumentParser()
  a.add_argument('--bootstrap', help='Bootstrap accounts.', type=int)
  a.add_argument('--app', action='store_true', help='Start rest api.')
  args, remaining_args = a.parse_known_args()
  if args.bootstrap:
    # TODO: add bootstrapping
    drop_database()
  if args.app or not args.bootstrap:
    options = {
      'bind': f'{MZ_HOST}:{MZ_PORT}',
      'workers': MZ_WORKERS,
    }
    MzStandalone(api, options).run()
