from mongoengine import Document, CASCADE, ValidationError
from mongoengine.fields import ReferenceField, DateTimeField, ListField, StringField


def unique_fullname_validation(fullname):
    authors = Author.objects(fullname=fullname)
    if len(authors):
        raise ValidationError(f'Author "{fullname}" already exists!')


class Author(Document):
    fullname = StringField(required=True, validation=unique_fullname_validation)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE, required=True)
    qoute = StringField(required=True)
