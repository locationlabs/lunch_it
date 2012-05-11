#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunch_it.settings")

   from django.core.management import setup_environ
   from lunch_it import settings
   setup_environ(settings)

   from trains.models import Restaurant, Office

   Restaurant(
         name = "Ruby's", address = "6233 Hollis Street, Emeryville, CA",
         latitude = "37.843351", longitude = "-122.290492",
         walkable = True).save()
   Restaurant(
         name = "Liba Falafel", address = "6355 Hollis Street, Emeryville, CA",
         latitude = "37.834073", longitude = "-122.287681",
         url = "http://libasf.com/",
         menu_url = "http://libasf.com/eat.html",
         walkable = True).save()
   Restaurant(
         name = "Berkeley Bowl West", address = "920 Heinz Avenue, Berkeley, CA",
         latitude = "37.853441", longitude = "-122.289762",
         url = "http://www.berkeleybowl.com/",
         walkable = False).save()

   Office(
         name = "LLHQ",
         location = "Emeryville, CA",
         latitude = "37.842139", longitude = "-122.289215").save()

   print 'Created initial data in DB!'


