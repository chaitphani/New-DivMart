from django.db import models
from django.db.models.fields import DurationField


class BusinessLocation(models.Model):

    name = models.CharField(max_length=100)
    location_id = models.CharField(max_length=50,blank=True,null=True)
    landmark = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    alternative_contact_no = models.CharField(max_length=50,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    website = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class TaxRate(models.Model):

    name = models.CharField(max_length=100)
    rate = models.FloatField(default=0, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.rate)