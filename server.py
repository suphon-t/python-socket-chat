import asyncio, json, socket

clients = set()

async def send(writer, data):
  encoded = data.encode('utf8')
  writer.write(len(encoded).to_bytes(4, 'big'))
  writer.write(encoded)
  await writer.drain()

async def receive(reader):
  length_bytes = await reader.read(4)
  length = int.from_bytes(length_bytes, "big")
  data = (await reader.read(length)).decode('utf8')
  return data

async def broadcast(data):
  for writer in clients:
    await send(writer, data)

async def handle_client(reader, writer):
  print('connected')
  clients.add(writer)
  try:
    request = None
    while request != 'quit':
      request = await receive(reader)
      response = str(f"from client: {request}")
      await broadcast(response)
  except:
    print('disconnected')
  clients.remove(writer)
  writer.close()

async def run_server():
  server = await asyncio.start_server(handle_client, 'localhost', 8080)
  async with server:
    await server.serve_forever()

asyncio.run(run_server())
