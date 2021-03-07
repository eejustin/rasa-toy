import json
import pika


if __name__ == '__main__':

    # RabbitMQ credentials with username and password
    credentials = pika.PlainCredentials('admin', 'password')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='rasa_core_events', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def call_back(ch, method, properties, body):
        print('Received event {}'.format(json.loads(body)))


    channel.basic_consume(
        queue=queue_name,
        on_message_callback=call_back,
        auto_ack=True
    )

    channel.start_consuming()