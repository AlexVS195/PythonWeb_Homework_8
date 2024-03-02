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
channel.queue_declare(queue='email_queue')

# Функція для імітації надсилання електронного листа
def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.email}...")
        # Імітуємо надсилання листа, позначаємо контакт як повідомлення відправлено
        contact.message_sent = True
        contact.save()
        print("Email sent successfully.")
    else:
        print("Contact not found.")

# Функція обробки повідомлення
def callback(ch, method, properties, body):
    message = json.loads(body)
    print("Received email:", message)
    send_email(message["contact_id"])

# Вказуємо RabbitMQ, яку функцію викликати для обробки повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for email messages...')
channel.start_consuming()