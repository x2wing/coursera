import asyncio
import re


class Server:

    def __init__(self):
        self.db = {}

    def response_generate(self, key):
        return ''.join(f'{key} {i[1]} {i[0]}\n' for i in self.db[key])

    def _process_comand(self, rawdata):
        if re.findall(b'(put (.+?) (.+?) (\d+)\\n)', rawdata):
            key, value, timestamp = rawdata[3:-1].decode().split()
            if key not in self.db:
                self.db[key] = []
            ts_met = (int(timestamp), float(value))
            if self.db[key] and self.db[key][~0] == ts_met:
                self.db[key].pop()
            self.db[key].append(ts_met)

            # print(self.db)
            return b'ok\n\n'
        elif re.findall(b'(get (.+?)\\n)', rawdata):
            key = rawdata.decode().split()[1]

            if key == '*':
                # print('db', self.db.keys())
                server_otvet = ('ok\n' + '\n'.join(map(self.response_generate, self.db.keys())) + '\n')
                # print('g', server_otvet)
                server_otvet = server_otvet.replace('\n\n', '\n') + '\n'
                # print('r', server_otvet)
                return server_otvet.encode("utf8")
            elif key not in self.db.keys():
                return b'ok\n\n'
            else:
                return ('ok\n' + self.response_generate(key) + '\n').encode("utf8")
        else:
            # print(rawdata)
            return b'error\nwrong command\n\n'
        # f"put {host_metric} {value} {timestamp}\n".encode("utf8")

    async def handle_echo(self, reader, writer):
        while True:
            data = await reader.read(1024)
            if data:
                response = self._process_comand(data)
                # print('otvet servera', response)
                writer.write(response)
                # message = data.decode()
                # addr = writer.get_extra_info("peername")
                # print("received %r from%r" % (message, addr))
            else:
                break

        writer.close()


def run_server(host, port):
    serv = Server()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(serv.handle_echo, host, port, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server("127.0.0.1", 8888)
