from django.db import models as m
from django.core.exceptions import ValidationError

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
    
    def clean(self):
        """
        Make sure that the company for client is the same as the company for
        the customer contact person.
        """
        if not self.client.company == self.company_contact_person.company:
            raise ValidationError('The clients and the contacts company does'
                                  ' not match.')
    
    def __unicode__(self):
        return u'Case: %d' % self.id
