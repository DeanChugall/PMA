from django.urls import path

from . import views


app_name = "landing_page"

urlpatterns = [
    path("", views.LandingPageView.as_view(), name='landing_page'),

]


htmx_urlpatterns = [
    path("join_hello_message/", views.join_hello_message, name="join_hello_message"),
]

urlpatterns += htmx_urlpatterns
