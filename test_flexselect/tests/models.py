from django.db import models as m

"""
No changes to the models are needed to use flexselect.
"""

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