from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.urls import reverse
from django.views import generic

from pma_apps.auctions.models import Category
from pma_apps.users.forms import DetaljiVozacaForm, KreirajVozacaForm, UlogujVozacaForm
from pma_apps.users.models import Vozac, VozacProfile

User = get_user_model()


class LoginKorisnikaView(LoginView):
    """
    Display the login form and handle the login action.
    """

    form_class = UlogujVozacaForm
    template_name = "account/login.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page, "")
        return reverse("ponude:ponude")


class KreirajVozacaView(generic.CreateView):
    template_name = "vozaci/kreiraj_vozaca.html"
    form_class = KreirajVozacaForm
    context_object_name = "kreiraj_vozaca"

    def get_success_url(self):
        return reverse("users:prijava")


class DetaljiVozacaView(LoginRequiredMixin, generic.UpdateView):
    template_name = "vozaci/detalji-vozaca.html"
    form_class = DetaljiVozacaForm
    queryset = Vozac.objects.all()
    context_object_name = "detalji_vozaca"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):

        vozac = Vozac.objects.all().filter(username=self.kwargs["username"]).first()
        profil_vozaca = VozacProfile.objects.all().filter(user_id=vozac.id).first()

        context = {
            "categories": Category.objects.all(),
            "detalji_vozaca": vozac,
            "profil_vozaca": profil_vozaca,
        }

        return context

    def post(self, request, *args, **kwargs):
        self.queryset = self.get_object()
        return super().post(request, *args, **kwargs)


class UrediVozacaView(LoginRequiredMixin, generic.UpdateView):
    template_name = "vozaci/detalji-vozaca.html"
    # queryset = Vozac.objects.all()
    form_class = DetaljiVozacaForm
    context_object_name = "uredi_vozaca"

    #
    # def get(self, request, *args, **kwargs):
    #     self.queryset = self.get_object()
    #     return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.queryset = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("auctions:ponude")
