from django.urls import path

from . import views
from .views import ListaZahtevaVozacaView, ObrisiPonuduZahtevaView, ObrisiZahtevView

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
    path("zahtevi/brisanje/<int:pk>", ObrisiZahtevView.as_view(), name="obrisi_zahtev"),
    path("zahtevi/aktivni", views.aktivni_zahtevi_view, name="aktivni_zahtevi"),
    path(
        "zahtevi/<str:username>/aktivni",
        ListaZahtevaVozacaView.as_view(),
        name="aktivni_zahtevi_vozaca",
    ),
    path("zahtevi/pracenje", views.watchlist_view, name="pacenje_zahteva"),
    path(
        "zahtevi/pracenje/<int:zahtev_id>/edit/<str:reverse_method>",
        views.watchlist_edit,
        name="pracenje_zahteva_edit",
    ),
    # HTMX
    path(
        "zahtevi/<int:pk>/uredjivanje",
        views.uredi_zahtev_vozaca_view,
        name="uredi_zahtev_vozaca",
    ),
    # PONUDE SERVISERA
    path(
        "zahtevi/<str:zahtev_id>/ponuda",
        views.ponuda_zahteva_view,
        name="ponuda_zahteva",
    ),
    path(
        "zahtevi/<int:pk>/brisanje-ponude",
        ObrisiPonuduZahtevaView.as_view(),
        name="obrisi_ponudu_zahteva",
    ),
]
