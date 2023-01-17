import logging
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from pma_apps.auctions.models import Auction, Bid, Category
from pma_apps.auto_servisi.filters import FilterServisaPoGradovima
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

User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KreirajServisKorisnikaView(generic.CreateView):
    template_name = "auto_servis/kreiraj-servis.html"
    form_class = KreirajServisKorisnikaForm
    context_object_name = "kreiraj_servis"

    def get_success_url(self):
        # Send Mail (Administratoru) da je nalog SERVISA kreiran.
        try:
            logger.info(
                f"<KREIRANJE SERVISA>"
                f">>> KORISNIK {self.object.username}  JE NAPRAVIO NOVI NALOG AUTO SERVISA. <<< "
                f"</KREIRANJE SERVISA>"
            )

            admin_email = settings.ADMINS[0][1]

            # Posalji mail adminu da je kreiran Vozac
            data = (
                (
                    f"Kreiranje novog SERVISA '{self.object.username}'.",
                    f"Poštovani, KORISNIK {self.object.username} je kreirao novi SERVIS!\n"
                    f"-------------------------------------------------------\n"
                    f"\n"
                    f"Srdačan pozdrav, 'Vaš Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [admin_email],
                ),
            )
            send_mass_mail(data)
        except BadHeaderError:  # subject is not properly formatted.
            logger.info("<MAIL-ERROR> >>> Invalid header found <<< </MAIL-ERROR>")
        except SMTPException as e:  # errors related to SMTP.
            logger.info(
                "<MAIL-ERROR>"
                f">>> here was an error sending an email: {e} <<< "
                "</MAIL-ERROR>"
            )
        return reverse("users:prijava")


class DetaljiServisaView(generic.DetailView):
    template_name = "auto_servis/detalji-servisa.html"
    queryset = Servis.objects.all()
    context_object_name = "detalji_servisa"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        """
        Broj ponuda servisa se dobija tako sto se pozove metoda 'count_ponude' iz
        modela @see:'from pma_apps.users.models ServisProfile'.

        :param kwargs: self, kwargs
        :return: context
        """

        servis = Servis.objects.all().filter(username=self.kwargs["username"]).first()
        profil_servisa = ServisProfile.objects.all().filter(user_id=servis.id).first()

        logger.info(
            f'Poseta korisnika >>> {self.kwargs["username"]} <<< detalju servisa >>> {profil_servisa.ime_servisa} <<< '
        )

        slika_servisa = SlikeServisa.objects.all().filter(servis=profil_servisa)[:1]
        slika_logo_servisa = (
            SlikaLogoServisa.objects.all().filter(servis=profil_servisa).first()
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
            "slika_servisa": slika_servisa,
            "slika_logo_servisa": slika_logo_servisa,
            "reviews": reviews,
        }

        return context


@login_required
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

    # Slika i Logo servisa
    slika_servisa = SlikeServisa.objects.all().filter(servis=servis_profile)[:1]
    logo_servisa = SlikaLogoServisa.objects.all().filter(servis=servis_profile).first()

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

                    new_image = SlikeServisa(servis=servis_profile, slika_servisa=image)
                    new_image.save()

            for servis_form in slika_logoa_image_form.cleaned_data:
                if servis_form:
                    image = servis_form["slika_logo_servisa"]

                    new_image = SlikaLogoServisa(
                        servis=servis_profile, slika_logo_servisa=image
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
        "slika_servisa": slika_servisa,
        "logo_servisa": logo_servisa,
    }

    return render(request, "auto_servis/uredi-auto-servis.html", context)


class ListaSvihServisaView(generic.ListView):
    template_name = "auto_servis/listing-svih-servisa.html"
    context_object_name = "lista_svih_servisa"

    def get_context_data(self, **kwargs):

        # profil_servisa = FilterServisaPoGradovima(ServisProfile.objects.all()
        profil_servisa = FilterServisaPoGradovima(
            self.request.GET,
            queryset=ServisProfile.objects.all(),
        )

        # Prosledi URL parametar ako ima u GET-u za paginaciju.
        get_grad_servisa_pagination_url = self.request.GET.get("grad_auto_servisa")

        # Get Last uploaded logo image for Servis
        for servis in profil_servisa.qs:
            servis.slika_logo_servisa = servis.get_slika_logo_servisa.first()
            servis.prosek_rating = servis.averageReview
            servis.rating = servis.countReview
            servis.ponude = servis.count_ponude
            servis.prihvacene_ponude = servis.count_prihvacene_poonude

        page = self.request.GET.get("page", 1)
        paginator = Paginator(profil_servisa.qs, 10)

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context = {
            "profil_servisa": profil_servisa.qs,
            "profil_servisa_form": profil_servisa.form,
            "categories": Category.objects.all(),
            "pages": pages,
            "get_grad_servisa_pagination_url": get_grad_servisa_pagination_url,
        }

        return context

    def get_queryset(self):
        queryset = (ServisProfile.objects.all(),)
        return queryset


class ListaPonudaServisaView(LoginRequiredMixin, generic.ListView):
    template_name = "auto_servis/sve-ponude-jednog-servisa.html"
    context_object_name = "sve_ponude_servisa"

    def get_context_data(self, **kwargs):

        profil_servisa = ServisProfile.objects.get(user_id=self.request.user.id)

        ponude = Bid.objects.all().filter(servis=profil_servisa)

        prihvacene_ponude = Auction.objects.all().filter(
            buyer__username=self.kwargs["username"]
        )

        id_pracenog_zahteva = self.request.user.watchlist.all()

        for auction in ponude:
            auction.image = auction.auction.get_images.first()
            auction.amount = auction.auction.get_bids.first()
            auction.prihvacena_cena = auction.auction.current_bid
            auction.user = auction.auction.creator.get_profil_vozaca

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
            "prihvacene_ponude": prihvacene_ponude,
        }

        return context

    def get_queryset(self):
        queryset = Servis.objects.all()
        return queryset


class ListaPrihvacenihPonudaServisaView(LoginRequiredMixin, generic.ListView):
    template_name = "auto_servis/sve-prihvacene-ponude-servisa.html"
    context_object_name = "sve_ponude_servisa"

    def get_context_data(self, **kwargs):

        profil_servisa = ServisProfile.objects.get(user_id=self.request.user.id)

        # sve ponude ali isto tako i samo one koje su prihvacene.
        # To je za prikaz u sekciji listinga svih prihvacenih ponuda.
        ponude = (
            Bid.objects.all()
            .filter(servis=profil_servisa)
            .select_related("auction")
            .filter(auction__buyer__username=self.kwargs["username"])
            .filter(auction__active=False)
        )

        id_pracenog_zahteva = self.request.user.watchlist.all()

        for auction in ponude:
            auction.image = auction.auction.get_images.first()
            auction.amount = auction.auction.get_bids.first()
            auction.prihvacena_cena = auction.auction.current_bid
            auction.user = auction.auction.creator.get_profil_vozaca

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


@login_required
def submit_review(request, profil_servisa_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = RatingServisa.objects.get(
                vozac_id=request.user.id, servis_id=profil_servisa_id
            )
            form = RatingServisaForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Zahvaljujemo, Vaš utisak je ažuriran.")

            # Send Mail
            servis = Servis.objects.get(id=profil_servisa_id)
            send_mail(
                "Promena Utiska Vozača!",
                "Poštovani, Vozača je promenuo utisak!",
                settings.EMAIL_HOST_USER,
                [servis.email],
            )

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
                messages.success(request, "Hvala! Vaš utisak je uspešno postavljen.")

                # Send Mail
                servis = Servis.objects.get(id=profil_servisa_id)
                send_mail(
                    "Novi Utisak Vozača!",
                    "Poštovani, imate ostavljen novi utisak Vozača!",
                    settings.EMAIL_HOST_USER,
                    [servis.email],
                )
                return redirect(url)


class ObrisiReviewVozacaView(LoginRequiredMixin, generic.DeleteView):
    model = RatingServisa

    context_object_name = "obrisi_utisak_servisa"
    success_message = " Uspešno obrisan utisak."

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        try:
            logger.info(
                f"<SERVIS>"
                f">>> Brisanje Utiska Korisnika:  {self.request.user} <<< "
                f">>> Email Servisa {self.object.servis.email_servisa} <<< "
                f">>> Ime Servisa {self.object.servis.ime_servisa} <<< "
                f"</SERVIS>"
            )

            send_mail(
                f"Brisanje Utisaka Vozača {self.request.user}!",
                f"Poštovani, Vozač {self.request.user} je obrisao svoj utisak!\n"
                f"Srdačan pozdrav, Vaš Popravi Moj Auto.",
                settings.EMAIL_HOST_USER,
                [self.object.servis.email_servisa],
            )
        except BadHeaderError:  # subject is not properly formatted.
            logger.info("<MAIL-ERROR> >>> Invalid header found <<< </MAIL-ERROR>")
        except SMTPException as e:  # errors related to SMTP.
            logger.info(
                "<MAIL-ERROR>"
                f">>> here was an error sending an email: {e} <<< "
                "</MAIL-ERROR>"
            )
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class ObrisiServisView(LoginRequiredMixin, generic.DeleteView):
    model = User
    queryset = User.objects.all()

    def get_success_url(self):
        return reverse("landing_page:landing_page")
