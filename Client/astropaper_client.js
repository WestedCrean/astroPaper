var messages = require('./apservice_pb');
var services = require('./apservice_grpc_pb');
var EventEmitter = require('events').EventEmitter;
var grpc = require('grpc');

function main() {
  console.log("Client is running");
  var client = new services.AstropaperClient('localhost:50050',
                                       grpc.credentials.createInsecure());
  var request = new messages.WallpaperRequest();
  
  var quantity;
  if (process.argv.length >= 3) {
    quantity = process.argv[2];
  } else {
    quantity = 1;
  }

  request.setQuantity(quantity);
  client.getNewWallpaper(request, function(err, response) {
    console.log('Wallpaper:', response.array[0]);
    var wallpaper = response.array[0];
    // chained get + setup
    // TODO: make it event driven
    // 
    // ex: 6 calls for new wallpapers
    // on each done => display in app
    // on event 'checked' and 'setup' call setup
    var setup = new messages.SetupRequest();
    setup.setWallpaper(wallpaper);
    client.setupWallpaper(setup, function(err, response) {
      console.log('', wallpaper);
    });
  });
}

main();