if(navigator.mediaDevices===undefined)navigator.mediaDevices={};if(navigator.mediaDevices.getUserMedia===undefined)navigator.mediaDevices.getUserMedia=function(a){var b=(navigator.getUserMedia||navigator.webkitGetUserMedia||navigator.mozGetUserMedia);if(!b)return Promise.reject(new Error('getUserMedia is not implemented in this browser'));return new Promise(function(c,d){b.call(navigator,a,c,d);});};;;