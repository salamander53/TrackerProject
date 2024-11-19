import asyncio

async def start_client_b(server_host, server_port):
    reader, writer = await asyncio.open_connection(server_host, server_port)

    # Gửi thông tin Client B
    writer.write(b"B")
    await writer.drain()

    print("Connected to server as Client B.")

    try:
        while True:
            # Nhận dữ liệu từ Client A
            data = await reader.read(1024)
            if not data:
                break
            print(f"Received from Client A: {data.decode()}")

            # Nhập phản hồi để gửi về Client A
            response = input("Enter response to send back to Client A: ")
            writer.write(response.encode())
            await writer.drain()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()

if __name__ == "__main__":
    asyncio.run(start_client_b('localhost', 5000))