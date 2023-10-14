from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.core.views import robots_txt, maintenance
from apps.page.sitemaps import PageSitemap

sitemaps = {

    'page': PageSitemap,

}

urlpatterns = [

    path('admin/', admin.site.urls),

    path('robots.txt', robots_txt),
    path('maintenance/', maintenance, name='maintenance'),

    path('core/', include('apps.core.urls', namespace='core')),

    path('attachment/', include('apps.attachment.urls', namespace='attachment')),

    path('', include('apps.page.urls', namespace='page')),
    path('account/', include('apps.account.urls', namespace='account')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:

    if apps.is_installed('debug_toolbar'):
        import debug_toolbar

        urlpatterns = [

            path('__debug__/', include(debug_toolbar.urls)),

        ] + urlpatterns
