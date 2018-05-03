from __future__ import print_function
import astroPaper

import sys
import zerorpc
import platform

import tkinter as tk


current_system = platform.system()
print("Current system: ", current_system)
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("Current screen's width: " + str(screen_width) + " Current screen's height: " + str(screen_height))

class AstroPaperApi(object):
    currentWallpaperpath = ""
    def roll(self):
        """Download a random wallpaper from apod.nasa.gov"""
        try:
            print("main routine - api.py")
            validFileFound = False
            downloadSuccess = False
            while(not downloadSuccess):
                while(not validFileFound):
                    check = astroPaper.rollAWallpaper()
                    validFileFound = True
                url = check
                astroPaper.downloadImage(url)
                downloadSuccess = True
            filename = url.split('/')[-1]
            self.currentWallpaperpath = "/code/astroPaper/astroPaper/"+filename
            self.hasWallpaper = True
            return filename
        except Exception as e:
            print(e)
    def setup(self):
        try:
            """Set up the latest downloaded wallpaper """
            current_system = platform.system()
            print("API.PY: currentWallpaperpath: {}".format(self.currentWallpaperpath))
            astroPaper.wallpaperSetup(current_system, self.currentWallpaperpath)
        except AttributeError:
            print("Download a wallpaper first")
    def display(self, image):
        """Show downloaded wallpaper"""
        pass

def parse_port():
    return 4242

def main():
    addr = 'tcp://127.0.0.1:' + str(parse_port())
    s = zerorpc.Server(AstroPaperApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
