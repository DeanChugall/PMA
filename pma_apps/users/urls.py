from django.urls import path

from pma_apps.users.views import DetaljiVozacaView, KreirajServisView

app_name = "users"
urlpatterns = [
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path(
        "detalji-vozaca/<str:username>/",
        DetaljiVozacaView.as_view(),
        name="detalji_vozaca",
    ),
    path("kreiraj_servis/", KreirajServisView.as_view(), name="kreiraj_servis"),
]
