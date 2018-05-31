from __future__ import print_function

import grpc

import api_pb2
import api_pb2_grpc

def run():
    print("Client is running")
    channel = grpc.insecure_channel('localhost:50051')
    print("Creating stub")
    stub = api_pb2_grpc.AstroPaperStub(channel)
    print("Stub created, making GET request")
    wallpaper = stub.getWallpaper(api_pb2.Empty())
    print("getWallpaper() response : " + wallpaper.file)

if __name__ == '__main__':
    run()