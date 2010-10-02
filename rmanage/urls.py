from django.conf.urls.defaults import *

from cpanel.views import index, switch_isp, shutdown
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^admin/', include(admin.site.urls)),
    (r'^shutdown/', shutdown),
    (r'^switch_isp/', switch_isp),
    (r'^site_media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
