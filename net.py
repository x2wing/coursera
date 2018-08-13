# import socket
#
# host, port = ('', 12000)
# sock = socket.create_connection((host, port), 5)
# sock.listen(1)

# создание сокета, контекстный менеджер
# сервер
import socket

with socket.socket() as sock:
    sock.bind(('', 9090))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if 'a' in data.decode("utf8"):
                    conn.send(b'hello, world!')
                if not data:
                    break
                print(data.upper())


#
# import socket
#
# sock = socket.socket()
# sock.bind(('', 9090))
# sock.listen(1)
# conn, addr = sock.accept()
#
# print('connected:', addr)
#
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data.upper())
#
# conn.close()