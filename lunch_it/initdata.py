#!/usr/bin/env python
import os
import sys
import csv
import urllib
import xml.etree.ElementTree
import time

if __name__ == "__main__":
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunch_it.settings")

   from django.core.management import setup_environ
   from lunch_it import settings
   setup_environ(settings)

   from trains.models import Restaurant, Office, UserInfo
   from django.contrib.auth.models import User

   r = csv.reader(open('restaurants.csv'))
   for row in r:
      address = row[1]

      params = urllib.urlencode({'address' : address, 'sensor' : 'true'})

      geo_content = urllib.urlopen('http://maps.googleapis.com/maps/api/geocode/xml?%s' % params)
      geo_content_text = geo_content.read()
      # print geo_content_text
      geo_xml = xml.etree.ElementTree.XML(geo_content_text)
      location_xml = geo_xml.find('result').find('geometry').find('location')
      lat = location_xml.find('lat').text
      lon = location_xml.find('lng').text

      # not currently used
      cuisines = [ c.strip() for c in row[5].split(',') ]

      restaurant = Restaurant(
            name = row[0], address = address, url = row[2],
            phone = row[3], notes = row[4],
            latitude = lat, longitude = lon)

      restaurant.save()
      time.sleep(1)

   u = csv.reader(open('users.csv'))
   user_rows = []
   for user_row in u:
      user_rows.append(user_row)

   duplicate_given_names = set()
   given_names = set()
   for user_row in user_rows:
      if user_row[1] in given_names:
         duplicate_given_names.add(user_row[1])
      else:
         given_names.add(user_row[1])

   for user_row in user_rows:
      if user_row[1] in duplicate_given_names:
         display_name = user_row[1] + " " + user_row[0][0] + "."
      else:
         display_name = user_row[1]
      user = User(username = user_row[2], first_name = user_row[1], last_name = user_row[0])
      user.set_password("password")
      user.save()

      user_info = UserInfo(username = user_row[2],
                  display_name = display_name)
      user_info.save()

   Office(
         name = "LLHQ",
         location = "Emeryville, CA",
         latitude = "37.842139", longitude = "-122.289215").save()

   print 'Created initial data in DB!'


