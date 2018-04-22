// renderer.js

const zerorpc = require("zerorpc");
let client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");
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

const exec = require('child_process').exec;
const serverCall = 'zerorpc tcp://127.0.0.1:4242 ';
let rollButton = document.getElementById('roll');
let setupButton = document.getElementById('setup');
rollButton.addEventListener = ('click', () => {
	exec(String.join(serverCall,'roll'), (error, stdout, stderr) => {
            console.log(`${stdout}`);
            console.log(`${stderr}`);
            if (error !== null) {
                console.log(`exec error: ${error}`);
            }})});
setupButton.addEventListener = ('click', () => {
  client.invoke("roll", (error,res) => {
    if(error) {
      console.error(error)
    }
  })
});
rollButton.dispatchEvent(new Event('click'));
setupButton.dispatchEvent(new Event('click'));