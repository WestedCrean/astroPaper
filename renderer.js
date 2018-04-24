// renderer.js

const zerorpc = require("zerorpc");
let client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

var wow = () => {
  console.log("Listening for clicks");
};

wow();
document.getElementById("roll").addEventListener("click", () => {
  console.log("roll clicked");
  client.invoke("roll", function(error, res, more) {
    if(error) {
        console.error(error);
    } else {
        console.log("UPDATE:", res);
    }

    if(!more) {
        console.log("Done.");
    }
  })
});

document.getElementById('setup').addEventListener('click', () => {
  console.log("setup clicked");
  client.invoke("setup", function(error, res, more) {
    if(error) {
        console.error(error);
    } else {
        console.log("UPDATE:", res);
    }

    if(!more) {
        console.log("Done.");
    }
  })
});