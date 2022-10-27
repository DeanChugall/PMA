from decimal import Decimal
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from pma_apps.auctions.models import Auction, Bid, Category, Image, User
from pma_apps.auctions.forms import AuctionForm, ImageForm, CommentForm, BidForm
def auctions(request):
    """
    The default route which renders a Dashboard page
    """
    auctions_obj = Auction.objects.all()

    expensive_auctions = Auction.objects.order_by('-starting_bid')[:4]

    for auction in auctions_obj:
        auction.image = auction.get_images.first()

    # Show 5 auctions_obj per page
    page = request.GET.get('page', 1)
    paginator = Paginator(auctions_obj, 5)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'auctions/auctions.html', {
        'categories': Category.objects.all(),
        'auctions_obj': auctions_obj,
        'expensive_auctions': expensive_auctions,
        'auctions_count': Auction.objects.all().count(),
        'bids_count': Bid.objects.all().count(),
        'categories_count': Category.objects.all().count(),
        'users_count': User.objects.all().count(),
        'pages': pages,
        'title': 'Dashboard',
    })
