import json

from django.http import HttpResponse
from django.forms.widgets import Select

from flexselect import (FlexSelectWidget, choices_from_queryset, 
                        choices_from_instance, details_from_instance,
                        instance_from_request)

def update(request):
    """
    Ajax callback called when on of the trigger fields is changed. Returns
    html for new options and details for the dependent field as json.
    """
    hashed_name = request.POST.__getitem__('hashed_name')
    renderer = FlexSelectWidget.instances[hashed_name]
    
    instance = instance_from_request(request, renderer)
    choices = choices_from_instance(instance, renderer)
    return HttpResponse(json.dumps({
        'options' : Select(choices=choices).render_options([], []),
        'details': details_from_instance(instance, renderer),
        }), mimetype='application/json')
    