// main.js

const electron = require('electron')
const {ipcMain} = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

var messages = require('./Client/apservice_pb');
var services = require('./Client/apservice_grpc_pb');
var EventEmitter = require('events').EventEmitter;
const grpc = require('grpc');

// settting up the app

let mainWindow = null
const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1100, height: 600});
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }));
  
  mainWindow.on('closed', () => {
    mainWindow = null
  });
}
app.on('ready', createWindow);
app.on('window-all-closed', () => {
    app.quit()
});
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
});

// grpc connection
let client = new services.AstropaperClient('localhost:50050', grpc.credentials.createInsecure());
let request = new messages.WallpaperRequest();
// Python Backend

let pyProc = null
let pyPort = null

const selectPort = () => {
  pyPort = 4242
  return pyPort
}

const createPyProc = () => {
  let port = '' + selectPort()
  let script = path.join(__dirname, 'Server', 'astropaper_server.py')
  pyProc = require('child_process').spawn('python', [script, port])
  if (pyProc != null) {
    console.log('child process success')
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

// communication with renderer.js

ipcMain.on('asynchronous-message', (event, arg) => {
  // setup
  console.log(arg)
  if(arg == 'roll clicked'){
    request.setQuantity(1);
    client.getNewWallpaper(request, function(err, response) {
      this.w = response.array[0]
    console.log('Wallpaper:', this.w)
    });
    event.sender.send('asynchronous-reply', 'main.js : asynchronous reply roll ')
  }else{
    event.sender.send('asynchronous-reply', 'main.js : asynchronous reply setup ')
  }
})

ipcMain.on('synchronous-message', (event, arg) => {
  // roll
  //let setup = new messages.SetupRequest();
  console.log(arg)
  event.returnValue = arg; //'main.js : setup'
})



app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)
