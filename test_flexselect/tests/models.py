from django.db import models as m
from django.utils.encoding import force_unicode
    
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

class CompanyContactPersonRenderer(object):
    triggers = ['client']
    text_on_invalid = 'Please update the client field first'

    def queryset(self, instance):
        return CompanyContactPerson.objects.filter(company=instance.client.company)
    
class Client(m.Model):
    company = m.ForeignKey(Company)
    name = m.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name
     
class Case(m.Model):
    client = m.ForeignKey(Client)
    company_contact_person = m.ForeignKey(CompanyContactPerson)
    
    def __unicode__(self):
        return str(self.id)