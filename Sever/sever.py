import asyncio

class RelayServer:
    def __init__(self):
        self.clients = {}

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected to {addr}")

        # Nhận dữ liệu từ client
        data = await reader.read(100)
        identifier = data.decode()

        self.clients[identifier] = (reader, writer)

        # Khi cả Client A và Client B đã kết nối
        if len(self.clients) == 2:
            client_a_writer = self.clients.get('A')[1]
            client_b_writer = self.clients.get('B')[1]

            # Thông báo cho Client A rằng nó đã kết nối với Client B
            client_a_writer.write("Connected to Client B. You can start sending messages.\n".encode())
            await client_a_writer.drain()

            # Bắt đầu chuyển tiếp dữ liệu
            await self.forward_messages()

    async def forward_messages(self):
        while True:
            # Chuyển tiếp từ Client A đến Client B
            if 'A' in self.clients:
                client_a_reader = self.clients['A'][0]
                client_b_writer = self.clients['B'][1]

                data = await client_a_reader.read(1024)
                if not data:
                    break
                client_b_writer.write(data)
                await client_b_writer.drain()

            # Chuyển tiếp từ Client B đến Client A
            if 'B' in self.clients:
                client_b_reader = self.clients['B'][0]
                client_a_writer = self.clients['A'][1]

                data = await client_b_reader.read(1024)
                if not data:
                    break
                client_a_writer.write(data)
                await client_a_writer.drain()

    async def start_server(self, host='0.0.0.0', port=5000):
        server = await asyncio.start_server(self.handle_client, host, port)
        async with server:
            print(f'Server listening on {host}:{port}')
            await server.serve_forever()

if __name__ == "__main__":
    relay_server = RelayServer()
    asyncio.run(relay_server.start_server())