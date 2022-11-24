from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.ponude_view, name="ponude"),
    path(
        "kategorija/<str:category_name>",
        views.category_details_view,
        name="category_details_view",
    ),
]
