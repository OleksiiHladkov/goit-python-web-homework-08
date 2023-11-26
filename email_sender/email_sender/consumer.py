import time
from datetime import datetime
import json
from bson import ObjectId

from connect_rebbit import channel
import connect_db
from models import Contact


channel.queue_declare(queue="test_queue", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def send_message():
    time.sleep(1)
    return True


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    if send_message():
        print(f" [x] Done: {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        contact = Contact.objects(id=ObjectId(message.get("id"))).first()
        contact.is_send = True
        contact.send_date = datetime.now()
        contact.save()
    else:
        print(f" [x] Failed: {method.delivery_tag}")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="test_queue", on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
