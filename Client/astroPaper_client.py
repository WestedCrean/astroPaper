from __future__ import print_function

import grpc
import re

import astropaperservice_pb2
import astropaperservice_pb2_grpc

def clearReply(reply_string):
    reply_string = str(reply_string)
    reply_string = reply_string[8:]
    reply_string = reply_string[:-2]
    return reply_string

def run():
    print("Client is running")
    channel = grpc.insecure_channel('localhost:50050')
    stub = astropaperservice_pb2_grpc.AstroPaperServiceStub(channel)
    print("GET request")
    wallpaper = stub.GetNewWallpaper(astropaperservice_pb2.WallpaperRequest(quantity=1))
    wallpaper = clearReply(wallpaper)
    print("Cleared reply: " + wallpaper )
    #print("Wallpaper : " + str(wallpaper))
    setup_reply = stub.SetupWallpaper(astropaperservice_pb2.SetupRequest(wallpaper=str(wallpaper)))
if __name__ == '__main__':
    run()