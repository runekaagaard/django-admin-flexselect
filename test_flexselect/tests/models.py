from django.db import models as m
from django.utils.encoding import force_unicode

from flexselect import FlexSelectWidget
    
class Company(m.Model):
    name = m.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name

class CompanyContactPerson(m.Model):
    company = m.ForeignKey(Company)
    name = m.CharField(max_length=80)
    email = m.EmailField()
    
    def __unicode__(self):
        return self.name

class CompanyContactPersonWidget(FlexSelectWidget):
    trigger_fields = ['client']
    
    def details(self, related_instance, instance):
        return """\
        <div>
            <dl>
                <dt>%s</dt><dd>%s</dd>
                <dt>%s</dt><dd>%s</dd>
            </dl>
        </div>
        """ % ('Company', related_instance.company,
               'Email',  related_instance.email,
              )
        
    def queryset(self, instance):
        return CompanyContactPerson.objects.filter(
                                                company=instance.client.company)
    
    def empty_choices_text(self, instance):
        return "Please update the client field"
    
class Client(m.Model):
    company = m.ForeignKey(Company)
    name = m.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name
     
class Case(m.Model):
    client = m.ForeignKey(Client)
    company_contact_person = m.ForeignKey(CompanyContactPerson)
    
    def __unicode__(self):
        return u'Case: %d' % self.id