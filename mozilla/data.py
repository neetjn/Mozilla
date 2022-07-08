from peewee import SqliteDatabase, Model, ForeignKeyField, CharField, TextField, BooleanField, FloatField, IntegerField, PrimaryKeyField

from mozilla.constants import MZ_DB_NAME


db = SqliteDatabase(f'{MZ_DB_NAME}.db', {
  'journal_mode': 'wal',
  'cache_size': 1024 * 64})

db.connect()


class MzModel(Model):
  class Meta:
    database = db


class Account(MzModel):
  id = TextField(primary_key=True)
  name = CharField(unique=True)
  balance = FloatField(default=0.00)
  updated = IntegerField(null=True)
  created = IntegerField()
  is_deleted = BooleanField(default=False)
  deleted = IntegerField(null=True)


class Transaction(MzModel):
  id = TextField(primary_key=True)
  account = ForeignKeyField(Account)
  type = CharField(null=False)
  amount = FloatField(default=0.00)
  created = IntegerField()


def drop_database():
  db.drop_tables([Account, Transaction])
  db.create_tables([Account, Transaction])

