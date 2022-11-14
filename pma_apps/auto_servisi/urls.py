from django.urls import path

from pma_apps.auto_servisi.views import DetaljiServisaView, KreirajServisView

app_name = "auto_servisi"

urlpatterns = [
    path("kreiraj_servis/", KreirajServisView.as_view(), name="kreiraj_servis"),
    path(
        "detalji-servisa/<str:username>/",
        DetaljiServisaView.as_view(),
        name="detalji_servisa",
    ),
]