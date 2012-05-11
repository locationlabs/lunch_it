from django.db import models

# Create your models here.

class UserInfo(models.Model):
   username = models.CharField(max_length=256)
   password = models.CharField(max_length=256)
   display_name = models.CharField(max_length=256)

   def __unicode__(self):
      return self.name


class Office(models.Model):
   location = models.CharField(max_length=256)
   name = models.CharField(max_length=256)
   latitude = models.DecimalField(decimal_places=5, max_digits=10)
   longitude = models.DecimalField(decimal_places=5, max_digits=10)

   def __unicode__(self):
      return self.name


class Restaurant(models.Model):
   name = models.CharField(max_length=256)
   address = models.CharField(max_length=256)
   phone = models.CharField(max_length=256)
   notes = models.CharField(max_length=256)
   icon = models.ImageField(upload_to='users/icons')
   url = models.URLField()
   menu_url = models.URLField()
   latitude = models.DecimalField(decimal_places=5, max_digits=10)
   longitude = models.DecimalField(decimal_places=5, max_digits=10)
   walkable = models.BooleanField()

   def __unicode__(self):
      return self.name


class Train(models.Model):
   departureTime = models.DateField()
   captain = models.ForeignKey('User', related_name='+')
   passengers = models.ManyToManyField('User')
   destination = models.ForeignKey('Restaurant')
   notes = models.TextField()

   def __unicode__(self):
      return u'%s train to %s' % (self.departureTime, self.destination)
