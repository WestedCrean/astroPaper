// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var apservice_pb = require('./apservice_pb.js');

function serialize_astropaperpackage_APIReply(arg) {
  if (!(arg instanceof apservice_pb.APIReply)) {
    throw new Error('Expected argument of type astropaperpackage.APIReply');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_astropaperpackage_APIReply(buffer_arg) {
  return apservice_pb.APIReply.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_astropaperpackage_SetupRequest(arg) {
  if (!(arg instanceof apservice_pb.SetupRequest)) {
    throw new Error('Expected argument of type astropaperpackage.SetupRequest');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_astropaperpackage_SetupRequest(buffer_arg) {
  return apservice_pb.SetupRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_astropaperpackage_WallpaperRequest(arg) {
  if (!(arg instanceof apservice_pb.WallpaperRequest)) {
    throw new Error('Expected argument of type astropaperpackage.WallpaperRequest');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_astropaperpackage_WallpaperRequest(buffer_arg) {
  return apservice_pb.WallpaperRequest.deserializeBinary(new Uint8Array(buffer_arg));
}


// The api service definition.
var AstropaperService = exports.AstropaperService = {
  getNewWallpaper: {
    path: '/astropaperpackage.Astropaper/GetNewWallpaper',
    requestStream: false,
    responseStream: false,
    requestType: apservice_pb.WallpaperRequest,
    responseType: apservice_pb.APIReply,
    requestSerialize: serialize_astropaperpackage_WallpaperRequest,
    requestDeserialize: deserialize_astropaperpackage_WallpaperRequest,
    responseSerialize: serialize_astropaperpackage_APIReply,
    responseDeserialize: deserialize_astropaperpackage_APIReply,
  },
  setupWallpaper: {
    path: '/astropaperpackage.Astropaper/SetupWallpaper',
    requestStream: false,
    responseStream: false,
    requestType: apservice_pb.SetupRequest,
    responseType: apservice_pb.APIReply,
    requestSerialize: serialize_astropaperpackage_SetupRequest,
    requestDeserialize: deserialize_astropaperpackage_SetupRequest,
    responseSerialize: serialize_astropaperpackage_APIReply,
    responseDeserialize: deserialize_astropaperpackage_APIReply,
  },
};

exports.AstropaperClient = grpc.makeGenericClientConstructor(AstropaperService);
