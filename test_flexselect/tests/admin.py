from django.contrib import admin
from test_flexselect.tests.models import (Company, Case, Client, 
                                          CompanyContactPerson, 
                                          CompanyContactPersonWidget)

class CaseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
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