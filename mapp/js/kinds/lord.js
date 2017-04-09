map.core.model.kinds.Owner = CT.Class({
	CLASSNAME: "map.core.model.kinds.Owner",
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
}, map.core.model.kinds.BuildingBase);