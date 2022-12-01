from django.urls import path

from . import views
from .views import ObrisiZahtevView

app_name = "auctions"

urlpatterns = [
    path("", views.ponude_view, name="ponude"),
    path(
        "kategorija/<str:category_name>",
        views.category_details_view,
        name="category_details_view",
    ),
    path(
        "zahtev/<str:zahtev_id>", views.auction_details_view, name="detalji_ponude_view"
    ),
    path("zahtevi/kreiranje", views.kreiranje_zahteva_view, name="kreiranje_zahteva"),
    path(
        "zahtevi/brisanje/<int:pk>/", ObrisiZahtevView.as_view(), name="obrisi_zahtev"
    ),
    path("zahtevi/aktivni", views.aktivni_zahtevi_view, name="aktivni_zahtevi_view"),
]
