import json


def send_json(sock, obj):
data = json.dumps(obj, ensure_ascii=False) + "\n"
sock.sendall(data.encode('utf-8'))


class LineBuffer:
def __init__(self):
self.buf = b""
def feed(self, data: bytes):
self.buf += data
lines = self.buf.split(b"\n")
self.buf = lines[-1]
for line in lines[:-1]:
if line.strip():
yield line.decode('utf-8', errors='ignore')


# RPS logic helpers
R, P, S = 'r', 'p', 's'
VALUES = {R: 'Rock', P: 'Paper', S: 'Scissors'}


def judge(a, b):
"""return 'a' if a wins, 'b' if b wins, 'draw' otherwise"""
if a == b:
return 'draw'
wins = {(R, S), (S, P), (P, R)}
return 'a' if (a, b) in wins else 'b'