## About Django Admin FlexSelect ##

FlexSelect is a little reusable app for the Django Admin that makes it trivial
to have foreign key fields depend on each other. The developer can by writing a 
simple configuration class filter the choices for the field based on values of  
other fields and append html with additional content as well.

## Installation ##
1. Clone the source

    `git clone git@github.com:runekaagaard/django-admin-flexselect.git`

1. Copy or symlink the "flexselect" folder to your Django project.

1. Add "flexselect" to `INSTALLED_APPS` in "settings.py".

1. Add `(r'^flexselect/', include('flexselect.urls')),` to your "urls.py".

1. Optionally Jquery UI can be added. If it is, the background color of dependent
   fields will fade from orange to white when one of their trigger fields are
   changed. Get it at http://jqueryui.com/download.

## Usage ##

Usage example:

```python
# In this example the ForeignKey field "customer_contact" will update
# when the ForeignKey field "client" is changed. 

# First a renderer class for the field that should update when other
# fields change must be defined.
class CustomerContactRenderer(object):
    triggers = ['client']
    text_on_invalid = 'Please update the client field first'
    
    def queryset(self, instance):
        customer = instance.client.department.customer
        return CustomerContact.objects.filter(customer=customer)
        
# Then the formfield_for_foreignkey() method of the ModelAdmin must be
# overwritten. 
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "customer_contact":
        kwargs['widget'] =  FlexSelectWidget(
            # An instance of the renderer class defined above.
            renderer=CustomerContactRenderer()
            db_field=db_field,
            modeladmin=self,
            request=request,
        )
    return super(CaseAdmin, self).formfield_for_foreignkey(db_field, 
        request, **kwargs)
```

