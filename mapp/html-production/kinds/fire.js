map.core.model.kinds.Fire=CT.Class({CLASSNAME:"map.core.model.kinds.Fire",icon:function(a){return "/img/fire.png";},info:function(a){var b=CT.data.get(a.building);return CT.dom.node([CT.dom.node(b.address,"div","big bold"),CT.dom.node(["alarms","battalion","persons","units","date"].map(this.iline(a))),CT.dom.node("","hr"),CT.dom.node([CT.dom.node("rent_control:","div","keycell"),CT.dom.node(b.rent_control?b.rent_control.toString():"(no value)","span")].concat(["year","building_type","building_id"].map(this.iline(b))))]);}},map.core.model.kinds.BReffer);;