from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, resolve_url
from django.urls import reverse_lazy
from django.views import generic

from pma_apps.auctions.forms import AuctionForm, BidForm, CommentForm, ImageForm
from pma_apps.auctions.models import Auction, Bid, Category, Image
from pma_apps.users.models import ServisProfile, VozacProfile

User = get_user_model()


def ponude_view(request):
    """
    The default route which renders a Dashboard page
    """
    auctions_obj = Auction.objects.all()

    for auction in auctions_obj:
        auction.image = auction.get_images.first()

    # Show 5 auctions_obj per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions_obj, 25)

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
            "auctions_count": Auction.objects.all().count(),
            "bids_count": Bid.objects.all().count(),
            "categories_count": Category.objects.all().count(),
            "users_count": VozacProfile.objects.all().count(),
            "servisa_count": ServisProfile.objects.all().count(),
            "pages": pages,
            "title": "Dashboard",
        },
    )


def category_details_view(request, category_name):
    """
    Clicking on the name of any category takes the user to a page that
    displays all the active listings in that category
    Auctions are paginated: 3 per page
    """

    category = get_object_or_404(Category, category_name=category_name)
    auctions = Auction.objects.filter(category=category).order_by("-date_created")

    for auction in auctions:
        auction.image = auction.get_images.first()
        auction.amount = auction.get_bids.first()

    # Show 3 active auctions per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions, 24)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(
        request,
        "auctions/auctions_category.html",
        {
            "categories": Category.objects.all(),
            "auctions": auctions,
            "auctions_count": auctions.count(),
            "pages": pages,
            "title": category.category_name,
        },
    )


@login_required
def auction_details_view(request, zahtev_id):
    """
    It renders a page that displays the details of a selected auction
    """
    if not request.user.is_authenticated:
        next_page = request.GET.get("next", "/")
        return resolve_url(next_page, "/")

    auction = Auction.objects.get(id=zahtev_id)

    # Filtrirane ponude Auto Servisa za odredjeni zahtev za ponudu.
    ponude_auto_servisa = Bid.objects.filter(auction=auction.id)
    ponude_auto_servisa_zadnja_cena = Bid.objects.filter(auction=auction.id).first()

    if request.user in auction.watchers.all():
        auction.is_watched = True
    else:
        auction.is_watched = False

    return render(
        request,
        "auctions/detalji_zahteva.html",
        {
            "categories": Category.objects.all(),
            "auction": auction,
            "images": auction.get_images.all(),
            "bid_form": BidForm(),
            "comments": auction.get_comments.all(),
            "comment_form": CommentForm(),
            "title": "Auction",
            "ponude_auto_servisa": ponude_auto_servisa,
            "ponude_auto_servisa_zadnja_cena": ponude_auto_servisa_zadnja_cena,
        },
    )


@login_required
def kreiranje_zahteva_view(request):
    """
    It allows the user to create a new zahtev
    """
    image_form_set = forms.modelformset_factory(Image, form=ImageForm, extra=1)

    if request.method == "POST":
        auction_form = AuctionForm(request.POST, request.FILES)
        image_form = image_form_set(
            request.POST, request.FILES, queryset=Image.objects.none()
        )

        if auction_form.is_valid() and image_form.is_valid():
            new_auction = auction_form.save(commit=False)
            new_auction.creator = request.user
            new_auction.save()

            for auction_form in image_form.cleaned_data:
                if auction_form:
                    image = auction_form["image"]

                    new_image = Image(auction=new_auction, image=image)
                    new_image.save()

            return render(
                request,
                "auctions/kreiranje_zahteva.html",
                {
                    "categories": Category.objects.all(),
                    "auction_form": AuctionForm(),
                    "image_form": image_form_set(queryset=Image.objects.none()),
                    "title": "Create Auction",
                    "success": True,
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
                    "title": "Create Auction",
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
                "title": "Create Auction",
            },
        )


class ListaZahtevaVozacaView(LoginRequiredMixin, generic.ListView):
    """Lista svih Zahteva filtrirana po polju username Vozaca"""

    template_name = "auctions/aktivni_zahtevi_vozaca.html"

    def get_context_data(self, **kwargs):
        auctions = Auction.objects.all().filter(
            creator__username=self.kwargs["username"]
        )

        for auction in auctions:
            auction.image = auction.get_images.first()
            auction.amount = auction.get_bids.first()

        context = {
            "categories": Category.objects.all(),
            "zahtevi_vozaca": auctions,
        }

        return context

    def get_queryset(self):
        auctions = Auction.objects.all()
        return auctions


class ObrisiZahtevView(LoginRequiredMixin, generic.DeleteView):
    template_name = "ponude/obrisi_zahtev.html"
    queryset = Auction.objects.all()
    form_class = AuctionForm
    context_object_name = "zahtev"

    def get_success_url(self):
        return reverse_lazy("ponude:ponude")


def aktivni_zahtevi_view(request):
    """
    It renders a page that displays all the currently active auction listings
    Active auctions are paginated: 3 per page
    """
    category_name = request.GET.get("category_name", None)
    if category_name is not None:
        auctions = Auction.objects.filter(active=True, category=category_name)
    else:
        auctions = Auction.objects.filter(active=True)

    for auction in auctions:
        auction.image = auction.get_images.first()
        if request.user in auction.watchers.all():
            auction.is_watched = True
        else:
            auction.is_watched = False

    # Show 3 active auctions per page
    page = request.GET.get("page", 1)
    paginator = Paginator(auctions, 3)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(
        request,
        "aktivni_zahtevi.html",
        {
            "categories": Category.objects.all(),
            "auctions": auctions,
            "auctions_count": auctions.count(),
            "pages": pages,
            "title": "Active Auctions",
        },
    )
