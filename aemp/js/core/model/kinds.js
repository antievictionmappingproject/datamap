core.model.kinds.Base = CT.Class({
	CLASSNAME: "core.model.kinds.Base",
	mapify: function(subdata) {
		var that = this;
		return function(bdata) {
			that.setHeader(subdata, bdata);
			that.pager.setMarkers(bdata.map(that.process));
		};
	},
	header: function(subdata) {
		return subdata.label;
	},
	list: function(dlist) {
		var n = CT.dom.node();
		CT.panel.triggerList(dlist, this.markers, n);
		return n;
	},
	markers: function(subdata) {
		this.mapify(subdata)([subdata]);
		core.controller.map.markers[subdata.key].showInfo();
	},
	setHeader: function(subdata, bdata) {
		CT.dom.setContent(core.controller.nodes.header,
			CT.dom.node(this.header(subdata, bdata), "div", "biggest bold"));
	},
	iline: function(d) {
		var process = function(p) {
			if ((typeof p == "string") && (p.slice(0, 4) == "http"))
				return CT.parse.process(p);
			return p || "(none)";
		};
		return function(p) {
			return CT.dom.node([
				CT.dom.node(p + ":", "div", "keycell"),
				CT.dom.node(process(d[p]), "span")
			]);
		};
	},
	process: function(d) {
		return {
			key: d.key,
			position: {
				lng: d.longitude,
				lat: d.latitude
			},
			info: this.info(d),
			icon: this.icon(d)
		}
	},
	info: function(d) {
		var iline = this.iline(d);
		return CT.dom.node([
			CT.dom.node(d.label, "div", "big bold"),
			CT.db.eachProp(d.modelName, iline)
		]);
	},
	icon: function(d) {
		return null; // falls back to map default
	},
	init: function(pager) {
		this.pager = pager;
		this.opts = this.pager.opts;
	}
});

core.model.kinds.Policemurder = CT.Class({
	CLASSNAME: "core.model.kinds.Policemurder",
	icon: function(d) {
		return "/img/murder.png"
	},
}, core.model.kinds.Base);

core.model.kinds.BuildingBase = CT.Class({
	CLASSNAME: "core.model.kinds.BuildingBase",
	process: function(d) {
		return {
			key: d.key,
			address: d.address + ", san francisco",
			position: {
				lng: d.longitude,
				lat: d.latitude
			},
			info: this.info(d),
			icon: this.icon(d)
		};
	},
	info: function(d) {
		return CT.dom.node([
			CT.dom.node(d.address, "div", "big bold"),
			CT.dom.node([
				CT.dom.node("rent_control:", "div", "keycell"),
				CT.dom.node(d.rent_control ? d.rent_control.toString() : "(no value)", "span")
			])
		].concat(["year", "building_type", "building_id"].map(this.iline(d))));
	},
 	_icons: ["ONE FAMILY", "HOUSE", "OFFICE", "BUSINESS", "INDUSTRIAL", "COMMERCIAL", "RESIDENTIAL"],
	icon: function(d) {
		if (d.building_type) {
			for (var i = 0; i < this._icons.length; i++) {
				var icon = this._icons[i];
				if (d.building_type.indexOf(icon) != -1)
					return "/img/" + icon.toLowerCase().replace(" ", "-") + ".png";
			}
		}
	}
}, core.model.kinds.Base);

core.model.kinds.Building = CT.Class({
	CLASSNAME: "core.model.kinds.Building",
}, core.model.kinds.BuildingBase);

core.model.kinds.BReffer = CT.Class({
	CLASSNAME: "core.model.kinds.BReffer",
	process: function(d) {
		var b = CT.data.get(d.building);
		return {
			key: d.key,
			address: b.address + ", san francisco",
			position: {
				lng: b.longitude,
				lat: b.latitude
			},
			icon: this.icon(b),
			info: this.info(d)
		};
	},
	list: function(dlist) {
		var n = CT.dom.node(),
			markers = this.markers;
		CT.db.multi(dlist.map(function(d) {
			return d.building;
		}), function(buildings) {
			buildings.forEach(function(b, i) {
				dlist[i].title = b.address;
			});
			CT.panel.triggerList(dlist, markers, n);
		});
		return n;
	},
	setHeader: function(subdata, bdata) {
		var b = CT.data.get(subdata.building);
		CT.dom.setContent(core.controller.nodes.header,
			CT.dom.node(this.header(b, b), "div", "biggest bold"));
	}
}, core.model.kinds.BuildingBase);

core.model.kinds.Fire = CT.Class({
	CLASSNAME: "core.model.kinds.Fire",
	icon: function(d) {
		return "/img/fire.png";
	},
	info: function(d) {
		var b = CT.data.get(d.building);
		return CT.dom.node([
			CT.dom.node(b.address, "div", "big bold"),
			CT.dom.node(["alarms", "battalion", "persons", "units", "date"].map(this.iline(d))),
			CT.dom.node("", "hr"),
			CT.dom.node([
				CT.dom.node("rent_control:", "div", "keycell"),
				CT.dom.node(b.rent_control ? b.rent_control.toString() : "(no value)", "span")
			].concat(["year", "building_type", "building_id"].map(this.iline(b))))
		]);
	}
}, core.model.kinds.BReffer);

core.model.kinds.Eviction = CT.Class({
	CLASSNAME: "core.model.kinds.Eviction",
	info: function(d) {
		var b = CT.data.get(d.building);
		return CT.dom.node([
			CT.dom.node(b.address, "div", "big bold"),
			CT.dom.node(["petition", "reason", "date"].map(this.iline(d))),
			CT.dom.node("", "hr"),
			CT.dom.node([
				CT.dom.node("rent_control:", "div", "keycell"),
				CT.dom.node(b.rent_control ? b.rent_control.toString() : "(no value)", "span")
			].concat(["year", "building_type", "building_id"].map(this.iline(b))))
		]);
	}
}, core.model.kinds.BReffer);

core.model.kinds.Owner = CT.Class({
	CLASSNAME: "core.model.kinds.Owner",
	header: function(subdata, bdata) {
		return subdata.name + ": " + bdata.length + " properties";
	},
	markers: function(subdata) {
		if (this.opts.order && this.opts.order.indexOf(".") != -1) {
			var ro = this.opts.order,
				ord = (ro.charAt(0) == "-") ? ro.slice(1) : ro,
				sord = ord.split("."),
				target = sord[0],
				property = sord[1],
				filters = this.opts.filters || {};
			if (sord.length == 3) {
				filters[sord[2]] = { comparator: "==", value: subdata.key };
				CT.db.get(property, this.mapify(subdata), 1000, 0, target + "." + property, filters);
			} else {
				filters[property] = { comparator: "==", value: subdata.key };
				CT.db.get(target, this.mapify(subdata), 1000, 0, null, filters);
			}
		} else
			CT.db.get(this.opts.modelName, this.mapify(subdata),
				1000, 0, this.opts.order, this.opts.filters);
	}
}, core.model.kinds.BuildingBase);