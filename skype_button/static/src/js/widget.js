odoo.define('web.web_widget_color', function(require) {
    "use strict";
	
	var core = require('web.core');
    var widget = require('web.form_widgets');
    var FormView = require('web.FormView');

    var QWeb = core.qweb;
    var _lt = core._lt;

	
	var FieldSkype = widget.FieldChar.extend({
		template: 'FieldSkype',
		start: function() {
			console.log('start function');
	        this._super();
	        var $button = this.$el.find('button');
	        $button.click(this.on_button_clicked);
	        this.setupFocus($button);
	    },
	    render_value: function() {
	    	console.log('render function');
	        if (!this.get("effective_readonly")) {
	            this._super();
	        } else {
	            this.$el.find('a')
	                    .attr('href', this.skype_uri())
	                    .text(this.get('value') || '');
	        }
	        console.log(this.get('value'))
	    },
		skype_uri:function(){
			return 'skype:' + this.get('value') + '?'+(this.options.type || 'chat') + (this.options.video?'&video=true':'') + (this.options.topic?'&topic='+encodeURIComponent(this.options.topic):'');
		},
	    on_button_clicked: function() {
	        if (!this.get('value') || !this.is_syntax_valid()) {
	            this.do_warn(_t("Skype Error"), _t("Can't skype to invalid skype address"));
	        } else {
	            location.href = this.skype_uri()
	        }
	    }
	});
	core.form_widget_registry.add('skype', FieldSkype);

    return {
        FieldSkype: FieldSkype
    };
});