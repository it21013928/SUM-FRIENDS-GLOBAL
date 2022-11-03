from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView
# from django.views.generic.base import RedirectView
# from django.contrib.staticfiles.storage import staticfiles_storage

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtail.contrib.sitemaps.views import sitemap

# from wagtail_favicon.urls import urls as favicon_urls

from search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),
    path('sitemap.xml', sitemap),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon/favicon.ico'))
    # path('', include(favicon_urls))
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    #path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico')))

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
