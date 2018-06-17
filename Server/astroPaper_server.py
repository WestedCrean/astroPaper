from concurrent import futures
import time

import grpc

import astropaperservice_pb2
import astropaperservice_pb2_grpc

import astropaper as ap

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class WallpaperServicer(astropaperservice_pb2_grpc.AstroPaperServiceServicer):
    def __init__(self):
        self.platform = ap.getPlatform()
        self.path = ap.getPath()
    def GetNewWallpaper(self, request, context):
        print("inside GetNewWallpaper() function")
        self.wallpaper = ap.newWallpaper(self.path)
        print("Path : " + self.path)
        print("Quantity: " + str(request.quantity))
        return astropaperservice_pb2.APIReply(reply=str(self.wallpaper))
    def SetupWallpaper(self, request, context):
        print("inside SetupWallpaper() function")
        ap.wallpaperSetup(self.platform, request.wallpaper, self.path)
        return astropaperservice_pb2.APIReply(reply="Wallpaper %s is set!" % request.wallpaper)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    astropaperservice_pb2_grpc.add_AstroPaperServiceServicer_to_server(WallpaperServicer(), server)
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