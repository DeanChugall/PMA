from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.urls import reverse
from django.views import generic

from pma_apps.auctions.models import Category
from pma_apps.users.forms import (
    DetaljiVozacaForm,
    KreirajVozacaForm,
    UlogujVozacaForm,
    UrediProfilVozacaForm,
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

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))

    def get_default_redirect_url(self):
        """
        Return the default redirect URL ka dashboard-u ako je Vozac vec bio ulogovan pre.
        - Vrati redirect URL ka izmeni profila ako je Vozac prvi put logovan.
        - Vrati redirect URL ka izmeni profila ako je SERVIS prvi put logovan.

        """
        context = {}
        user = self.request.user
        if user.is_first_login:
            context["isFirstTime"] = "isFirstTime"
            user.is_first_login = False
            user.save()
            if user.role == User.Role.VOZAC:
                return reverse("users:izmena_profila_vozaca", args=[user.username])
            elif user.role == User.Role.SERVIS:
                return reverse(
                    "auto_servis:izmena_profila_servisa", args=[user.username]
                )

        if self.next_page:
            return resolve_url(self.next_page, "")

        return reverse("ponude:ponude")


class KreirajVozacaView(generic.CreateView):
    template_name = "vozaci/kreiraj_vozaca.html"
    form_class = KreirajVozacaForm
    context_object_name = "kreiraj_vozaca"

    def get_success_url(self):
        return reverse("users:prijava")


class ObrisiVozacaView(LoginRequiredMixin, generic.DeleteView):
    model = User
    queryset = User.objects.all()

    def get_success_url(self):
        return reverse("landing_page:landing_page")


class DetaljiVozacaView(LoginRequiredMixin, generic.DetailView):
    template_name = "vozaci/detalji-vozaca.html"
    form_class = DetaljiVozacaForm
    queryset = Vozac.objects.all()

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


@login_required
def profil_vozaca_update_view(request, username):
    vozac = get_object_or_404(Vozac, username=username)
    vozac_form = UrediVozacaForm(request.POST or None, instance=vozac)

    vozac_profile = get_object_or_404(VozacProfile, user_id=vozac.id)
    vozac_profile_form = UrediProfilVozacaForm(
        request.POST or None, instance=vozac_profile
    )

    if request.method == "POST":
        if vozac_form.is_valid() and vozac_profile_form.is_valid():
            vozac.save()
            vozac_profile.save()

            return redirect("users:detalji_vozaca", vozac.username)

    context = {
        "categories": Category.objects.all(),
        "detalji_vozaca": vozac_form,
        "detalji_profila_vozaca": vozac_profile_form,
        "vozac_obj": vozac,
    }

    return render(request, "vozaci/uredi-vozaca.html", context)
