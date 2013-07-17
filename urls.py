from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'rb.songs.views.songlist', {}, 'songlist'),
    (r'^ownsong/song_(?P<id>\d+)/own_(?P<own>\d)$', 'rb.songs.views.mark_ownership', {}, 'mark_ownership'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, 'login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/rb'}, 'logout'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

)
