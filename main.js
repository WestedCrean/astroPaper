// main.js

const electron = require('electron')
const {ipcMain} = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

// settting up the app

let mainWindow = null
const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1000, height: 600});
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

// communication with renderer.js
/*
ipcMain.on('asynchronous-message', (event, arg) => {
  console.log(arg) // prints "ping"
  event.sender.send('asynchronous-reply', 'Main.js : ' + arg)
});

ipcMain.on('synchronous-message', (event, arg) => {
  console.log(arg) // prints "ping"
  event.returnValue = 'Main.js : ' + arg
});*/

ipcMain.on('asynchronous-message', (event, arg) => {
    console.log(arg) // prints "ping"
    event.sender.send('asynchronous-reply', 'main.js : asynchronous reply : ')
  })
  
  ipcMain.on('synchronous-message', (event, arg) => {
    console.log(arg) // prints "ping"
    event.returnValue = 'main.js : synchronous reply : pong'
  })



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


app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)
