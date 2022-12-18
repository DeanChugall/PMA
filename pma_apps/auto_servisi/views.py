from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from pma_apps.auctions.models import Auction, Bid, Category
from pma_apps.auto_servisi.forms import (
    KreirajServisKorisnikaForm,
    UrediProfilServisaForm,
    UrediServisForm,
)
from pma_apps.users.models import Servis, ServisProfile


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

    def get_context_data(self, **kwargs):
        servis = Servis.objects.all().filter(username=self.kwargs["username"]).first()
        profil_servisa = ServisProfile.objects.all().filter(user_id=servis.id).first()

        context = {
            "categories": Category.objects.all(),
            "servis": servis,
            "profil_servisa": profil_servisa,
        }

        return context


def profil_servisa_update_view(request, username):
    servis = get_object_or_404(Servis, username=username)
    servis_form = UrediServisForm(request.POST or None, instance=servis)

    servis_profile = get_object_or_404(ServisProfile, user_id=servis.id)
    servis_profile_form = UrediProfilServisaForm(
        request.POST or None, instance=servis_profile
    )

    if request.method == "POST":
        if servis_form.is_valid() and servis_profile_form.is_valid():
            servis.save()
            servis_profile.save()

            return redirect("auto_servis:detalji_servisa", servis.username)

    context = {
        "categories": Category.objects.all(),
        "detalji_servisa": servis_form,
        "detalji_profila_servisa": servis_profile_form,
        "vozac_obj": servis,
    }

    return render(request, "auto_servis/uredi-auto-servis.html", context)


class ListaPonudaServisaView(LoginRequiredMixin, generic.ListView):
    template_name = "auto_servis/sve-ponude-jednog-servisa.html"
    context_object_name = "sve_ponude_servisa"

    def get_context_data(self, **kwargs):

        ponude = Bid.objects.all().filter(servis_id=self.request.user.id)

        id_pracenog_zahteva = self.request.user.watchlist.all()

        for auction in ponude:
            auction.image = auction.auction.get_images.first()
            auction.amount = auction.auction.get_bids.first()

        page = self.request.GET.get("page", 1)
        paginator = Paginator(ponude, 9)

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context = {
            "categories": Category.objects.all(),
            "zahtevi_vozaca": ponude,
            "pages": pages,
            "id_pracenog_zahteva": id_pracenog_zahteva,
        }

        return context

    def get_queryset(self):
        queryset = Servis.objects.all()
        return queryset


class ListaPrihvacenihPonudaServisaView(LoginRequiredMixin, generic.ListView):
    """
    Not in use for now ..... Za listing svih ponuda koje je Serviser dobio.
    """

    template_name = "auto_servis/sve-ponude-jednog-servisa.html"
    context_object_name = "sve_ponude_servisa"

    def get_context_data(self, **kwargs):

        auctions = Auction.objects.all().filter(buyer__username=self.kwargs["username"])

        id_pracenog_zahteva = self.request.user.watchlist.all()

        for auction in auctions:
            auction.image = auction.get_images.first()
            auction.amount = auction.get_bids.first()

        page = self.request.GET.get("page", 1)
        paginator = Paginator(auctions, 9)

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context = {
            "categories": Category.objects.all(),
            "zahtevi_vozaca": auctions,
            "pages": pages,
            "id_pracenog_zahteva": id_pracenog_zahteva,
        }

        return context

    def get_queryset(self):
        queryset = Servis.objects.all()
        return queryset
