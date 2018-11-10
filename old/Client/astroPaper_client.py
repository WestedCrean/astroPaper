from __future__ import print_function

import grpc
import re

import apservice_pb2_grpc
import apservice_pb2

def clearReply(reply_string):
    reply_string = str(reply_string)
    reply_string = reply_string[8:]
    reply_string = reply_string[:-2]
    return reply_string

def run():
    print("Client is running")
    channel = grpc.insecure_channel('localhost:50050')
    stub = apservice_pb2_grpc.AstropaperStub(channel)
    print("GET request")
    wallpaper = stub.GetNewWallpaper(apservice_pb2.WallpaperRequest(quantity=1))
    wallpaper = clearReply(wallpaper)
    print("Cleared reply: " + wallpaper )
    #print("Wallpaper : " + str(wallpaper))
    setup_reply = stub.SetupWallpaper(apservice_pb2.SetupRequest(wallpaper=str(wallpaper)))
if __name__ == '__main__':
    run()