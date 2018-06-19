# 🚀💫🌔 astroPaper

AstroPaper is a Electron.js + Python app, serving you random wallpapers of your choice

![](https://i.imgur.com/s9DvJ2d.gif)

Currently it's downloading random astrophotography wallpapers from NASA's Astronomy Picture of The Day (http://apod.nasa.gov/)
but in the future users will be able to specify topics of interest and app will do the rest

If you want to use it as a console application - download astropaper.py from 'Server' folder and run
```
pipenv install
```
then
```
cd Server
pipenv shell
python astropaper.py
```

Feel free to fork it, tweak it and send a pull request! I plan to move from astrophotography to other pictures also, to let a user choose his/her own wallpaper genre.

## ☑ ROADMAP

- [X] python backend (finally bulletproof)
- [X] prototype frontend
- [X] make Electron.js work
- [X] add zerorpc
- [X] move from zerorpc to grpc
- [ ] connect node client with Electron frontend
- [ ] add favourites button?
- [ ] React app serving images to Electron
<br/>   .
<br/>   .
<br/>   .
- [ ] release ?
