CT.require("CT.all");
CT.require("CT.map");
CT.require("core.all");
CT.map.util.setGeoKeys([
	"AIzaSyCgnoy4AYjX5qblebjf8HASGyHhnCZYMkQ",
	"AIzaSyDW-yuqN1MeX06PDburFj76rf6LhUoSuOc"]);
CT.net.setCache(true);
CT.net.setSpinner(true);
CT.map.useSingleInfoWindow();

CT.onload(function() {
	CT.log.startTimer("load");
	core.controller.init();
	CT.dom.id("clearcache").onclick = CT.storage.clear;
	CT.dom.id("clearmap").onclick = core.controller.map.clearMarkers;
});