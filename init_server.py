import asyncio, json, socket
from common.socketconnection import SocketConnection
from server.chatclient import ChatClient

clients = set()

async def broadcast_json(data):
  await broadcast(json.dumps(data))

async def broadcast(data):
  for client in clients:
    await client.conn.send(data)

async def handle_data(client, data):
  if data['event'] == 'message':
    await broadcast_json({'type': 'message', 'id': client.id, 'name': client.name, 'message': data['message']})

async def handle_client(reader, writer):
  conn = SocketConnection(reader, writer)
  client = ChatClient(conn)
  await client.handshake()
  print(f'{client.id} ({client.name}) connected')
  try:
    clients.add(client)
    await broadcast_json({'type': 'join', 'id': client.id, 'name': client.name})
    await client.receive_messages(handle_data)
  except:
    pass
  print(f'{client.id} ({client.name}) disconnected')
  clients.remove(client)
  await broadcast_json({'type': 'leave', 'id': client.id, 'name': client.name})
  writer.close()

async def run_server():
  server = await asyncio.start_server(handle_client, 'localhost', 8080)
  async with server:
    await server.serve_forever()

asyncio.run(run_server())
