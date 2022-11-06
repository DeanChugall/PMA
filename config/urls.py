from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [

    path("", include("pma_apps.landing_page.urls", namespace="landing_page")),


    path("users/", include("pma_apps.users.urls", namespace="users")),

    # path("servis/", include("pma_apps.auto_servis.urls", namespace="auto_servis")),

    path('auctions/', include('pma_apps.auctions.urls', namespace="auctions")),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ADMIN_ENABLED:
    urlpatterns += [path('admin/', admin.site.urls),]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
