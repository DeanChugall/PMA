from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from pma_apps.auto_servisi.forms import KreirajServisKorisnikaForm
from pma_apps.users.models import Servis


class KreirajServisKorisnikaView(generic.CreateView):
    template_name = "auto_servis/kreiraj-servis.html"
    form_class = KreirajServisKorisnikaForm
    context_object_name = "kreiraj_servis"

    def get_success_url(self):
        return reverse("users:prijava")


class DetaljiServisaView(LoginRequiredMixin, generic.DetailView):
    template_name = "auto_servis/detalji-servisa.html"
    queryset = Servis.objects.all()
    context_object_name = "detalji_servisa"

    slug_field = "username"
    slug_url_kwarg = "username"
