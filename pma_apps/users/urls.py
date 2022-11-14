from allauth.account import views
from django.urls import path

from pma_apps.users.views import DetaljiVozacaView, KreirajVozacaView, LoginVozacaView

app_name = "users"
urlpatterns = [
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    # path("prijava/", views.login, name="vozaci-prijava"),
    path("prijava/", LoginVozacaView.as_view(), name="vozaci-prijava"),
    path("odjava/", views.logout, name="vozaci-odjava"),
    path("zaboravljena-lozinka", views.password_reset, name="vozaci-pass-reset"),
    path("kreiraj_vozaca/", KreirajVozacaView.as_view(), name="kreiraj_vozaca"),
    path(
        "detalji-vozaca/<str:username>/",
        DetaljiVozacaView.as_view(),
        name="detalji_vozaca",
    ),
]
