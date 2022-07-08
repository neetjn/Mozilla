from datetime import datetime, timezone
from uuid import uuid4


def generate_uuid():
  return str(uuid4()).replace('-', '')


def get_timestamp():
  return int(datetime.now(timezone.utc).timestamp())
