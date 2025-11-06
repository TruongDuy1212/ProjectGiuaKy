import socket
def v(x): return VALUES.get(x, x)
who = {'you':'You','opponent':'Opponent','draw':'Draw'}[win]
print(f"[RESULT] You={v(you)} Opponent={v(op)} => {who}")
elif t == 'SCORE':
print(f"[SCORE] You={msg.get('you')} Opponent={msg.get('opponent')}")
elif t == 'GAME_OVER':
print(f"[GAME] Result: {msg.get('result').upper()} (type /queue to rematch)")
elif t == 'CHAT':
print(f"[CHAT] {msg.get('from')}: {msg.get('text')}")
elif t == 'ERROR':
print(f"[ERROR] {msg.get('message')}")


def send_queue(self):
send_json(self.sock, {"type":"QUEUE"})


def send_move(self, v):
send_json(self.sock, {"type":"MOVE","value": v})


def send_chat(self, text):
send_json(self.sock, {"type":"CHAT","text": text})


def quit(self):
try:
send_json(self.sock, {"type":"QUIT"})
finally:
self.alive = False
try: self.sock.close()
except: pass




def main():
p = argparse.ArgumentParser()
p.add_argument('--host', default=HOST)
p.add_argument('--port', type=int, default=PORT)
p.add_argument('--name', default='Player')
args = p.parse_args()


c = Client(args.host, args.port, args.name)


thr = threading.Thread(target=c.recv_loop, daemon=True)
thr.start()


print("Commands: /queue | /m r|p|s | /say text | /quit")
try:
while c.alive:
line = sys.stdin.readline()
if not line:
break
line = line.strip()
if not line:
continue
if line == '/queue':
c.send_queue()
elif line.startswith('/m '):
v = line.split(' ',1)[1].strip().lower()
if v not in ('r','p','s'):
print('[!] Move must be r|p|s')
else:
c.send_move(v)
elif line.startswith('/say '):
c.send_chat(line.split(' ',1)[1])
elif line == '/quit':
break
else:
print('[?] Unknown command')
finally:
c.quit()


if __name__ == '__main__':
main()