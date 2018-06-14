import os
import re
import requests
import sys

def downloadImage(url):
    file_name = url.split('/')[-1]
    file_name
    r = requests.get(url, stream=True)
    size = r.headers.get('Content-Length')
    size = int(size)
    os.path.abspath(__file__)
    path = os.path.abspath(__file__)
    path = re.sub(__file__, '', path)


    with open(path + '/' + file_name, 'wb') as file:
        download = 0
        for chunk in r.iter_content(256):
            download += len(chunk)
            file.write(chunk)
            sys.stdout.write("Done: %d / %d bytes\r" % (download, size))
            sys.stdout.flush()
    return file_name

url = "https://apod.nasa.gov/apod/image/1707/MOSAIC_IC1396_HaSHO_blanco.jpg"

downloadImage(url)