# asyncio, tcp клиент
import asyncio
async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection("127.0.0.1",
                                                    8181,
                                                    loop=loop)

    print("send: %r" % message)

    writer.write(message.encode())
    data = await reader.read(1024)
    print(data)
    writer.close()

loop = asyncio.get_event_loop()
message = "hello World!"
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()