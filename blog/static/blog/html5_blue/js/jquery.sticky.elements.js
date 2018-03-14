/**
 * jquery plugin to create image jigsaw
 */
var objx;
(function( $ ) {
	$.fn.stikify = function(options)
	{
		var settings = $.extend( {}, $.fn.stikify, options );
		$.fn.stikify.defaults = settings;
		$.each(this, function(index, obj) {
			var $this = $(obj);
			
			if (typeof options.floor == 'undefined')
				options.floor = $this.position().top;

			if (typeof options.cieling == 'undefined') {
				// -10 keeps things safe
				options.cieling = $this.outerHeight()*(-1) - 10; 
			}

			if (typeof options.rate == 'undefined')
				options.rate = 1;	//Normal scroll

			var $prop = options;
			$(window).scroll(function() {
				$this.css("position", "fixed");
				var cp = $(window).scrollTop();
				if (cp == 0) {
					$this.animate({top: $prop.floor +"px"}, "slow");
					$this.animate({opacity: 1}, "fast");
					return;
				}
				var lp = parseInt($this.attr("lp"));
				if(isNaN(lp))
					lp = 0;

				var dy = lp - cp;
				// ^ -ve if going down, +ve otherwise
				var cpos = parseInt($this.css("top"));
				if (isNaN(cpos))
					cpos = options.floor;

				var npos = cpos + dy / $prop.rate;

				if (dy  <= 0 && npos < $prop.cieling) {
					// going up
					npos = $prop.cieling;
				} else if (dy > 0 && npos > $prop.floor) {
					// going down
					npos = $prop.floor;
				}
				$this.css("top", npos +"px");

				if (typeof $prop.trans != 'undefined'
					&& $prop.trans == true) {
					// Transparency as one move up
					$this.css("opacity", 1 - (($prop.floor - npos) / ($prop.floor - $prop.cieling)));
				}
				$this.attr("lp", cp);
			});
		});
		
	}
}( jQuery ));