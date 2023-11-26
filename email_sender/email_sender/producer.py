from pika import BasicProperties, spec
from faker import Faker

from datetime import datetime
import json

from connect_rebbit import channel, connection
from models import Contact
import connect_db


channel.exchange_declare(exchange="email_sender", exchange_type="direct")
channel.queue_declare(queue="test_queue", durable=True)
channel.queue_bind(exchange="email_sender", queue="test_queue")


def generate_fake_contacts():
    fake_data = Faker()

    for _ in range(20):
        contact = Contact(fullname=fake_data.name(), email=fake_data.email()).save()


def send_emails():
    contacts = Contact.objects(is_send=False)

    for contact in contacts:
        print(str(contact.id), type(str(contact.id)))
        message = {
            "id": str(contact.id),
            "payload": f"Task #{str(contact.id)}",
            "date": datetime.now().isoformat(),
            "text": f"Hello, {contact.fullname}!\nThis is a test. Do not answer to this message!"
        }


        channel.basic_publish(
            exchange="email_sender",
            routing_key="test_queue",
            body=json.dumps(message).encode(),
            properties=BasicProperties(delivery_mode=spec.PERSISTENT_DELIVERY_MODE),
        )
        print(" [x] Sent %r" % message)
    
    connection.close()


if __name__ == "__main__":
    print("generating fake contacts and write database...")
    generate_fake_contacts()
    print("start sending...")
    send_emails()
