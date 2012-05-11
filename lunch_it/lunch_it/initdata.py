#!/usr/bin/env python
import os
import sys
import csv
import urllib
import xml.etree.ElementTree
import time
projectpath=os.getcwd()
modelpath = os.path.join(projectpath, "..")
sys.path.append(projectpath)
sys.path.append(modelpath)
from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.contrib.auth.models import User
from trains.models import *


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunch_it.settings")

    from django.core.management import setup_environ
    from lunch_it import settings
    setup_environ(settings)

    from trains.models import Restaurant, Office, User
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
        first_name = user_row[1]
        last_name = user_row[0]
        user = User(username = user_row[2],
                  first_name = first_name,
                  last_name = last_name,
                                          )
        user.set_password('password')
        user.save()

    Office(
         name = "LLHQ",
         location = "Emeryville, CA",
         latitude = "37.842139", longitude = "-122.289215").save()

    print 'Created initial data in DB!'


