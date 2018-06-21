// renderer.js

//communication with main.js
const {ipcRenderer} = require('electron')

document.getElementById("roll").addEventListener("click", () => {
  console.log(ipcRenderer.sendSync('synchronous-message','renderer.js : roll clicked'))
});

document.getElementById('setup').addEventListener('click', () => {
  ipcRenderer.send('asynchronous-message', 'renderer.js : setup clicked')
});

ipcRenderer.on('asynchronous-reply', (event, arg) => {
  console.log(arg) // prints "pong"
});
