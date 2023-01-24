import logging
import re
from decimal import Decimal
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mass_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, resolve_url
from django.urls import reverse, reverse_lazy
from django.views import generic

from pma_apps.auctions.filters import FilterZahtevaPoGradovima
from pma_apps.auctions.forms import AuctionForm, BidForm, CommentForm, ImageForm
from pma_apps.auctions.models import Auction, Bid, Category, Image
from pma_apps.users.models import ServisProfile, VozacProfile

User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ponude_view(request):
    """
    The default route which renders a Dashboard page
    """
    auctions_obj = Auction.objects.filter(active=True)[:4]

    for auction in auctions_obj:
        auction.image = auction.get_images.first()

    # Show 5 auctions_obj per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions_obj, 9)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(
        request,
        "auctions/auctions_dashboard.html",
        {
            "categories": Category.objects.all(),
            "auctions_obj": auctions_obj,
            "auctions_count": Auction.objects.filter(active=True).count(),
            "bids_count": Bid.objects.all().count(),
            "categories_count": Category.objects.all().count(),
            "users_count": VozacProfile.objects.all().count(),
            "servisa_count": ServisProfile.objects.all().count(),
            "pages": pages,
        },
    )


@login_required
def category_details_view(request, category_name):
    """
    Clicking on the name of any category takes the user to a page that
    displays all the active listings in that category
    Auctions are paginated: 3 per page
    """

    # Uzmi Sve zahteva i prosledi u header *(obavestenja-zvono)
    auctions_obj = Auction.objects.filter(active=True)[:4]

    category = get_object_or_404(Category, category_name=category_name)

    auctions = FilterZahtevaPoGradovima(
        request.GET,
        queryset=Auction.objects.filter(category=category)
        .filter(active=True)
        .order_by("-date_created"),
    )

    id_pracenog_zahteva = request.user.watchlist.all()

    for auction in auctions.qs:
        auction.image = auction.get_images.first()
        auction.amount = auction.get_bids.first()
        auction.user = auction.creator.get_profil_vozaca

    # Show 3 active auctions per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions.qs, 9)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    # Prosledi URL parametar ako ima u GET-u za paginaciju.
    get_grad_pagination_url = request.GET.get("creator__grad")

    # Samo za prikaz grada u Title HTML-a
    if request.GET.get("creator__grad"):
        grad_filtera = request.GET.get("creator__grad").split("|")[0]
    else:
        grad_filtera = ""

    return render(
        request,
        "auctions/auctions_category.html",
        {
            "categories": Category.objects.all(),
            "category": category,
            "auctions_obj": auctions_obj,
            "auctions": auctions.qs,
            "auctions_form": auctions.form,
            "auctions_count": auctions.qs.count(),
            "pages": pages,
            "title": category.category_name,
            "id_pracenog_zahteva": id_pracenog_zahteva,
            "get_grad_pagination_url": get_grad_pagination_url,
            "grad_filtera": grad_filtera,
        },
    )


@login_required
def detalji_zahteva_view(request, zahtev_id):
    """
    Prikaz detalja jednog zahteva Vozača.
    """
    if not request.user.is_authenticated:
        next_page = request.GET.get("next", "/")
        return resolve_url(next_page, "/")

    # Uzmi Sve zahteva i prosledi u header *(obavestenja-zvono)
    auctions_obj = Auction.objects.filter(active=True)[:4]

    zahtevi = Auction.objects.get(id=zahtev_id)

    id_pracenog_zahteva = request.user.watchlist.all()

    # Filtrirane ponude Auto Servisa za odredjeni zahtev za ponudu.
    ponude_auto_servisa = Bid.objects.filter(auction=zahtevi.id)
    ponude_auto_servisa_zadnja_cena = Bid.objects.filter(auction=zahtevi.id).first()

    profil_vozaca = VozacProfile.objects.get(user=zahtevi.creator)

    profil_servisa = ServisProfile.objects.filter(user=request.user)
    ponuda_jednog_auto_servisa = (
        Bid.objects.all()
        .filter(auction=zahtevi.id)
        .filter(servis=profil_servisa.first())
    )

    # TODO: Implementirati bolju logiku za prikaz Serviserima preporucene zahteve
    preporuceni_zahtevi_servisima = Auction.objects.filter(active=True)[:3]

    for servis in ponude_auto_servisa:
        servis.slika_logo_servisa = servis.servis.get_slika_logo_servisa.first()

    for zahtev in preporuceni_zahtevi_servisima:
        zahtev.image = zahtev.get_images.first()
        zahtev.amount = zahtev.get_bids.first()
        zahtev.prihvacena_cena = zahtev.current_bid

    if request.user in zahtevi.watchers.all():
        zahtevi.is_watched = True
    else:
        zahtevi.is_watched = False

    # Prosledjivanje inicijalne vrednosti za modal uredjivanja ponude
    if ponuda_jednog_auto_servisa:
        cena_servisa = ponuda_jednog_auto_servisa[0].amount
        opis_ponude_servisa = ponuda_jednog_auto_servisa[0].opis_ponude
    else:
        cena_servisa = None
        opis_ponude_servisa = ""

    return render(
        request,
        "auctions/detalji_zahteva.html",
        {
            "categories": Category.objects.all(),
            "auctions_obj": auctions_obj,
            "auction": zahtevi,
            "images": zahtevi.get_images.all(),
            "bid_form": BidForm(
                initial={"amount": cena_servisa, "opis_ponude": opis_ponude_servisa}
            ),
            "comments": zahtevi.get_comments.all(),
            "comment_form": CommentForm(),
            "ponude_auto_servisa": ponude_auto_servisa,
            "ponude_auto_servisa_zadnja_cena": ponude_auto_servisa_zadnja_cena,
            "preporuceni_zahtevi_servisima": preporuceni_zahtevi_servisima,
            "id_pracenog_zahteva": id_pracenog_zahteva,
            "profil_vozaca": profil_vozaca,
            "profil_servisa": profil_servisa,
            "ponuda_jednog_auto_servisa": ponuda_jednog_auto_servisa,
        },
    )


@login_required
def kreiranje_zahteva_view(request):
    """
    It allows the Vozaca to create a new zahtev
    """
    image_form_set = forms.modelformset_factory(Image, form=ImageForm, extra=1)

    profil_vozaca = VozacProfile.objects.get(user=request.user)

    if request.method == "POST":
        zahtev_form = AuctionForm(request.POST, request.FILES)
        image_form = image_form_set(
            request.POST, request.FILES, queryset=Image.objects.none()
        )

        if zahtev_form.is_valid() and image_form.is_valid():
            new_auction = zahtev_form.save(commit=False)
            new_auction.creator = request.user
            new_auction.save()

            for zahtev_form in image_form.cleaned_data:
                if zahtev_form:
                    image = zahtev_form["image"]

                    new_image = Image(auction=new_auction, image=image)
                    new_image.save()

            return render(
                request,
                "auctions/kreiranje_zahteva.html",
                {
                    "categories": Category.objects.all(),
                    "auction_form": AuctionForm(),
                    "image_form": image_form_set(queryset=Image.objects.none()),
                    "success": True,
                    "profil_vozaca": profil_vozaca,
                },
            )
        else:
            return render(
                request,
                "auctions/kreiranje_zahteva.html",
                {
                    "categories": Category.objects.all(),
                    "auction_form": AuctionForm(),
                    "image_form": image_form_set(queryset=Image.objects.none()),
                    "profil_vozaca": profil_vozaca,
                },
            )
    else:
        return render(
            request,
            "auctions/kreiranje_zahteva.html",
            {
                "categories": Category.objects.all(),
                "auction_form": AuctionForm(),
                "image_form": image_form_set(queryset=Image.objects.none()),
                "profil_vozaca": profil_vozaca,
            },
        )


@login_required
def prihvati_ponudu_zahteva_view(request, pk):
    """
    Zatvaranje zahteva Vozaca tako sto se prihvata ponuda Servisa.
    """
    ponuda = Bid.objects.get(id=pk)
    zahtev = ponuda.auction

    if request.user == zahtev.creator:
        zahtev.active = False
        zahtev.buyer = (
            Bid.objects.filter(auction=zahtev).filter(id=ponuda.id).last().servis.user
        )
        zahtev.current_bid = ponuda.amount
        zahtev.save()

        # Send Mail (Vozacu i Serviseru) i loguj da je ponuda prihvacena,
        try:
            logger.info(
                f"<PONUDE>"
                f">>> KORISNIK {request.user}  JE PRIHVATIO PONUDU <<< "
                f"</PONUDE>"
            )

            email_vozac = zahtev.creator.email
            email_servis = ponuda.servis.email_servisa

            datatuple = (
                # Posalji mail vozacu
                (
                    f"Potvrda prihvaćene ponude '{ponuda.auction.title}'.",
                    f"Poštovani {request.user}, prihvatili ste ponudu:\n"
                    f"-------------------------------------------------------\n"
                    f"Servis: {ponuda.servis.ime_servisa}\n"
                    f"Grad: {ponuda.servis.grad_auto_servisa}\n"
                    f"Adresa: {ponuda.servis.adresa_servisa}\n"
                    f"Telefon Vlasnika: {ponuda.servis.broj_telefona_vlasnika}\n"
                    f"Telefon Servisa: {ponuda.servis.broj_telefona_servisa}\n"
                    f"Email Servisa: {ponuda.servis.email_servisa}\n"
                    f"Opis Ponude: {ponuda.opis_ponude}\n"
                    f"Cena: {ponuda.amount} rsd\n"
                    f"\n"
                    f"Srdačan pozdrav, 'Vaš Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [email_vozac],
                ),
                # Posalji mail Servisu
                (
                    f"Vozač {request.user} je prihvatio Vašu ponudu!",
                    f"Čestitamo {ponuda.servis.user.username}, "
                    f"Vozač {request.user} je prihvatio Vašu ponudu u zahtevu: {ponuda.auction.title}!\n"
                    f"-----------------------------------------------------------------------------------\n"
                    f"Naziv Zahteva: {ponuda.auction.title}\n"
                    f"Opis Zahteva: {ponuda.auction.description}\n"
                    f"Datum Kreiranja Zahteva: {ponuda.auction.date_created}\n"
                    f"CENA: {ponuda.amount} rsd\n"
                    f"\n"
                    f"Srdačan pozdrav, Vaš 'Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [email_servis],
                ),
            )
            send_mass_mail(datatuple)
        except BadHeaderError:  # subject is not properly formatted.
            logger.info("<MAIL-ERROR> >>> Invalid header found <<< </MAIL-ERROR>")
        except SMTPException as e:  # errors related to SMTP.
            logger.info(
                "<MAIL-ERROR>"
                f">>> here was an error sending an email: {e} <<< "
                "</MAIL-ERROR>"
            )

        return HttpResponseRedirect(
            reverse("ponude:detalji_ponude_view", args=[zahtev.pk])
        )
    return HttpResponseRedirect(reverse("ponude:detalji_ponude_view", args=[zahtev.pk]))


@login_required
def otkazi_ponudu_zahteva_view(request, pk):
    """
    Otkazivanje Pobnude zahteva Vozaca tako sto se otkazuje ponuda Servisa.
    """
    zahtev = Auction.objects.get(id=pk)
    profil_servisa_email = zahtev.buyer.servisprofile

    ponuda = Bid.objects.filter(auction_id=zahtev.id).first()

    if request.user == zahtev.creator:
        zahtev.active = True
        zahtev.current_bid = ponuda.amount
        zahtev.buyer_id = None
        zahtev.save()

        # Send Mail (Vozacu i Serviseru) i loguj da je ponuda Otkazana,
        try:
            logger.info(
                f"<PONUDE>"
                f">>> KORISNIK {request.user}  JE OTKAZAO PONUDU <<< "
                f"</PONUDE>"
            )

            email_vozac = zahtev.creator.email

            datatuple = (
                # Posalji mail vozacu
                (
                    f"Otkazivanje prihvaćene ponude '{ponuda.auction.title}'.",
                    f"Poštovani {request.user}, otkazali ste ponudu:\n"
                    f"-------------------------------------------------------\n"
                    f"Servis: {profil_servisa_email.ime_servisa}\n"
                    f"Adresa: {profil_servisa_email.adresa_servisa}\n"
                    f"Telefon Vlasnika: {profil_servisa_email.broj_telefona_vlasnika}\n"
                    f"Telefon Servisa: {profil_servisa_email.broj_telefona_servisa}\n"
                    f"Opis Ponude: {ponuda.opis_ponude}\n"
                    f"\n"
                    f"Srdačan pozdrav, 'Vaš Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [email_vozac],
                ),
                # Posalji mail Servisu
                (
                    f"Vozač {request.user} je otkazao Vašu ponudu!",
                    f"Nažalost {profil_servisa_email.user.username},"
                    f" Vozač {request.user} je otkazao Vašu ponudu u zahtevu: {ponuda.auction.title}!\n"
                    f"---------------------------------------------------------------------------------\n"
                    f"Naziv Zahteva: {ponuda.auction.title}\n"
                    f"Opis Zahteva: {ponuda.auction.description}\n"
                    f"Datum Kreiranja Zahteva: {ponuda.auction.date_created}\n"
                    f"\n"
                    f"Srdačan pozdrav, Vaš 'Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [profil_servisa_email.email_servisa],
                ),
            )
            send_mass_mail(datatuple)
        except BadHeaderError:  # subject is not properly formatted.
            logger.info("<MAIL-ERROR> >>> Invalid header found <<< </MAIL-ERROR>")
        except SMTPException as e:  # errors related to SMTP.
            logger.info(
                "<MAIL-ERROR>"
                f">>> here was an error sending an email: {e} <<< "
                "</MAIL-ERROR>"
            )

        return HttpResponseRedirect(
            reverse("ponude:detalji_ponude_view", args=[zahtev.pk])
        )
    return HttpResponseRedirect(reverse("ponude:detalji_ponude_view", args=[zahtev.pk]))


class ListaZahtevaVozacaView(LoginRequiredMixin, generic.ListView):
    """Lista svih Zahteva filtrirana po polju username Vozaca"""

    template_name = "auctions/aktivni_zahtevi_vozaca.html"

    def get_context_data(self, **kwargs):

        auctions = Auction.objects.all().filter(
            creator__username=self.kwargs["username"]
        )

        id_pracenog_zahteva = self.request.user.watchlist.all()

        for auction in auctions:
            auction.image = auction.get_images.first()
            auction.amount = auction.get_bids.first()
            auction.user = auction.creator.get_profil_vozaca

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
        auctions = Auction.objects.all()
        return auctions


class ObrisiZahtevView(LoginRequiredMixin, generic.DeleteView):
    model = Auction

    context_object_name = "brisanje_zahteva"
    success_message = " Uspešno obrisan zahtev."

    def get_success_url(self):
        return reverse_lazy(
            "ponude:aktivni_zahtevi_vozaca",
            kwargs={"username": self.request.user.username},
        )


@login_required
def uredi_zahtev_vozaca_view(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    form = AuctionForm(request.POST or None, instance=auction)

    zahtevi = Auction.objects.get(id=pk)

    profil_vozaca = VozacProfile.objects.get(user=zahtevi.creator)
    profil_servisa = ServisProfile.objects.filter(user=request.user)
    ponuda_jednog_auto_servisa = (
        Bid.objects.all()
        .filter(auction=zahtevi.id)
        .filter(servis=profil_servisa.first())
    )

    context = {
        "form": form,
        "auction": auction,
    }
    if form.is_valid():
        ispravljen_zahtev = form.save(commit=False)
        ispravljen_zahtev.save()
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionForm(request.POST or None, instance=auction)
        context = {
            "form": form,
            "auction": auction,
            "profil_servisa": profil_servisa,
            "ponuda_jednog_auto_servisa": ponuda_jednog_auto_servisa,
            "profil_vozaca": profil_vozaca,
        }
        return render(request, "auctions/partials/detalji_zahteva.html", context)
    return render(request, "auctions/partials/uredi_zahtev_vozaca.html", context)


@login_required
def aktivni_zahtevi_view(request):
    """
    It renders a page that displays all the currently active auction listings
    Active auctions are paginated: 3 per page
    """
    # Uzmi Sve zahteva i prosledi u header *(obavestenja-zvono)
    auctions_obj = Auction.objects.filter(active=True)[:4]

    id_pracenog_zahteva = request.user.watchlist.all()

    category_name = request.GET.get("category_name", None)

    # Filtriranje Zahteva po gradovima
    if category_name is not None:
        auctions = FilterZahtevaPoGradovima(
            request.GET,
            queryset=Auction.objects.filter(active=True, category=category_name),
        )
    else:
        auctions = FilterZahtevaPoGradovima(
            request.GET, queryset=Auction.objects.filter(active=True)
        )

    for auction in auctions.qs:
        auction.image = auction.get_images.first()
        auction.user = auction.creator.get_profil_vozaca

        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 9 active auctions per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions.qs, 9)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    # Prosledi URL parametar ako ima u GET-u za paginaciju.
    get_grad_pagination_url = request.GET.get("creator__grad")

    # Samo za prikaz grada u Title HTML-a
    if request.GET.get("creator__grad"):
        grad_filtera = request.GET.get("creator__grad").split("|")[0]
    else:
        grad_filtera = ""

    return render(
        request,
        "auctions/aktivni_zahtevi.html",
        {
            "categories": Category.objects.all(),
            "auctions": auctions.qs,
            "auctions_obj": auctions_obj,
            "auctions_count": auctions.qs.count(),
            "pages": pages,
            "title": "Aktivni Zahtevi Auctions",
            "id_pracenog_zahteva": id_pracenog_zahteva,
            "auctions_form": auctions.form,
            "get_grad_pagination_url": get_grad_pagination_url,
            "grad_filtera": grad_filtera,
        },
    )


@login_required
def watchlist_view(request):
    """
    It renders a page that displays all the listings Zahteva that a
    user has added to their watchlist Zahteva are paginated: 3 per page.
    """

    # Uzmi Sve zahteva i prosledi u header *(obavestenja-zvono)
    auctions_obj = Auction.objects.filter(active=True)[:4]

    auctions = request.user.watchlist.all()

    for auction in auctions:
        auction.image = auction.get_images.first()
        auction.user = auction.creator.get_profil_vozaca

        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 3 active auctions per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions, 9)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(
        request,
        "auctions/zahtevi_koje_pratim.html",
        {
            "categories": Category.objects.all(),
            "auctions": auctions,
            "auctions_obj": auctions_obj,
            "auctions_count": auctions.count(),
            "pages": pages,
            "title": "Watchlist",
        },
    )


@login_required
def watchlist_edit(request, zahtev_id, reverse_method):
    """
    It allows the users to edit the watchlist - add and
    remove items from the Watchlist
    """

    auction = Auction.objects.get(id=zahtev_id)

    if request.user in auction.watchers.all():
        auction.watchers.remove(request.user)
    else:
        auction.watchers.add(request.user)

    if reverse_method == "ponude:detalji_zahteva_view":
        return detalji_zahteva_view(request, zahtev_id)
    else:
        return HttpResponseRedirect(reverse(reverse_method))


# SERVISERI (Ponude)
@login_required
def ponuda_zahteva_view(request, zahtev_id):
    """
    View za postavljanje Ponuda Servisera na Zahtev Vozaca. Takodje i slanja email-a Servisu i Vozacu.
    """
    auction = Auction.objects.get(id=zahtev_id)

    # Podaci iz POST-a ponude
    amount = Decimal(re.sub(r"[^0-9]", "", request.POST["amount"]))
    opis_ponude = request.POST["opis_ponude"]

    profil_servisa = ServisProfile.objects.get(user_id=request.user.id)

    # Get Ponudu Servisa
    ponuda = Bid.objects.filter(auction_id=auction.id).first()

    auction.current_bid = amount

    # Ocisti sve no int vrednosti iz POST-aa i sacuvaj za validaciju forme.
    post = request.POST.copy()
    post["amount"] = amount
    request.POST = post

    form = BidForm(request.POST)
    if form.is_valid():

        new_bid = form.save(commit=False)
        new_bid.auction = auction
        new_bid.servis = profil_servisa
        new_bid.save()
        auction.save()

        # Send Mail (Vozacu i Serviseru) i loguj da je data Ponuda Servisa,
        try:
            logger.info(
                f"<PONUDE>"
                f">>> KORISNIK {request.user}  JE DAO PONUDU <<< "
                f"</PONUDE>"
            )

            # Ako je Servis uneo Email u profil, posalji na taj mail.
            # Ako nije posalji na mail Vlasnika Servisa.
            if profil_servisa.email_servisa:
                email_servis = profil_servisa.email_servisa
            else:
                email_servis = request.user.email

            # Email Vozaca
            email_vozaca = auction.creator.email

            postavljena_ponuda_email = (
                # Posalji mail Vozacu
                (
                    f"Data je nova ponuda za zahtev: '{auction.title}'.",
                    f"Poštovani {auction.creator.username},\n"
                    f"-------------------------------------------------------\n"
                    f"Servis: {profil_servisa.ime_servisa}\n"
                    f"Adresa: {profil_servisa.adresa_servisa}\n"
                    f"Telefon Vlasnika: {profil_servisa.broj_telefona_vlasnika}\n"
                    f"Telefon Servisa: {profil_servisa.broj_telefona_servisa}\n"
                    f"Cena: {amount}\n"
                    f"Opis Ponude: {opis_ponude}\n"
                    f"\n"
                    f"Srdačan pozdrav, 'Vaš Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [email_vozaca],
                ),
                # Posalji mail Servisu
                (
                    f"Poštovani {profil_servisa.user.username},",
                    f"Dali ste novu ponuda za zahtev: '{auction.title}'.\n"
                    f"---------------------------------------------------------------------------------\n"
                    f"Naziv Zahteva: {ponuda.auction.title}\n"
                    f"Opis Zahteva: {ponuda.auction.description}\n"
                    f"Datum Kreiranja Zahteva: {ponuda.auction.date_created}\n"
                    f"\n"
                    f"---------------------------------------------------------------------------------\n"
                    f"Cena: {amount}\n"
                    f"Opis Ponude: {opis_ponude}\n"
                    f"---------------------------------------------------------------------------------\n\n"
                    f"Srdačan pozdrav, Vaš 'Popravi Moj Auto'.",
                    settings.EMAIL_HOST_USER,
                    [email_servis],
                ),
            )
            send_mass_mail(postavljena_ponuda_email)
        except BadHeaderError:  # subject is not properly formatted.
            logger.info("<MAIL-ERROR> >>> Invalid header found <<< </MAIL-ERROR>")
        except SMTPException as e:  # errors related to SMTP.
            logger.info(
                "<MAIL-ERROR>"
                f">>> here was an error sending an email: {e} <<< "
                "</MAIL-ERROR>"
            )

        return HttpResponseRedirect(
            "{}#listing-ponuda-zahteva".format(
                reverse("ponude:detalji_ponude_view", args=[zahtev_id])
            )
        )
    else:
        return render(
            request,
            "auctions/detalji_zahteva.html",
            {
                "categories": Category.objects.all(),
                "auction": auction,
                "images": auction.get_images.all(),
                "form": BidForm(),
                "error_min_value": True,
                "title": "Auction",
            },
        )


class IzmeniPonuduZahtevaView(LoginRequiredMixin, generic.UpdateView):
    """
    Izmena zahteva Servisera koji se izvrsava u modalu.

    @return: Vraca detalje zahteva i to na '#' selektoru '#listing-ponuda-zahteva'.
    """

    template_name = "auctions/detalji_ponude.html"
    queryset = Bid.objects.all()
    form_class = BidForm
    context_object_name = "brisanje_ponude"

    def form_valid(self, form):
        success_url = self.get_success_url()

        # Uradi update za polje current_bid da bi se prikazala vrednost na frontu.
        self.object.auction.current_bid = self.object.amount
        self.object.auction.save()
        form.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return "{}#listing-ponuda-zahteva".format(
            reverse("ponude:detalji_ponude_view", args=[self.object.auction.id])
        )


class ObrisiPonuduZahtevaView(LoginRequiredMixin, generic.DeleteView):
    """
    Brisanje Ponuda koje je postavio Serviser.
    """

    model = Bid

    def form_valid(self, form):
        """
        Da bi se postavila pravilna cena poslednje ponude zahteva na html template,
        potrebno je prvo proveriti da li uopste ima ponuda posle brisanje, ako ima
        postavi zadnju ucitanu cenu servisera, a ukoliko nema, postavi cenu na 0.

        :param form: BidForm()
        :return: Detalji Zahteva
        """
        success_url = self.get_success_url()

        self.object.delete()  # Obrisi Ponudu

        # Get all Ponude za this Zahtev.
        sve_ponude_zahteva = Bid.objects.all().filter(auction_id=self.object.auction.id)

        if sve_ponude_zahteva.count() > 0:
            self.object.auction.current_bid = sve_ponude_zahteva.first().amount
        else:
            self.object.auction.current_bid = 0
        self.object.auction.save()

        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy("ponude:detalji_ponude_view", args=[self.object.auction.id])
