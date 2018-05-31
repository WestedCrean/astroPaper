from concurrent import futures
import time

import grpc

import api_pb2
import api_pb2_grpc

import astroPaper

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class WallpaperServicer(api_pb2_grpc.AstroPaperServicer):
    wallpaper = ""
    def getWallpaper(self, request, context):
        print("inside getWallpaper() function")
        self.wallpaper = astroPaper.newWallpaper()
        return api_pb2.GetResponse(file='%s' % self.wallpaper)
    def setupWallpaper(self, request, context):
        print("inside setupWallpaper() function")
        astroPaper.wallpaperSetup(astroPaper.getPlatform(), self.wallpaper)
        return api_pb2.SetupResponse(message="Wallpaper %s is set!" % self.wallpaper)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_AstroPaperServicer_to_server(WallpaperServicer(), server)
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