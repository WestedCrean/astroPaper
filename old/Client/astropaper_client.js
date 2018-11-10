var messages = require('./apservice_pb');
var services = require('./apservice_grpc_pb');
var EventEmitter = require('events').EventEmitter;
var grpc = require('grpc');


var getWallpaper = function (client, request, q) {
  let e = new EventEmitter();
  process.nextTick(function(){
    request.setQuantity(q);
    e.emit('start');
    client.getNewWallpaper(request, function(err, response) {
      var wallpaper = response.array[0]
      e.emit('end')
      console.log('Wallpaper:', wallpaper)
      });
  });
  return(e);
}

function main() {
  console.log("Client is running");
  var client = new services.AstropaperClient('localhost:50050', grpc.credentials.createInsecure());
  var request = new messages.WallpaperRequest();

  var w = getWallpaper(client, request, 1);
  w.on('start',() => {
    console.log('calling wallpaper')
    // render download bar
  });
  w.on('end', () => {
    console.log('downloaded')
    // destroy download bar
    var setup = new messages.SetupRequest();
    setup.setWallpaper(w);
    client.setupWallpaper(setup, function(err, response) {
      console.log('', w);
    });
  });

    // chained get + setup
    // TODO: make it event driven
    // 
    // ex: 6 calls for new wallpapers
    // on each done => display in app
    // on event 'checked' and 'setup' call setup
}

main();