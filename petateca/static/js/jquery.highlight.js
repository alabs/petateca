	jQuery.fn.highlight = function(selector, className, eventStart, eventEnd){
	
		// variables
			var className = className || 'highlight-form';
			if(eventStart == undefined && eventEnd == undefined)
			{
				var eventStart = 'mouseover';
				var eventEnd = 'mouseout';
			}
			else if(eventStart == eventEnd || eventStart != undefined && eventEnd == undefined)
			{
				var toggle = true;
			}
		
		// code
			this.each
			(
				function()
				{
				
					var tagName	= this.tagName.toLowerCase();
					
					if(tagName == 'form')
					{
					
						selector		= selector || 'li';
						var elements 	= jQuery("textarea, select, multi-select, :text, :image, :password, :radio, :checkbox, :file", this);
	
						elements.bind
						(
							'focus', 
							function()
							{
								var parents	= jQuery(this).parents(selector);
								var parent	= jQuery(parents.get(0));
								parent.addClass(className);
							}
						);
							
						elements.bind
						(
							'blur', 
							function()
							{
								var parents	= jQuery(this).parents(selector);
								var parent	= jQuery(parents.get(0));
								parent.removeClass(className);
							}
						);

					}
					
					else
					{
	
	
						if(tagName.match(/^(table|tbody)$/) != null)
						{
							selector = selector || 'tr';
						}
						else if(tagName.match(/^(ul|ol)$/) != null)
						{
							selector = selector || 'li';
						}
						else
						{
							selector = '*';
						}
							
						var elements = jQuery(selector, this);
	
						if(toggle)
						{
							elements.bind
								(
								eventStart, 
								function()
								{
									if($(this).hasClass(className))
									{
										$(this).removeClass(className);
									}
									else
									{
										$(this).addClass(className);
									}
								}
							);
						
						}
							
						else
						{
							elements.bind
							(
								eventStart, 
								function()
								{
									$(this).addClass(className);
								}
							);
							
							elements.bind
							(
								eventEnd, 
								function()
								{
									$(this).removeClass(className);
								}
							);
						}
				
					}
				}
			);
				
		// return
			return this;
		
		}
