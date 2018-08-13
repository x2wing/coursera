import socket
ip = ''
port = 8888
with socket.create_connection((ip, port)) as sock:
    # set socket read timeout

    # try:
    sock.sendall(b'fdgdfgdfgfdg')
    data = sock.recv(1024)
    print(data)

    # except Exception:
    #     print("")