core.query = {
	sample: {
		lords: function() {
			core.query._build({
				modelName: "owner",
				order: "-building.owner"
			});
		},
		homes: function() {
			core.query._build({
				modelName: "building",
				order: "-parcel.building"
			});
		},
		evictions: function() {
			core.query._build({
				modelName: "building",
				order: "-eviction.building"
			});
		},
		fires: function() {
			core.query._build({
				modelName: "fire",
				order: "-persons"
			});
		},
		murders: function() {
			core.query._build({
				modelName: "policemurder"
			});
		},
	},
	_build: function(opts) {
		new core.model.Pager(opts);
	},
	_setup: function(schema) {
		core.query.modal = new CT.modal.Prompt({
			transition: "fade",
			style: "single-choice",
			cb: function(index) {
				CT.db.query({
					modelName: core.controller.options[index],
					submit: core.query._build,
					startYear: 2005,
					showHelp: true
				}, "slide");
			},
			data: core.controller.options.map(function(d) {
				return CT.dom.node(d);
			})
		});
		core.controller.nodes.button.onclick = function() {
			core.query.modal.showHide();
		};
		for (var sample in core.query.sample)
			core.query.sample[sample]();
	},
	init: function() {
		CT.db.init({ cb: core.query._setup });
	}
};