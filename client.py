import asyncio
from aioconsole import ainput

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

async def receive_messages(reader):
  while True:
    data = await receive(reader)
    print(f'got data: {data}')

async def send_messages(writer):
  while True:
    line  = await ainput()
    await send(writer, line)

async def init_socket(loop):
  reader, writer = await asyncio.open_connection('127.0.0.1', 8080, loop=loop)
  return reader, writer

def main():
  loop = asyncio.get_event_loop()
  reader, writer = loop.run_until_complete(init_socket(loop))
  tasks = [
      receive_messages(reader),
      send_messages(writer),
  ]
  loop.run_until_complete(asyncio.wait(tasks))
  loop.close()
  writer.close()

main()
