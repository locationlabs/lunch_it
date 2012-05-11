from django.db import models

# Create your models here.

class User(models.Model):
   name = models.CharField()

   def __unicode__(self):
      return self.name


class Office(models.Model):
   location = models.CharField()
   name = models.CharField()

   def __unicode__(self):
      return self.name


class Restaurant(models.Model):
   name = models.CharField()
   address = models.CharField()
   icon = models.ImageField()
   url = models.URLField()
   menu_url = models.URLField()
   latitude = models.DecimalField()
   longitude = models.DecimalField()
   walkable = models.BooleanField()

   def __unicode__(self):
      return self.name


class Train(models.Model):
   departureTime = models.DateField()
   captain = models.ForeignKey('User')
   passengers = models.ManyToMany('User')
   destination = models.ForeignKey('Restaurant')

   def __unicode__(self):
      return u'%s train to %s' % (self.departureTime, self.destination)
