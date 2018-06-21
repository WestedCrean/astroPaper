from concurrent import futures
import time

import grpc

import apservice_pb2_grpc
import apservice_pb2

import astropaper as ap

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class WallpaperServicer(apservice_pb2_grpc.AstropaperServicer):
    def __init__(self):
        self.platform = ap.getPlatform()
        self.path = ap.getPath(self.platform)
    def GetNewWallpaper(self, request, context):
        self.wallpaper = ap.newWallpaper(self.path)
        ap.createPreview(self.path + '/' + self.wallpaper)
        print("Path : " + self.path)
        print("Quantity: " + str(request.quantity))
        return apservice_pb2.APIReply(reply=str(self.wallpaper))
    def SetupWallpaper(self, request, context):
        print("Setup request: " + request.wallpaper)
        #print("The request is: " + str(request))
        ap.wallpaperSetup(self.platform, request.wallpaper, self.path)
        return apservice_pb2.APIReply(reply="Wallpaper %s is set!" % request.wallpaper)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apservice_pb2_grpc.add_AstropaperServicer_to_server(WallpaperServicer(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("Server started, entering loop")
    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()