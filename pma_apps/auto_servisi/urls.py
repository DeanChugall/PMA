from django.urls import path

from pma_apps.auto_servisi.views import (
    DetaljiServisaView,
    KreirajServisKorisnikaView,
    ListaPonudaServisaView,
    profil_servisa_update_view,
)

app_name = "auto_servisi"

urlpatterns = [
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
]
