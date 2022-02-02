import asyncio, uuid
from aioconsole import ainput
from common.socketconnection import SocketConnection

id = str(uuid.uuid4())

async def receive_messages(conn):
  while True:
    data = await conn.receive_json()
    print(f'server: {data}')

async def send_messages(conn):
  while True:
    message  = await ainput()
    await conn.send_json({'event': 'message', 'message': message})

async def init_socket():
  reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
  conn = SocketConnection(reader, writer)
  name = await ainput("Enter your name: ")
  await conn.send_json({'id': id, 'name': name})
  return conn

def main():
  loop = asyncio.get_event_loop()
  conn = loop.run_until_complete(init_socket())
  tasks = [
      receive_messages(conn),
      send_messages(conn),
  ]
  loop.run_until_complete(asyncio.wait(tasks))
  loop.close()
  writer.close()

main()
