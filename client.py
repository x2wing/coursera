# создание сокета, контекстный менеджер
# сервер
import socket
import re


#
# with socket.socket() as sock:
#     sock.bind(("", 10001))
#     sock.listen()
#     while True:
#         conn, addr = sock.accept()
#         with conn:
#             while True:
#                 data = conn.recv(1024)
#                 if not data:
#                     break
#                 else:
#                     conn.send(50*data)
#                 print(data.decode("utf8"))

class ClientError(Exception):
    pass


class ClientSocketError(ClientError):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class ClientProtocolError(ClientError):
    """Исключение, выбрасываемое клиентом при ошибке протокола"""
    pass



class Client:

    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def put(self, host_metric, value, timestamp=0):
        with socket.create_connection((self.ip, self.port), self.timeout) as sock:
            # set socket read timeout


            try:
                sock.sendall(f"put {host_metric} {value} {timestamp}\n".encode("utf8"))
                data = sock.recv(1024)
            except Exception:
                raise ClientError
            # except socket.timeout:
            #     print("send data timeout")
            # except socket.error as ex:
            #     print("send data error:", ex)

    def get(self, key):
        # metrics = {'palm.cpu': [], 'eardrum.cpu': [], 'test': [], 'load': []}
        metrics = {}
        with socket.create_connection((self.ip, self.port), self.timeout) as sock:
            # set socket read timeout

            try:
                sock.sendall(f'get {key}\n'.encode('utf8'))
                data = sock.recv(1024)
                # logger
                # with open('log', 'w') as f:
                #     f.write(data)
                # print(data)
                print(data)

                if data == b'':
                    raise ClientError
                if data == b'ok\n\n':
                    return {}
                if data[:3] != b'ok\n':
                    raise ClientError

                # print('re',data)
                if re.findall(b'\\n(.+?) (.+?) (\d+)\\n((.+?) (.+?) (\d+)\\n)+\\n', data):
                    # print('re in')
                    # print(data)

                    # data - list of str
                    data = data[3:-2].decode('utf8').split('\n')
                    # print(data)
                    for d in data:
                        d = d.split(' ')
                        if metrics.setdefault(d[0], []):
                            metrics[d[0]].append((int(d[2]), float(d[1])))
                        else:
                            metrics[d[0]].append((int(d[2]), float(d[1])))
                    return metrics
                raise ClientError
            except KeyError:
                raise ClientError


            except Exception:
                raise ClientError  # ClientError


if __name__ == '__main__':
    client = Client("127.0.0.1", 8888, timeout=15)

    # client.put("palm.cpu", 0.5, timestamp=1150864247)
    # client.put("palm.cpu", 2.0, timestamp=1150864248)
    # client.put("palm.cpu", 0.5, timestamp=1150864248)
    #
    # client.put("eardrum.cpu", 3, timestamp=1150864250)
    # client.put("eardrum.cpu", 4, timestamp=1150864251)
    # client.put("eardrum.memory", 4200000)

    print(client.get("*"))
