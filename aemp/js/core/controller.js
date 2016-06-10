core.controller = {
	options: ["building", "owner", "eviction", "fire"],
	show: function(pager) {
		core.controller.nodes.shown.appendChild(pager.node);
		core.controller.map.addMarkers(pager.mdata);
	},
	hide: function(pager) {
		core.controller.nodes.hidden.appendChild(pager.node);
		core.controller.map.clearMarkers(pager.markers);
	},
	init: function() {
		core.controller.nodes = {
			shown: CT.dom.id("dbpanels"),
			hidden: CT.dom.id("dbmin"),
			button: CT.dom.id("qbutton"),
			header: CT.dom.id("header"),
			map: CT.dom.id("map")
		}
		core.controller.map = new CT.map.Map({
			node: core.controller.nodes.map,
			center: { lat: 37.75, lng: -122.45 }
		});
		core.query.init();
	}
};
