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
    wallpaper = stub.GetNewWallpaper(astropaperservice_pb2.WallpaperRequest(quantity=1))
    print("getWallpaper() : " + str(wallpaper))
    setup_reply = stub.SetupWallpaper(astropaperservice_pb2.SetupRequest(wallpaper=str(wallpaper)))
if __name__ == '__main__':
    run()