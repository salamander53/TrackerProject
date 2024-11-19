import asyncio

async def start_client_a(server_host, server_port):
    reader, writer = await asyncio.open_connection(server_host, server_port)

    # Gửi thông tin Client A
    writer.write(b"A")
    await writer.drain()

    print("Connected to server as Client A.")

    try:
        while True:
            # Nhập tin nhắn để gửi đến Client B
            message = input("Enter message to send to Client B: ")
            writer.write(message.encode())
            await writer.drain()

            # Nhận phản hồi từ Client B
            response = await reader.read(1024)
            print(f"Received from Client B: {response.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()

if __name__ == "__main__":
    asyncio.run(start_client_a('localhost', 5000))