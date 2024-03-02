import enum
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, BooleanField


class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


class ContactMethod(enum.Enum):
    EMAIL = "email"
    SMS = "sms"


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)
    contact_method = StringField(choices=[method.value for method in ContactMethod], default=ContactMethod.EMAIL.value)
