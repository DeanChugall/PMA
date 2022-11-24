from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from pma_apps.auctions.models import Auction, Bid, Category
from pma_apps.users.models import ServisProfile, VozacProfile

User = get_user_model()


def ponude_view(request):
    """
    The default route which renders a Dashboard page
    """
    auctions_obj = Auction.objects.all()

    expensive_auctions = Auction.objects.order_by("-starting_bid")[:4]

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
        "auctions/auctions.html",
        {
            "categories": Category.objects.all(),
            "auctions_obj": auctions_obj,
            "expensive_auctions": expensive_auctions,
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

    category = Category.objects.get(category_name=category_name)
    auctions = Auction.objects.filter(category=category)

    for auction in auctions:
        auction.image = auction.get_images.first()

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
        "auctions/auctions_category.html",
        {
            "categories": Category.objects.all(),
            "auctions": auctions,
            "auctions_count": auctions.count(),
            "pages": pages,
            "title": category.category_name,
        },
    )
