import json
import pika
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime

# Carrega variáveis do .env
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY")

# Configuração de credenciais e conexão
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Declara Exchange e Fila
channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct', durable=True)
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)

# Publica mensagens com UUID
for i in range(1000):
    item = dict(
        id=str(uuid.uuid4()), 
        name="User" + str(i), 
        created_at=datetime.utcnow().isoformat()
    )

    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=RABBITMQ_ROUTING_KEY,
        body=json.dumps(item),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    print(f" [x] Sent 'User' messageId: {item['id']}")

connection.close()
