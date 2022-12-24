from django.urls import path

from pma_apps.auto_servisi.views import (
    DetaljiServisaView,
    KreirajServisKorisnikaView,
    ListaPonudaServisaView,
    ListaPrihvacenihPonudaServisaView,
    ListaSvihServisaView,
    ObrisiReviewVozacaView,
    ObrisiServisView,
    profil_servisa_update_view,
)

from . import views

app_name = "auto_servisi"

urlpatterns = [
    path(
        "lista-svih-servisa/", ListaSvihServisaView.as_view(), name="lista_svih_servisa"
    ),
    path(
        "kreiraj_servis/", KreirajServisKorisnikaView.as_view(), name="kreiraj_servis"
    ),
    path(
        "detalji-servisa/<str:username>/",
        DetaljiServisaView.as_view(),
        name="detalji_servisa",
    ),
    path(
        "izmena-profila-servisa/<str:username>/",
        profil_servisa_update_view,
        name="izmena_profila_servisa",
    ),
    path(
        "ponude_servisa/<str:username>/",
        ListaPonudaServisaView.as_view(),
        name="sve_ponude_servisa",
    ),
    path(
        "prihvacene_ponude_servisa/<str:username>/",
        ListaPrihvacenihPonudaServisaView.as_view(),
        name="sve_prihvacene_ponude_servisa",
    ),
    path(
        "submit_review/<int:profil_servisa_id>/",
        views.submit_review,
        name="submit_review",
    ),
    path(
        "obrisi_ustisak_servisa/<int:pk>/",
        ObrisiReviewVozacaView.as_view(),
        name="obrisi_utisak_servisa",
    ),
    path(
        "brisanje-servisa/<int:pk>/",
        ObrisiServisView.as_view(),
        name="brisanje_servisa",
    ),
]
