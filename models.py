import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    joined_on = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    @classmethod
    def write_user(cls, username, password, is_admin, joined_on=None):
        if not joined_on:
            joined_on = datetime.date.today()
        try:
            with DATABASE.transaction():
                cls.create(username=username,
                           password=generate_password_hash(password),
                           is_admin=is_admin,
                           joined_on=joined_on)
        except IntegrityError:
            raise ValueError("User already exists")

    def get_user_entry(self, entry_id, user_id):
        try:
            return Entry.get((Entry.id == entry_id) & (Entry.user == user_id))
        except DoesNotExist:
            raise ValueError("No records available.")


class Entry(BaseModel):
    user = ForeignKeyField(User, backref='entries')
    title = TextField()
    date = DateField()
    time_spent = IntegerField()
    learnings = TextField()
    rememberings = TextField()

    @classmethod
    def write_entry(cls, user, title, time_spent, learnings, rememberings, date=None):
        if not date:
            date = datetime.date.today()
        try:
            with DATABASE.transaction():
                cls.create(user=user,
                           title=title,
                           time_spent=time_spent,
                           learnings=learnings,
                           rememberings=rememberings,
                           date=date)
        except IntegrityError:
            raise ValueError("Entry already exists")

    @classmethod
    def get_all_entries(cls):
        return cls.select()

    @classmethod
    def get_specific_entry(cls, entry_id):
       return cls.select().where(Entry.id == entry_id).get()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
