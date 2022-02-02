import asyncio, json
from common.socketconnection import SocketConnection

class ChatClient:
  def __init__(self, connection: SocketConnection):
    self.conn = connection

  async def handshake(self):
    data = await self.conn.receive_json()
    self.id = data['id']
    self.name = data['name']

  async def receive_messages(self, callback):
    while True:
      request = await self.conn.receive_json()
      await callback(self, request)
