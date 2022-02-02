import asyncio, json

class SocketConnection:
  def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    self.reader = reader
    self.writer = writer

  async def send_json(self, data):
    await self.send(json.dumps(data))

  async def receive_json(self):
    data = await self.receive()
    return json.loads(data)

  async def send(self, data):
    encoded = data.encode('utf8')
    self.writer.write(len(encoded).to_bytes(4, 'big'))
    self.writer.write(encoded)
    await self.writer.drain()

  async def receive(self):
    length_bytes = await self.reader.read(4)
    length = int.from_bytes(length_bytes, "big")
    data = (await self.reader.read(length)).decode('utf8')
    return data
