// renderer.js

// grpc
const messages = require('./apservice_pb');
const services = require('./apservice_grpc_pb');
const grpc = require('grpc');

var client = new services.AstropaperClient('localhost:50050', grpc.credentials.createInsecure());
var request = new messages.WallpaperRequest();

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