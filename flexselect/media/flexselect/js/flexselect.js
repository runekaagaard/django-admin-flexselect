var flexselect = flexselect || {};

/**
 * Moves all details fields to after the green plussign.
 */
flexselect.move_after_plussign = function() {
	// Delay execution to after all other initial js have been run.
	window.setTimeout(function() {		
		$('span.flexselect_details').each(function() {
			$(this).next('.add-another').after($(this));
		});
	}, 0);	
};

/**
 * Returns the form element from a field name in the model.
 */
flexselect.get_element = function(field_name) {
	return $('#id_' + field_name);	
};

/**
 * Binds the change event of a field to the flexselect.triggered function.
 */
flexselect.bind_field = function(field_that_triggers, hashed_name, 
field_to_update) {
	flexselect.get_element(field_that_triggers).live('change', {
		'field_to_update': field_to_update,
		'field_that_triggers': field_that_triggers,
		'hashed_name': hashed_name,
	}, flexselect.triggered);
};

/**
 * Binds the flexselect triggers.
 */
flexselect.bind_events = function() {
	for (field_to_update in flexselect.triggers)
		for (j in flexselect.triggers[field_to_update])
			flexselect.bind_field(
				flexselect.triggers[field_to_update][j][0], 
				flexselect.triggers[field_to_update][j][1], 
				field_to_update
			);
};

/**
 * When a trigger field is changed this function is called which queries the
 * server for updated options and details for the dependent field.
 */
flexselect.triggered = function(event) {
	$.ajax({
		url: '/flexselect/update?' + $('form').formSerialize(),
		data: $('form').formSerialize() + '&hashed_name=' 
		                                + event.data.hashed_name,
		type: 'post',
		context: flexselect.get_element(event.data.field_to_update),
		success: function(data) {
			$(this).html(data.options);
			$(this).parent().find('span.flexselect_details').html(data.details);
	    },
	    error: function(data) {
	    	alert("Something went wrong with flexselect.");
	    },
	});
};

/**
 * Overrides the original dismissAddAnotherPopup and triggers a change event
 * on field after the popup has been added.
 */
function dismissAddAnotherPopup(win, newId, newRepr) {
    // Original.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elem.nodeName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 
            && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
    // Added change event trigger.
    $(elem).trigger('change');
}

$(function() {
	flexselect.bind_events();
	flexselect.move_after_plussign();
});


