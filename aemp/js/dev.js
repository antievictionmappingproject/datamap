CT.require("CT.all");
CT.require("CT.map");

CT.onload(function() {
	CT.dom.id("build").onclick = function() {
		CT.log("scraping buildings");
		CT.net.post("/scrape", { "scraper": "buildings" },
			"error scraping buildings", function(d) {
				CT.log("scraping rent-control");
				CT.net.post("/scrape", { "scraper": "rent_control" },
					"error scraping rent control", function(d) {
						CT.log("scraping lords");
						CT.net.post("/scrape", { "scraper": "lords" },
							"error scraping rent control", function(d) {
								CT.log("done!"); // TODO: fires
							});

					});
			});
	};

	CT.dom.id("fetch").onclick = function() {
		CT.log("fetching owners");
		CT.net.post("/get", { "model": "owner" },
			"error loading owners", function(owners) {
				CT.log("got " + owners.length + " owners");
				var o = [];
				owners.forEach(function(p) {
					o.push(p.name);
				});
				CT.log("loading owners");
				CT.panel.load(o);
				CT.log("owners loaded");
			});
	};

	CT.dom.id("test").onclick = function() {
		CT.net.post("/test", {}, "error performing test", function(d) {
			CT.dom.id("data").appendChild(CT.dom.node(JSON.stringify(d)));
		});
	};

	var mkeys = {};
	var getPage = function(mod, offset) {
		CT.log("loading " + mod + " with offset " + offset);
		CT.net.post("/get", { "model": mod, "offset": offset },
			"error retrieving " +  mod + " records", function(d) {
				CT.log("got " + d.length + " " + mod + " records");
				d.forEach(function(item) {
					if (item.key in mkeys)
						CT.log("REPEAT: " + item.key);
					else
						mkeys[item.key] = item;
				});
			});
	};

	CT.dom.id("reqtest").onclick = function() {
		var mods = ["building", "parcel", "owner", "zipcode", "propertyvalue", "fire"];
		var max_off = 100;
		var off_inc = 20;
		CT.log("testing hecka (" + mods.length * (1 + (max_off / off_inc)) + ") rapid consecutive requests");
		for (var offset = 0; offset <= max_off; offset += off_inc) {
			mods.forEach(function(mod, i) {
				getPage(mod, offset);
			});

		}
	};

	var map = CT.dom.id("map");
	CT.dom.id("mapup").onclick = function() {
		CT.dom.showHide(map);
	};

	CT.map.Map({ node: map, center: { lat: 37.75, lng: -122.45 }});
});