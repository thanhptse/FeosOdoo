odoo.define('web.web_widget_color', function(require) {
    "use strict";
	
	var core = require('web.core');
    var widget = require('web.form_widgets');
    var FormView = require('web.FormView');

    var QWeb = core.qweb;
    var _lt = core._lt;

	
	var FieldSkype = widget.FieldChar.extend({
		template: 'FieldSkype',
		prefix: 'skype',
		
		start: function() {
			this._super.apply(this, arguments);
			
	    },
	    render_value: function() {
	    	this._super();
	    	if(this.get("effective_readonly")){
	    		this.$el.attr('href', this.prefix + ':' + this.get('value') + '?'+(this.options.type || 'call'));
	    	}
	    }
	});
	core.form_widget_registry.add('skype', FieldSkype);

    return {
        FieldSkype: FieldSkype
    };
});