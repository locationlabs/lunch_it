from django.conf.urls import patterns, include, url

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'trains.views.index', name='index'),
    url(r'newGroup/', 'trains.views.createNewGroup', name='newTrain'),
    url(r'join/', 'trains.views.joinGroup', name='join'),
    url(r'leave/', 'trains.views.leaveGroup', name='leave'),
    # Examples:
    # url(r'^$', 'lunch_it.views.home', name='home'),
    # url(r'^lunch_it/', include('lunch_it.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# This lets you use static files folder on development environments
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
