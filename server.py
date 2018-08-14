import asyncio


class Server:
    db = {}
    async def handle_echo(reader, writer):
        data = await reader.read(1024)

        message = data.decode()


        addr = writer.get_extra_info("peername")
        print("received %r from%r" % (message, addr))
        writer.write(b'ok\n\n')
        # writer.close()

    def Process_comand(self, rawdata):
        pass
        #f"put {host_metric} {value} {timestamp}\n".encode("utf8")




loop = asyncio.get_event_loop()
coro = asyncio.start_server(Server.handle_echo, "127.0.0.1", 8888, loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
