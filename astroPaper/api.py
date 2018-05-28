from __future__ import print_function
import astroPaper
import sys
import zerorpc

class Wallpaper:
    wallpaper = ""
    def __init__(self): 
        self.wallpaper = astroPaper.newWallpaper()
    def setup(self):
        astroPaper.wallpaperSetup(astroPaper.getPlatform(), self.wallpaper)

def parse_port():
    return 4242

def main():
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(Wallpaper())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
