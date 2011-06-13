from collections import defaultdict
from itertools import chain
import hashlib

from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

EMPTY_CHOICE = ('', '---------')

# Update default settings.
FLEXSELECT = {
    'include_jquery': False,
}
try: FLEXSELECT.update(settings.FLEXSELECT)
except AttributeError: pass
 
def choices_from_queryset(queryset):
    """
    Makes choices from a QuerySet in a format that is usable by the 
    django.forms.widget.Select widget.
    
    queryset: An instance of django.db.models.query.QuerySet
    """
    return chain(
        [EMPTY_CHOICE],
        [(o.pk, smart_unicode(o)) for o in queryset],
    )

def choices_from_instance(instance, widget):
    """
    Builds choices from a model instance using the widgets queryset() method. 
    If any of the widgets trigger fields is not defined on the instance or the
    instance itself is None, None is returned.
    
    instance: An instance of the model used on the current admin page.
    widget: A widget instance given to the FlexSelectWidget.
    """
    try:
        for trigger in widget.triggers:
            getattr(instance, trigger)
    except ObjectDoesNotExist:
        return [('', widget.empty_choices_text(instance))]
    
    return choices_from_queryset(widget.queryset(instance))
    
def details_from_instance(instance, widget):
    """
    Builds html from a model instance using the widgets details() method. If
    any of the widgets trigger fields is not defined on the instance or the
    instance itself is None, None is returned.
    
    instance: An instance of the model used on the current admin page.
    widget: A widget instance given to the FlexSelectWidget.
    """
    try:
        for trigger in widget.triggers:
            getattr(instance, trigger)
        related_instance = getattr(instance, widget.db_field.name)
    except ObjectDoesNotExist:
        return u''
    return widget.details(related_instance, instance)

def instance_from_request(request, widget):
        """
        Returns a partial instance of the widgets model loading it with values
        from a POST request.
        """
        items = dict(request.POST.items())
        values = {}
        for f in widget.db_field.model._meta.fields:
            if f.name in items:
                try:
                    value = f.formfield().to_python(items[f.name])
                    if value is not None:
                        values[f.name] = value
                except ValidationError:
                    pass
        return widget.db_field.model(**values)
    
class FlexSelectWidget(Select):
    """
    A widget for use in the admin that makes it easy to make foreign key fields
    depend on eachother. When you update one foreign key field, the choices
    of one or more other foreign key fields will be updated.
    
    Usage example:
        # In this example the ForeignKey field "customer_contact" will update
        # when the ForeignKey field "client" is changed. 
        
        # First a widget class for the field that should update when other
        # fields change must be defined.
        class CustomerContactRenderer(object):
            triggers = ['client']
            empty_choices_text = 'Please update the client field first'
            
            def details(self, instance):
                return "<div>" + force_unicode(instance.client) + "</div>"
            
            def queryset(self, instance):
                customer = instance.client.department.customer
                return CustomerContact.objects.filter(customer=customer)
                
        # Then the formfield_for_foreignkey() method of the ModelAdmin must be
        # overwritten. 
        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "customer_contact":
                kwargs['widget'] =  FlexSelectWidget(
                    # An instance of the widget class defined above.
                    widget=CustomerContactRenderer()
                    db_field=db_field,
                    modeladmin=self,
                    request=request,
                )
            return super(CaseAdmin, self).formfield_for_foreignkey(db_field, 
                request, **kwargs)
    """
    instances = {}
    """ Instances of widgets with their hashed names as keys."""
    
    class Media:
        js = []
        if FLEXSELECT['include_jquery']:
            googlecdn = "https://ajax.googleapis.com/ajax/libs"
            js.append('%s/jquery/1.6.1/jquery.min.js' % googlecdn)
            js.append('%s/jqueryui/1.8.13/jquery-ui.min.js' % googlecdn)
        js.append('flexselect/js/flexselect.js')
        
    def __init__(self, db_field, modeladmin, request, *args, 
                 **kwargs):
            
        self.db_field = db_field
        self.modeladmin = modeladmin
        self.request = request
        
        self.hashed_name = self._hashed_name()
        FlexSelectWidget.instances[self.hashed_name] = self
        super(FlexSelectWidget, self).__init__(*args, **kwargs)
    
    def _hashed_name(self):
        """
        Each widget will be unique by the name of the field and the class name 
        of the model admin.
        """
        salted_string = "".join([
              settings.SECRET_KEY,
              self.db_field.name, 
              self.modeladmin.__class__.__name__,         
        ])
        return hashlib.sha1(salted_string).hexdigest()
        
    def _get_instance(self):
        """
        Returns a model instance from the url in the admin page.
        """
        if self.request.method == 'POST':
            return instance_from_request(self.request, self)
        else:
            try:
                path = self.request.META['PATH_INFO'].strip('/')
                object_id = int(path.split('/').pop())
                return self.modeladmin.get_object(self.request, object_id)
            except ValueError:
                return None
    
    def _build_js(self):
        """
        Adds the widgets hashed_name as the key with an array of its triggers
        as the value to flexselect.selects.
        """
        return """
            <script>
                var flexselect = flexselect || {};
                flexselect.triggers = flexselect.triggers || {};
                flexselect.triggers.%(field)s = flexselect.triggers.%(field)s || 
                                                                             [];
                flexselect.triggers.%(field)s.push(%(triggers)s);
            </script>""" % {
                'field': self.db_field.name,
                'triggers': 
                    ",".join('["%s", "%s"]' % (t, self.hashed_name) 
                    for t in self.triggers),
            };
 
        
    def render(self, name, value, attrs=None, choices=(), *args, **kwargs):
        """
        Overrides. Reduces the choices by calling the widgets queryset() 
        method and adds a details <span> that is filled with the widgets 
        details() method.
        """
        instance = self._get_instance()
        self.choices = choices_from_instance(instance, self)
        html = []
        html.append(super(FlexSelectWidget, self).render(
            name, value, attrs=attrs, 
            *args, **kwargs
        ))
        html.append(self._build_js())
        html.append('<span class="flexselect_details">')
        html.append(details_from_instance(instance, self))
        html.append('</span>')
        return mark_safe("".join(html))
    
    # Methods and properties that must be implemented.
      
    def details(self, related_instance, instance):
        raise NotImplementedError
    
    def queryset(self, instance):
        raise NotImplementedError
    
    def empty_choices_text(self, instance):
        raise NotImplementedError
    
    