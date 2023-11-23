from mongoengine import Document, CASCADE
from mongoengine.fields import ReferenceField, DateTimeField, ListField, StringField


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE, required=True)
    qoute = StringField(required=True)
