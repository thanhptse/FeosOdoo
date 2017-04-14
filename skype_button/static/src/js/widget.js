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
		clickable: true,
		
		start: function() {
			console.log('start function');
			this._super.apply(this, arguments);
			
	    },
	    render_value: function() {
	    	console.log('render function')
	    	this._super();
	    	if(this.get("effective_readonly") && this.clickable){
	    		console.log('trong if');
	    		this.$el.attr('href', this.prefix + ':' + this.get('value') + '?'+(this.options.type || 'call'));
	    	}else{
	    		console.log('ngoai if');
	    		console.log(this.get("effective_readonly"))
	    		console.log(this.clickable)
	    	}
	    }
	});
	core.form_widget_registry.add('skype', FieldSkype);

    return {
        FieldSkype: FieldSkype
    };
});