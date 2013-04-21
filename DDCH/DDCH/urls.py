from django.conf.urls import patterns, include, url
from core.views import DashboardView
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'core.views.custom_login', name='login'),
    url(r'^analyse/$', 'bills.views.analyse_view', name='analyse'),
    url(r'^expenses/$', 'bills.views.expense_view', name='expenses'),
    url(r'^$', DashboardView.as_view(), name='home'),
    url(r'^logout/$', 'core.views.custom_logout', name='logout'),

    # url(r'^DDCH/', include('DDCH.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
