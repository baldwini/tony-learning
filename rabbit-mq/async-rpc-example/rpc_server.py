import asyncio
import aiormq
import aiormq.abc


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


async def on_message(message:aiormq.abc.DeliveredMessage):
    n = int(message.body.decode())

    print(f" [.] fib({n})")
    response = str(fib(n)).encode()

    await message.channel.basic_publish(
        response, routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),

    )

    await message.channel.basic_ack(message.delivery.delivery_tag)
    print('Request complete')


async def main():
    # Perform connection
    connection = await aiormq.connect("amqp://guest:guest@localhost/")

    # Creating a channel
    channel = await connection.channel()

    # Declaring queue
    declare_ok = await channel.queue_declare('rpc_queue')

    print(declare_ok.queue)

    # Start listening the queue with name 'hello'
    await channel.basic_consume(declare_ok.queue, on_message)


loop = asyncio.get_event_loop()
loop.create_task(main())

# we enter a never-ending loop that waits for data
# and runs callbacks whenever necessary.
print(" [x] Awaiting RPC requests")
loop.run_forever()