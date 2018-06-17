var PROTO_PATH = __dirname + '/../Proto/astropaperservice.proto';

var grpc = require('grpc');

var  astropaper_proto = grpc.load(PROTO_PATH).astropaperservice;
console.log(astropaper_proto);

function main() {
  console.log("Client is running")
  var client = new astropaper_proto.AstroPaperService('localhost:50050',
                                       grpc.credentials.createInsecure());
  client.GetNewWallpaper({quantity: 1}, function(err, response) {
    var wallpaperName = response.reply.slice(8,response.reply.length - 2);
    console.log('Wallpaper: ', wallpaperName);
  });
}

main();