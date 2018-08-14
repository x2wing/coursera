import asyncio
import re


class Server:

    def __init__(self):
        self.db = {}

    def response_generate(self, key):
        return key + ' ' +''.join(f'{i[1]} {i[0]}\n' for i in self.db[key])

    def _process_comand(self, rawdata):
        if re.findall(b'(put (.+?) (.+?) (\d+)\\n)', rawdata):
            key, value, timestamp = rawdata[3:-1].decode().split()
            if key not in self.db:
                self.db[key] = []
            self.db[key].append((int(timestamp), float(value)))
            print(self.db)
            return b'ok\n\n'
        elif re.findall(b'(get (.+?)\\n)', rawdata):
            key = rawdata.decode().split()[1]
            if key == '*':
                return ('ok\n' + '\n'.join(map(self.response_generate, self.db.keys())) + '\n').encode("utf8")
            else:
                return ('ok\n' + self.response_generate(key) + '\n').encode("utf8")
        else:
            print(rawdata)
            return b'error\nwrong command\n\n'
        # f"put {host_metric} {value} {timestamp}\n".encode("utf8")

    async def handle_echo(self, reader, writer):
        data = await reader.read(1024)
        response = self._process_comand(data)
        print(response)

        writer.write(response)

        message = data.decode()
        addr = writer.get_extra_info("peername")
        print("received %r from%r" % (message, addr))
        # writer.close()


serv = Server()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(serv.handle_echo, "127.0.0.1", 8888, loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
