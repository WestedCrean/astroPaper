// renderer.js

//communication with main.js
const {ipcRenderer} = require('electron')

document.getElementById("roll").addEventListener("click", () => {
  ipcRenderer.send('asynchronous-message', 'roll clicked')
});

document.getElementById('setup').addEventListener('click', () => {
  ipcRenderer.send('asynchronous-message', 'setup clicked')
});

ipcRenderer.on('asynchronous-reply', (event, arg) => {
  console.log(arg) 
});
