from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from pma_apps.users.models import User, Servis, Vozac


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.category_name}"

    @property
    def count_active_auctions(self):
        return Auction.objects.filter(category=self).count()


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800, null=True)
    creator = models.ForeignKey(
        Vozac, on_delete=models.PROTECT, related_name="auction_creator", default=1
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="auction_category", default=1
    )
    date_created = models.DateTimeField(default=timezone.now)
    starting_bid = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        default=0.01,
    )
    current_bid = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=True,
        null=True,
    )
    buyer = models.ForeignKey(Servis, on_delete=models.PROTECT,blank=True, null=True)
    watchers = models.ManyToManyField(Servis, related_name="watchlist", blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction #{self.id}: {self.title} ({self.creator})"


class Image(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="get_images"
    )
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"{self.image}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    servis = models.ForeignKey(Servis, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bid #{self.id}: {self.amount} on {self.auction.title} by {self.amount.username}"


class Comment(models.Model):
    vozac = models.ForeignKey(Vozac, on_delete=models.CASCADE, related_name="get_user")
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="get_comments"
    )
    comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def get_creation_date(self):
        return self.date_created.strftime("%B %d %Y")

    def __str__(self):
        return f"Comment #{self.id}: {self.vozac.id} on {self.auction.title}: {self.comment}"
