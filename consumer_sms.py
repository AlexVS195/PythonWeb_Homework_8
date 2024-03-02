import pika
from mongoengine import connect, Document, StringField, BooleanField
import json

# Підключення до бази даних MongoDB
connect("myFirstDatabase",
        host="mongodb+srv://osymashk:<Langeron2024!>@cluster0.oepyyjj.mongodb.net/",
        retryWrites=True,
        w="majority",
        appName="Cluster0")

# Модель для контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sms_queue')

# Функція для імітації надсилання SMS
def send_sms(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending SMS to {contact.phone_number}...")
        # Імітуємо надсилання SMS, позначаємо контакт як повідомлення відправлено
        contact.message_sent = True
        contact.save()
        print("SMS sent successfully.")
    else:
        print("Contact not found.")

# Функція обробки повідомлення
def callback(ch, method, properties, body):
    message = json.loads(body)
    print("Received SMS:", message)
    send_sms(message["contact_id"])

# Вказуємо RabbitMQ, яку функцію викликати для обробки повідомлень
channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for SMS messages...')
channel.start_consuming()