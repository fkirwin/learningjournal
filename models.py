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
    def write_user(cls, username, password, joined_on, is_admin):
        try:
            with DATABASE.transaction():
                cls.create(username = username,
                    password = generate_password_hash(password),
                    joined_on = joined_on,
                    is_admin = is_admin)
        except IntegrityError:
            raise ValueError("User already exists")

    def get_all_user_entries(self):
        try:
            return Entry.select().where(Entry.user == self)
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
                cls.create(user = user,
                    title = title,
                    time_spent = time_spent,
                    learnings = learnings,
                    rememberings = rememberings,
                    date = date)
        except IntegrityError:
            raise ValueError("Entry already exists")



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()

initialize()
"""
Interesting feature     for each in u.get_all_user_entries().dicts():
    Entry.write_entry(User.get(User.id==1), "test", 1, "nada", "imember")
    Entry.write_entry(User.get(User.id==1), "bad", 1, "bad", "bad")
"""