from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from pma_apps.auctions.models import Auction, Bid, Category
from pma_apps.auto_servisi.forms import (
    ImageLogoaServisaForm,
    ImageServisaForm,
    KreirajServisKorisnikaForm,
    RatingServisaForm,
    UrediProfilServisaForm,
    UrediServisForm,
)
from pma_apps.users.models import (
    RatingServisa,
    Servis,
    ServisProfile,
    SlikaLogoServisa,
    SlikeServisa,
    Vozac,
)


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
        # TODO Proslediti broj ponuda servisa
        servis = Servis.objects.all().filter(username=self.kwargs["username"]).first()
        profil_servisa = ServisProfile.objects.all().filter(user_id=servis.id).first()
        slika_profila_servisa = SlikeServisa.objects.all().filter(servis=servis).first()
        slika_logo_servisa = (
            SlikaLogoServisa.objects.all().filter(servis=servis).first()
        )

        # Broj ponuda Servisa
        broj_ponuda_servisa = Bid.objects.all().filter(servis=profil_servisa).count()

        # Uzmi sve utiske
        reviews = RatingServisa.objects.filter(servis_id=profil_servisa.id, status=True)

        context = {
            "categories": Category.objects.all(),
            "servis": servis,
            "broj_ponuda_servisa": broj_ponuda_servisa,
            "profil_servisa": profil_servisa,
            "slika_profila_servisa": slika_profila_servisa,
            "slika_logo_servisa": slika_logo_servisa,
            "reviews": reviews,
        }

        return context


def profil_servisa_update_view(request, username):

    # Slike Auto Servisa
    slika_auto_servisa_form_set = forms.modelformset_factory(
        SlikeServisa, form=ImageServisaForm, extra=1
    )

    # Logo Auto Servisa
    slika_logoa_form_set = forms.modelformset_factory(
        SlikaLogoServisa, form=ImageLogoaServisaForm, extra=1
    )

    # Servis obj.
    servis = get_object_or_404(Servis, username=username)
    servis_form = UrediServisForm(request.POST or None, instance=servis)

    # Profil Servisa obj.
    servis_profile = get_object_or_404(ServisProfile, user_id=servis.id)
    servis_profile_form = UrediProfilServisaForm(
        request.POST or None, instance=servis_profile
    )

    if request.method == "POST":

        slika_servisa_image_form = slika_auto_servisa_form_set(
            request.POST, request.FILES, queryset=SlikeServisa.objects.none()
        )

        slika_logoa_image_form = slika_logoa_form_set(
            request.POST, request.FILES, queryset=SlikaLogoServisa.objects.none()
        )

        if (
            servis_form.is_valid()
            and servis_profile_form.is_valid()
            and slika_servisa_image_form.is_valid()
            and slika_logoa_image_form.is_valid()
        ):
            servis.save()
            servis_profile.save()

            for servis_form in slika_servisa_image_form.cleaned_data:
                if servis_form:
                    image = servis_form["slika_servisa"]

                    new_image = SlikeServisa(servis=servis, slika_servisa=image)
                    new_image.save()

            for servis_form in slika_logoa_image_form.cleaned_data:
                if servis_form:
                    image = servis_form["slika_logo_servisa"]

                    new_image = SlikaLogoServisa(
                        servis=servis, slika_logo_servisa=image
                    )
                    new_image.save()

            return redirect("auto_servis:detalji_servisa", servis.username)

    context = {
        "categories": Category.objects.all(),
        "detalji_servisa": servis_form,
        "detalji_profila_servisa": servis_profile_form,
        "vozac_obj": servis,
        "slike_servisa_form": slika_auto_servisa_form_set(
            queryset=SlikeServisa.objects.none()
        ),
        "slika_logoa_form": slika_logoa_form_set(
            queryset=SlikaLogoServisa.objects.none()
        ),
    }

    return render(request, "auto_servis/uredi-auto-servis.html", context)


class ListaPonudaServisaView(LoginRequiredMixin, generic.ListView):
    template_name = "auto_servis/sve-ponude-jednog-servisa.html"
    context_object_name = "sve_ponude_servisa"

    def get_context_data(self, **kwargs):

        profil_servisa = ServisProfile.objects.get(user_id=self.request.user.id)

        ponude = Bid.objects.all().filter(servis=profil_servisa)

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


def submit_review(request, profil_servisa_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = RatingServisa.objects.get(
                vozac_id=request.user.id, servis_id=profil_servisa_id
            )
            form = RatingServisaForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except RatingServisa.DoesNotExist:
            form = RatingServisaForm(request.POST)
            if form.is_valid():
                data = RatingServisa()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.servis = ServisProfile.objects.get(user=profil_servisa_id)
                data.vozac = Vozac.objects.get(id=request.user.id)
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
