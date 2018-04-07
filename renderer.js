// renderer.js

const zerorpc = require("zerorpc");
let client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

let roll = document.querySelector('#roll');
let setup = document.querySelector('#setup');
/*
let wallpaper = "";
roll.addEventListener('click', () => {
  client.invoke("roll", formula.value, (error, res) => {
    if(error) {
      console.error(error)
    } else {
      wallpaper = result.textContent;
    }
  })
});

setup.addEventListener('click', () => {
    client.invoke("setup", formula.value, (error, res) => {
      if(error) {
        console.error(error)
      }
    })
  });

*/
roll.dispatchEvent(new Event('click'));