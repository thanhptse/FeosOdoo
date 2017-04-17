/*odoo.define('web.web_widget_color', function(require) {
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
});*/

odoo.define('skypebutton.Widget', function(require) {
	"use strict";

	var core = require('web.core');
	var Widget = require('web.form_widgets');

	var QWeb = core.qweb;
	var _lt = core._lt;
	var _callSkype = false;
	var initSkypeApi = function() {
		if (_callSkype) {
			return;
		}
		_callSkype = true;
		var s = document.createElement("script");
		s.type = "text/javascript";
		s.async = true;
		s.defer = true;
		s.src = "/skype_button/static/src/js/skype-uri.js";
		$("head").append(s);
	}

	var callbackFn = false;
	var callbackSkype = function() {
		if (Skype && callbackFn()) {
			return;
		}
		setTimeout(callbackSkype, 1000);
	}

	var SkypeButtonWidget = Widget.FieldChar.extend({
		template : 'SkypeButtonWidget',
		render_value : function() {
			var skype_name = this.format_value(this.get('value'));
			if (this.get('effective_readonly')) {
				var id = 'SkypeButton_Call_' + skype_name + '_1';
				this.$(".oe_skype_button").attr("id", id);
				initSkypeApi();
				callbackFn = function() {
					if (document.getElementById(id)) {
						Skype.ui({
							"name" : "call",
							"element" : id,
							"participants" : [ skype_name ],
							"imageSize" : 32
						});
						return true;
					}
					return false;
				};
				callbackSkype();
			}

		},
	});

	core.form_widget_registry.add('skypebutton', SkypeButtonWidget);

	var RatingWidget = Widget.FieldFloat.extend({
		template : 'RatingWidget',
		render_value : function() {
			console.log('render function');
			var rating_value = this.format_value(this.get('value'));
			if (this.get('effective_readonly')) {
				/*console.log('value is ' + rating_value );
				var id = "rating_button";
				this.$(".oe_rating_button").removeAttr(id);
				this.$(".oe_rating_button").attr("id", id);
				var i;

				for(i=0; i<rating_value; i++){
					this.$("#rating_button").append("<img src='https://cdn2.iconfinder.com/data/icons/circle-icons-1/64/star-16.png'/>");
					console.log(i)
				}*/
				
			}
		}
	});
	
	core.form_widget_registry.add('rating', RatingWidget);
	
	var PrintWidget = Widget.FieldFloat.extend({
		template : 'PrintingWidget',
		start: function() {
			this._super.apply(this, arguments);
			
	    },
		render_value : function() {
			console.log("render print widget");
			this._super();
	    	if(this.get("effective_readonly")){
	    		//do something
	    	}
		}
	});
	
	core.form_widget_registry.add('printing', PrintWidget);
});