map.core.model.kinds.Fire = CT.Class({
	CLASSNAME: "map.core.model.kinds.Fire",
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
}, map.core.model.kinds.BReffer);