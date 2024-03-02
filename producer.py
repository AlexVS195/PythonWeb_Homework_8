import pika
from faker import Faker
from mongoengine import connect
from models import Contact, ContactMethod
import json

# Підключення до бази даних MongoDB
connect("myFirstDatabase",
        host="mongodb+srv://osymashk:<Langeron2024!>@cluster0.oepyyjj.mongodb.net/",
        retryWrites=True,
        w="majority",
        appName="Cluster0")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черг для SMS та email
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

# Генеруємо фейкові контакти та додаємо їх до бази даних
fake = Faker()
for _ in range(5):
    contact_method = fake.random_element(elements=[ContactMethod.EMAIL.value, ContactMethod.SMS.value])
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        contact_method=contact_method
    )
    contact.save()

# Поміщаємо кожний контакт у відповідну чергу залежно від способу надсилання
for contact in Contact.objects:
    message = {"contact_id": str(contact.id)}
    if contact.contact_method == ContactMethod.EMAIL.value:
        channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=json.dumps(message))
    print("Sent:", message)

connection.close()