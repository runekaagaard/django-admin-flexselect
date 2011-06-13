from django.contrib import admin
from flexselect import FlexSelectWidget
from test_flexselect.tests.models import (Company, Case, Client, 
                                          CompanyContactPerson,)

class CompanyContactPersonWidget(FlexSelectWidget):
    """
    The widget must extend FlexSelectWidget and implement trigger_fields, 
    details(), queryset() and empty_choices_text().
     
    """
    
    trigger_fields = ['client']
    """Fields which on change will update the base field."""
    
    def details(self, base_field_instance, instance):
        """
        HTML appended to the base_field.
        
        - related_instance: An instance of the base_field.
        - instance: A partial instance of the parent model loaded from the
                    request.
                    
        Returns a unicoded string.
        """
        return u"""\
        <div>
            <dl>
                <dt>%s</dt><dd>%s</dd>
                <dt>%s</dt><dd>%s</dd>
            </dl>
        </div>
        """ % ('Company', base_field_instance.company,
               'Email',  base_field_instance.email,
              )
        
    def queryset(self, instance):
        """
        Returns the QuerySet populating the base field. If either of the
        trigger_fields is None, this function will not be called.
        
        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        company = instance.client.company
        return CompanyContactPerson.objects.filter(company=company)
    
    def empty_choices_text(self, instance):
        """
        If either of the trigger_fields is None this function will be called
        to get the text for the empty choice in the select box of the base
        field.
        
        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        return "Please update the client field"
    
class CaseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Alters the widget displayed for the base field.
        """
        if db_field.name == "company_contact_person":
            kwargs['widget'] =  CompanyContactPersonWidget(
                db_field=db_field,
                modeladmin=self,
                request=request,
            )
            kwargs['label'] = 'Contact'
        return super(CaseAdmin, self).formfield_for_foreignkey(db_field, 
            request, **kwargs)

class ClientAdmin(admin.ModelAdmin):
    pass

class CompanyContactPersonAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Case, CaseAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(CompanyContactPerson, CompanyContactPersonAdmin)
admin.site.register(Company, CompanyAdmin)