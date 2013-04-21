from django.conf.urls import patterns, include, url
from core.views import DashboardView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'core.views.custom_login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),


    url(r'^$', DashboardView.as_view(), name='home'),
    # url(r'^DDCH/', include('DDCH.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
