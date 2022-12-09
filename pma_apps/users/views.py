from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.urls import reverse, reverse_lazy
from django.views import generic

from pma_apps.auctions.models import Category
from pma_apps.users.forms import (
    DetaljiVozacaForm,
    KreirajVozacaForm,
    UlogujVozacaForm,
    UrediVozacaForm,
)
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


class DetaljiVozacaView(LoginRequiredMixin, generic.DetailView):
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


class UrediVozacaView(LoginRequiredMixin, generic.UpdateView):
    template_name = "vozaci/uredi-vozaca.html"
    queryset = Vozac.objects.all()
    context_object_name = "detalji_vozaca"
    form_class = UrediVozacaForm

    slug_field = "username"
    slug_url_kwarg = "username"

    # def get_context_data(self, **kwargs):
    #     vozac = Vozac.objects.all().filter(username=self.kwargs["username"]).first()
    #     profil_vozaca = VozacProfile.objects.all().filter(user_id=vozac.id).first()
    #
    #     context = {
    #         "form": self.form_class,
    #         "categories": Category.objects.all(),
    #         "detalji_vozaca": vozac,
    #         "profil_vozaca": profil_vozaca,
    #     }
    #
    #     return context
    # def get_context_data(self, **kwargs):
    #     if self.request.method == 'POST':
    #         context = super().get_context_data(**kwargs)
    #         vozac = Vozac.objects.all().filter(username=self.kwargs["username"]).first()
    #         profil_vozaca = VozacProfile.objects.all().filter(user_id=vozac.id).first()
    #
    #         context["profil_vozaca"] = profil_vozaca
    #         context["detalji_vozaca"] = vozac
    #         context["categories"] = Category.objects.all()
    #
    #         form = DetaljiVozacaForm(data=self.request.POST, instance=vozac)
    #
    #         if form.is_valid():
    #             print("DAAAAAAAAAAAAAA")
    #             ispravljen_zahtev = form.save(commit=False)
    #             ispravljen_zahtev.save()
    #         else:
    #             print(f"NEEEEEEEEEEEEEEEE{form.errors}")
    #
    #         print("JEEEEEESTEEE POOOOSTTT")
    #
    #         return context
    #
    #     else:
    #         print("NIJEEEEE POOOOSTTT")

    def get_success_url(self):
        print("OVDE SAAAAAAAAAAAAAAMMMM")
        # return reverse_lazy('ponude:ponude')
        return reverse_lazy(
            "users:detalji_vozaca", kwargs={"username": self.kwargs["username"]}
        )
