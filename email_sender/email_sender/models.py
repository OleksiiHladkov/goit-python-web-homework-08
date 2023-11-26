from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, BooleanField

from datetime import datetime


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    created = DateTimeField(default=datetime.now())
    is_send = BooleanField(default=False)
    send_date = DateTimeField()
