import asyncio

from django.views.static import serve
from tensorflow.python.ops.gen_io_ops import reader_read


class ClientConnectionHandler:

    def __init__(self,reader, writer):

        self.reader = reader
        self.writer = writer

        self.addr = writer.get_extra_info('peername')


    async def handle(self):

        try:
            await self.read_loop()
        except Exception as e:
            print(f"{self.addr}에서 처리되지 않은 에러 발생 {e}")

    async def read_loop(self):
        image_data = b""
        total_bytes = 0
        print("read loop=========================")
        while True:
            try:
                packet = await self.reader.read(4096)

                if not packet:
                    break
                image_data+=packet
                total_bytes+=len(packet)
            except ConnectionResetError:
                print(f"{self.addr}와의 연결이 끊어졌습니다.")
                break


        print("이미지22222222222222222222222222",total_bytes)

        #AI작업으로 처리해야함
        if image_data:
            with open('received_image.jpg', 'wb') as f:
                f.write(image_data)
                print("이미지 잘 받았음")


async  def client_connected_callback(reader, writer):

            handler = ClientConnectionHandler(reader,writer)
            await handler.handle()



class Server:

    def __init__(self,host:str='127.0.0.1',port:int=7777):
        self.host = host
        self.port = port


    async def run(self):

        server = await asyncio.start_server(client_connected_callback, host=self.host, port = self.port)
        addrs=','.join(str(sock.getsockname())for sock in server.sockets)
        print(f"서버 실행중 : {addrs}")

        async with server:
            await server.serve_forever()



if __name__=='__main__':

    server= Server()
    asyncio.run(server.run())
