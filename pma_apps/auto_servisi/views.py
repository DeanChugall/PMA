from django.urls import reverse
from django.views import generic

from pma_apps.auto_servisi.forms import KreirajServisForm


class KreirajServisView(generic.CreateView):
    template_name = "auto_servis/kreiraj-servis.html"
    form_class = KreirajServisForm
    context_object_name = "kreiraj_servis"

    def get_success_url(self):
        return reverse("account_login")
