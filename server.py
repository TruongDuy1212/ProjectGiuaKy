import socket
except Exception:
send_json(conn, {"type":"ERROR","message":"Invalid JSON"})
continue
t = msg.get('type')
if t == 'LOGIN':
name = (msg.get('name') or 'Player')[:20]
with clients_lock:
clients[conn] = {'name': name, 'room': None}
send_json(conn, {"type":"WELCOME","message":f"Hello {name}! Use QUEUE to match."})
elif t == 'QUEUE':
if conn not in clients:
send_json(conn, {"type":"ERROR","message":"LOGIN first"})
continue
try_queue(conn)
elif t == 'MOVE':
r = clients.get(conn, {}).get('room')
if not r:
send_json(conn, {"type":"ERROR","message":"Not in a room. Use QUEUE"})
else:
r.handle_move(conn, (msg.get('value') or '').lower())
elif t == 'CHAT':
r = clients.get(conn, {}).get('room')
if r:
r.handle_chat(conn, msg.get('text','')[:200])
elif t == 'QUIT':
return
else:
send_json(conn, {"type":"ERROR","message":"Unknown type"})
finally:
# cleanup
with clients_lock:
room = clients.get(conn, {}).get('room') if conn in clients else None
if conn in clients:
del clients[conn]
try:
conn.close()
except Exception:
pass
# nếu rời giữa trận, trả đối thủ về hàng chờ
if isinstance(room, GameRoom):
try:
other = room.opponent_of(conn)
if other:
send_json(other, {"type":"ERROR","message":"Opponent left. Returning to queue."})
try_queue(other)
except Exception:
pass




def main():
print(f"[SERVER] Listening on {HOST}:{PORT}")
with socket.create_server((HOST, PORT), reuse_port=False) as srv:
srv.listen()
while True:
conn, addr = srv.accept()
t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
t.start()


if __name__ == '__main__':
main()