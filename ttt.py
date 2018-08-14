import re

A = {'palm.cpu': [(1150864247, 0.5), (1150864248, 2.0), (1150864248, 0.5)],
     'eardrum.cpu': [(1150864250, 3.0), (1150864251, 4.0)], 'eardrum.memory': [(0, 4200000.0)]}
# print(A['palm.cpu'])
# print(''.join(f'{i[0]} {i[1]}\n' for i in A['palm.cpu']).encode("utf8"))
data = b'ok\npalm.cpu 0.5 1150864247\n2.0 1150864248\n0.5 1150864248\n0.5 1150864247\n2.0 1150864248\n0.5 1150864248\n\n'
if re.findall(b'\\n(.+?) (.+?) (\d+)\\n((.+?) (.+?))', data):
    print('accept')
