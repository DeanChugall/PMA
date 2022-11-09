from django.urls import path

from . import views

app_name = "landing_page"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing_page"),
]

htmx_urlpatterns = [
    path(
        "kontakt_hello_message/",
        views.kontakt_hello_message,
        name="kontakt_hello_message",
    ),
    path("send_email/", views.send_email, name="send_email"),
]

urlpatterns += htmx_urlpatterns
