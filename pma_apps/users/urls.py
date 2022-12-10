from allauth.account import views
from django.urls import path

from pma_apps.users.views import (
    DetaljiVozacaView,
    KreirajVozacaView,
    LoginKorisnikaView,
    ObrisiVozacaView,
    profil_vozaca_update_view,
)

app_name = "users"
urlpatterns = [
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    # path("prijava/", views.login, name="vozaci-prijava"),
    path("prijava/", LoginKorisnikaView.as_view(), name="prijava"),
    path("odjava/", views.logout, name="odjava"),  # use allauth view to logout user.
    path("zaboravljena-lozinka", views.password_reset, name="pass-reset"),
    path("kreiraj_vozaca/", KreirajVozacaView.as_view(), name="kreiraj_vozaca"),
    path(
        "detalji-vozaca/<str:username>/",
        DetaljiVozacaView.as_view(),
        name="detalji_vozaca",
    ),
    path(
        "izmena-profila-vozaca/<str:username>/",
        profil_vozaca_update_view,
        name="izmena_profila_vozaca",
    ),
    path(
        "brisanje-vozaca/<int:pk>/",
        ObrisiVozacaView.as_view(),
        name="brisanje_vozaca",
    ),
]
