import pika
import configparser
from pathlib import Path

# config parcer
config = configparser.ConfigParser()
path_to_config = Path(__file__).parent.joinpath("config_rabbit.ini")
config.read(path_to_config)

rabbit_user = config.get("docker_rabbit", "user")
rabbit_pass = config.get("docker_rabbit", "pass")
rabbit_host = config.get("docker_rabbit", "host")
rabbit_port = config.get("docker_rabbit", "port")

# connection
credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, credentials=credentials))

channel = connection.channel()