import asyncio
import uuid
import aiormq
import aiormq.abc


class FibonacciRpcClient:
    def __init__(self):
        self.connection = None      # type: #aiormq.Connection
        self.channel = None         # type: #aiormq.Channel
        self.callback_queue = ''
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await aiormq.connect("amqp://guest:guest@localhost/")

        self.channel = await self.connection.channel()
        declare_ok = await self.channel.queue_declare(
            exclusive=True, auto_delete=True
        )

        print(declare_ok.queue)

        await self.channel.basic_consume(declare_ok.queue, self.on_response)

        self.callback_queue = declare_ok.queue

        return self

    async def on_response(self, message: aiormq.abc.DeliveredMessage):
        future = self.futures.pop(message.header.properties.correlation_id)
        future.set_result(message.body)

    async def call(self, n):
        correlation_id = str(uuid.uuid4())
        future = loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.basic_publish(
            str(n).encode(), routing_key='rpc_queue',
            properties=aiormq.spec.Basic.Properties(
                content_type='text/plain',
                correlation_id=correlation_id,
                reply_to=self.callback_queue,
            )
        )

        return int(await future)


async def main():
    fibonacci_rpc = await FibonacciRpcClient().connect()
    print(" [x] Requesting fib(30)")
    response = await fibonacci_rpc.call(30)
    print(r" [.] Got {response!r}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())