import asyncio
import base64

import aiofiles
import struct
import json
import os
import cv2
import numpy as np
from django.template.context_processors import media

from config.settings.base import MEDIA_ROOT
from django.http import JsonResponse
from django.urls import reverse



REQUEST_IMAGE_1 = 100
REQUEST_IMAGE_2 = 101
REQUEST_AI_ANALYSIS = 200
RESPONSE_AI_ANALYSIS = 210
READY_AI_ANALYSIS  = 220

request_ai_ready = "REQ_AI_READY"
request_ai_ready_ok = 'REQ_AI_READY_OK'
request_ai_analysis_image = 'REQ_AI_IMAGE'
request_ai_analysis_image_ok = 'REQ_AI_IMAGE_OK'
from pathlib import Path

class Client:


    bErrorResult = True

    def __init__(self, img_path,host:str='52.78.102.210', port:int=7777):
        self.host = host
        self.port = port
        self.name = "" # chat program
        self.reader = None
        self.writer = None
        self.img_path = img_path
        self.answer_img_path =""
    async def connect(self):

        print("host ",self.host)

        try:
            reader ,writer = await asyncio.open_connection(self.host, self.port)
            self.reader = reader
            self.writer = writer
            print(f"서버에 연결됨: {self.host}: {self.port}")
        except Exception as e:
            print(f"서버에 연결 실패 {e}")
            self.bErrorResult = False

        return self.bErrorResult




    async def sendImage(self,image_path):

        try:
            async with aiofiles.open(image_path,'rb') as f:
                image_data = await f.read()
                self.writer.write(image_data)
                print(f'전송된 이미지 데이터의 크기: {len(image_data)} 바이트')
                await self.writer.drain()

        except Exception as e:
            print(f"이미지 전송중 에러 {e}")
            self.bErrorResult = True
            #처리된 이미지를 받아서 저장하기
            #response = await self.reader.read(4096)

    async def sendImage_toJson(self, image_path):
        try:
            async with aiofiles.open(image_path,'rb') as f:
                image_data = await f.read()
                #encoded_Image = base64.b64encode(image_data).decode()
                await self.protocol_send_data_json(request_ai_analysis_image,image_data,True)
                print(f'전송된 이미지 데이터의 크기: {len(image_data)} 바이트')

        except Exception as e:
            print(f"이미지 전송중 에러 {e}")
            self.bErrorResult = True
            #처리된 이미지를 받아서 저장하기
            #response = await self.reader.read(4096)


    async def close_connection(self):
        if self.writer:
            self.bErrorResult = False
            self.writer.close()
            await self.writer.wait_closed()

    async def write_loop(self):

        loop = asyncio.get_running_loop()

    async def protocol_send_data(self, protocol):
        #protocol을 붙이고 뒤에 데이타 보내기

        print("protocol  :==================", protocol)
        data_protocol = struct.pack('>I', protocol)  # Big-endian 형식으로 변환
        #data_protocol+=data
        if self.writer:
            self.writer.write(data_protocol)
            await self.writer.drain()

    async def protocol_send_data_json(self, protocol, data, isImage=False):

        if isImage == False:
            response = {"protocol": protocol, "message": data}
        else:
            response = {"protocol": protocol,"image_size":len(data)}

        try:
            self.writer.write((json.dumps(response)+'\n').encode())
            await self.writer.drain()
            print("protocol  json:==================", protocol)
        except Exception as e:
            print("Error send data json ============")
            self.bErrorResult = True

        if(isImage==True):
            self.writer.write(data)
            await  self.writer.drain()
            print("image data sent")


    async def read_data_json(self):
        try:
            print("read_data result==============")
            response = await asyncio.wait_for(self.reader.readline(), timeout=30.0)
            message = json.loads(response.decode())
            if message['protocol'] == request_ai_analysis_image_ok:
                img_size = message['image_size']
                print("결과 값 받기 OK image_size", img_size)

                image_data = b""
                while len(image_data) < img_size:
                    chunk = await self.reader.read(img_size - len(image_data))
                    if not chunk:
                        break
                    image_data += chunk
                if image_data :
                    base_dir = Path(__file__).resolve().parent.parent
                    media_root = os.path.join(base_dir,'media','')
                    print("base dir", base_dir, "media_root", media_root)
                    django_path = os.path.join(
                        media_root,
                        'ai\\answer_image',
                        os.path.basename(self.img_path)
                    )

                    print("django path ", django_path)
                    self.answer_img_path = os.path.join('ai\\answer_image',
                        os.path.basename(self.img_path))

                    try:
                        with open(django_path, 'wb') as out_file:
                            out_file.write(image_data)
                            print("image_data saved",self.img_path,"django", django_path)

                    except Exception as e:
                        print("error saved file",e)




        except Exception as e:
            print("read_data Error ===========" ,e)
            self.bErrorResult = True


    def get_answer_path(self):
        return self.answer_img_path
    async def send_data(self):

            await self.protocol_send_data_json(request_ai_ready,"")

            #응답기다리기
            # 처리된 이미지를 받아서 저장하기

            try:
                response = await asyncio.wait_for(self.reader.readline(),timeout=30.0)
                # protocol_id = int.from_bytes(response[:4], 'big')  # big endian
                # data = int.from_bytes(response[4:], 'little')
                # print("서버 응답 ", protocol_id, 'data', data)
                message = json.loads(response.decode())
                print("received json  message", message)

                if (message['protocol']==request_ai_ready_ok):
                    await self.sendImage_toJson(self.img_path)
                    await self.read_data_json()
                    print("이미지 전송하자")
                elif message['protocol']==request_ai_analysis_image_ok :
                    print("결과 값 받기 OK===================")

            except asyncio.TimeoutError:
                print("응답대기중 timeout ")
                self.bErrorResult = True
            except Exception as e:
                print("에러발생 ",e)
                self.bErrorResult = True



            #print("서버 응답 ", response)


    async def read_data(self):

            response = await self.reader.read(4096)

            protocol_id = int.from_bytes(response[:4], 'big')  # big endian
            data = int.from_bytes(response[4:],'little')
            print("서버 응답 ", protocol_id, 'data', data)



    async def run(self):

        try:
            conn_result = await  self.connect()

            if conn_result :
                await self.send_data()
            else:
                self.bErrorResult = True

        except Exception as e:
            print("error 발생:",e)
            self.bErrorResult = True
        finally:
            await self.close_connection()

        return self.bErrorResult





if __name__=="__main__":


    client = Client()
    asyncio.run(client.run())
