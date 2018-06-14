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
        self.wallpaper = ''
        self.path = ''

    def GetNewWallpaper(self, request, context):
        print("inside GetNewWallpaper() function")
        self.wallpaper = ap.downloadImage("https://apod.nasa.gov/apod/image/1707/MOSAIC_IC1396_HaSHO_blanco.jpg")
        self.path = ap.getPath(self.wallpaper)
        print("Path : " + self.path)
        return astropaperservice_pb2.APIReply(reply="%s" % self.wallpaper)
    def SetupWallpaper(self, request, context):
        print("inside SetupWallpaper() function")
        ap.wallpaperSetup(self.platform, self.wallpaper, self.path)
        return astropaperservice_pb2.APIReply(reply="Wallpaper %s is set!" % self.wallpaper)

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