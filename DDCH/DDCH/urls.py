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
<<<<<<< HEAD
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),


    url(r'^/$', DashboardView.as_view(), name='home'),
=======
    url(r'^logout/$', 'core.views.custom_logout', name='logout'),


    url(r'^$', DashboardView.as_view(), name='home'),
>>>>>>> cb4f1edae2ba6949e8154cca7989864e2494d656
    # url(r'^DDCH/', include('DDCH.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> cb4f1edae2ba6949e8154cca7989864e2494d656
