core.model.Pager = CT.Class({
	CLASSNAME: "core.model.Pager",
	mdata: [],
	markers: [],
	setMarkers: function(mlist) {
		this.mdata = mlist;
		this.markers = core.controller.map.addMarkers(mlist);
	},
	get: function(rdata, cb) {
		CT.db.get(this.opts.modelName, this._has_data ? cb : function(d) {
			if (!this._has_data) {
				this._has_data = true;
				CT.log.endTimer("load", this.opts.modelName);
			}
			cb(d);
		}.bind(this), rdata.limit, rdata.offset, this.opts.order, this.opts.filters);
	},
	header: function() {
		var f, fopts, opts = this.opts, label = opts.modelName;
		if (opts.order)
			label += " by " + opts.order;
		var n = CT.dom.node(CT.dom.node(label, "div", "bold"));
		if (opts.filters) {
			for (f in opts.filters) {
				fopts = opts.filters[f];
				val = CT.db.isKey(opts.modelName, f)
					? CT.db.key2label(fopts.value) : fopts.value;
				n.appendChild(CT.dom.node(f + " " + fopts.comparator + " " + val,
					"div", "smaller italic"));
			}
		}
		n.appendChild(CT.dom.node("", "hr"));
		return n;
	},
	toggle: function() {
		if (this.onOff.innerHTML == "-") {
			this.onOff.innerHTML = "+";
			core.controller.hide(this);
		} else {
			this.onOff.innerHTML = "-";
			core.controller.show(this);
		}
	},
	init: function(opts) {
		this.opts = opts;
		this.opts.header = this.opts.header || this.header();
		this.kind = new core.model.kinds[CT.parse.capitalize(this.opts.modelName)](this);
		this.pager = new CT.Pager(this.kind.list, this.get, 10,
			"smaller", this.opts.order, this.opts.filters);
		this.onOff = CT.dom.button("-", this.toggle, "right");
		this.node = CT.dom.node([
			this.onOff,
			CT.dom.node(this.opts.header),
			this.pager.node
		], "div", "qsnode");
		core.controller.show(this);
	}
});
