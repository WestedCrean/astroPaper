from __future__ import print_function

import grpc

import astropaperservice_pb2
import astropaperservice_pb2_grpc

def run():
    print("Client is running")
    channel = grpc.insecure_channel('localhost:50050')
    print("Creating stub")
    stub = astropaperservice_pb2_grpc.AstroPaperServiceStub(channel)
    print("Stub created, making GET request")
    wallpaper = stub.GetNewWallpaper(astropaperservice_pb2.APIRequest(name='you'))
    print("getWallpaper() : " + str(wallpaper))
    setup = stub.SetupWallpaper(astropaperservice_pb2.APIRequest(name=str(wallpaper)))
if __name__ == '__main__':
    run()