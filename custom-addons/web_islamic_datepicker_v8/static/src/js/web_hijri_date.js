openerp.web_islamic_datepicker_v8 = function (openerp) {
    var _t = openerp.web._t,
        _lt = openerp.web._lt;
    var QWeb = openerp.web.qweb;
    var lang = ''
    var date_format = ''	
    var res_obj = new openerp.web.Model("res.users");
    openerp.web.DateTimeWidget.include({
        start: function() {
            this.$input = this.$el.find('input.oe_datepicker_master');
            this.$input_picker = this.$el.find('input.oe_datepicker_container');
            this.$input_hijri = this.$el.find('input.oe_hijri');
            $(this.$input_hijri).val('')
            this._super();
            this.$input = this.$el.find('input.oe_simple_date');
        },
        on_picker_select: function(text, instance) {
            this._super(text, instance);	    	
	    text = instance.currentYear +'-'+ (instance.currentMonth+1) +'-'+ instance.currentDay	
            this.convert_gregorian_hijri(text);
        },
        convert_gregorian_hijri: function(text) {
	    
            if (text) {
            	if (text.indexOf('-')!= -1){
            		text_split = text.split('-');
            		year = parseInt(text_split[0]);
            		month = parseInt(text_split[1]);
            		day = parseInt(text_split[2]);			
			calendar = $.calendars.instance('gregorian');
			calendar1 = $.calendars.instance('islamic');			
            		var jd = calendar.toJD(year,month,day);
                	var date = calendar1.fromJD(jd);
			
            	}
            	
            	if(text.indexOf('/')!= -1){            		
            		text_split = text.split('/');
            		year = parseInt(text_split[2]);
            		month = parseInt(text_split[0]);
            		day = parseInt(text_split[1]);			
			calendar = $.calendars.instance('gregorian');
			calendar1 = $.calendars.instance('islamic');			
            		var jd = calendar.toJD(year,month,day);
                	var date = calendar1.fromJD(jd);                	
			
            	}
            	
            	m = (date.month() >=10 ? date.month():"0"+date.month());
            	d = (date.day() >=10 ? date.day():"0"+date.day());         
			
            	$(this.$input_hijri).val(calendar1.formatDate('M d, yyyy', date));
            }
        },
        
        set_value: function(value) {
            this._super(value);
            $(this.$input_hijri).val('')
            this.convert_gregorian_hijri(value);
            this.$input.val(value ? this.format_client(value) : '');
        },
        set_value_from_ui: function() {
            this._super();
            var value = this.$input.val() || false;
            this.value = this.parse_client(value);
            this.convert_gregorian_hijri(this.value);
        },
        set_readonly: function(readonly) {
            this._super(readonly);
            this.$input_hijri.prop('readonly', this.readonly);
        },
	change_datetime: function(e) {
            this.set_value_from_ui_();
            this.trigger("datetime_changed");        
	},
    });
    
    openerp.web.form.FieldDatetime.include({
        initialize_content: function() {
        	
        	res_obj.call("get_calendear_localisation", []).then(function(result) {
        		lang = result['lang'];
			date_format = result['date_format'];
        	});
        	
            if (!this.get("effective_readonly")) {
                this.datewidget = this.build_widget();
                this.datewidget.on('datetime_changed', this, _.bind(function() {
                    this.internal_set_value(this.datewidget.get_value());
                }, this));
                this.datewidget.appendTo(this.$el.find(".oe_simple_date")[0]);
                this.setupFocus(this.datewidget.$input);
                this.format = "%m/%d/%Y";
                showtime = false;
                this.calendar_format = this.field.type;

                this.datewidget.calendar_format = this.field.type;
                if (this.field.type == 'datetime'){
                    this.format = "%m/%d/%Y %H:%M:%S"
                    showtime = true
                }
                var self = this;
               
	   function convert_date_hijri(date) {
		console.log("date-----click here---------",parseInt(date[0].year()),parseInt(date[0].month()),parseInt(date[0].day()));
                   if (!date) {
                       return false
                   }
                
            var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()),parseInt(date[0].month()),parseInt(date[0].day()));
           	var date = $.calendars.instance('gregorian').fromJD(jd);
           	var date_value = new Date(parseInt(date.year()),parseInt(date.month())-1,parseInt(date.day()));
	        self.datewidget.$input.val(date_value.$format(date_format));
            self.datewidget.change_datetime();
           } 
           $('.oe_hijri').calendarsPicker({
        	   
        	   		calendar: $.calendars.instance('islamic',lang),
        			dateFormat: 'M d, yyyy',
        			onSelect: convert_date_hijri,
        			
        	});
        }            
            this.calendar_format = this.field.type;
        },
        convert_gregorian_hijri: function(text) {

        	if (text) {
            	if (text.indexOf('-')!= -1){
            		text_split = text.split('-');
            		year = parseInt(text_split[0]);
            		month = parseInt(text_split[1]);
            		day = parseInt(text_split[2]);
			calendar = $.calendars.instance('gregorian');
	    	        calendar1 = $.calendars.instance('islamic');
            		var jd = $.calendars.instance('gregorian').toJD(year,month,day);
                	var date = $.calendars.instance('islamic').fromJD(jd);
            	}
            	if(text.indexOf('/')!= -1){
            		text_split = text.split('/');
            		year = parseInt(text_split[2]);
            		month = parseInt(text_split[0]);
            		day = parseInt(text_split[1]);
			calendar = $.calendars.instance('gregorian');
	                calendar1 = $.calendars.instance('islamic');	
            		var jd = calendar.toJD(year,month,day);
                	var date = calendar1.fromJD(jd);
            	}
            	return (calendar1.formatDate('M d, yyyy', date));
            }
            return '';
        },
        
        render_value: function() {	    
            if (!this.get("effective_readonly")) {
                this.datewidget.set_value(this.get('value'));
            }
	    else {
                var date_value = openerp.web.format_value(this.get('value'), this, '');
                this.$el.find(".oe_simple_date").text(date_value);
                this.$el.find(".oe_hijri_date").text(this.convert_gregorian_hijri(this.get('value')));
            }
        },
    });
};
