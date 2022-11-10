from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from pma_apps.users.forms import DetaljiVozacaForm, KreirajVozacaForm
from pma_apps.users.models import Vozac

User = get_user_model()


class KreirajVozacaView(generic.CreateView):
    template_name = "vozaci/kreiraj_vozaca.html"
    form_class = KreirajVozacaForm
    context_object_name = "kreiraj_vozaca"

    def get_success_url(self):
        return reverse("account_login")


class DetaljiVozacaView(LoginRequiredMixin, generic.DetailView):
    template_name = "vozaci/detalji-vozaca.html"
    queryset = Vozac.objects.all()
    context_object_name = "detalji_vozaca"

    slug_field = "username"
    slug_url_kwarg = "username"


class UrediVozacaView(LoginRequiredMixin, generic.UpdateView):
    template_name = "vozaci/detalji-vozaca.html"
    queryset = Vozac.objects.all()
    form_class = DetaljiVozacaForm
    context_object_name = "uredi_vozaca"

    def get_success_url(self):
        return reverse("account_login")
