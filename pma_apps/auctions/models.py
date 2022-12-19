from django.db import models
from django.utils import timezone

from pma_apps.users.models import User, VozacProfile
from pma_apps.utils.image_resize import image_resize


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.category_name}"

    @property
    def count_active_auctions(self):
        return Auction.objects.filter(category=self).filter(active=True).count()


class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800, null=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_creator",
        default=1,
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="auction_category"
    )

    date_created = models.DateTimeField(default=timezone.now)

    current_bid = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    watchers = models.ManyToManyField(User, related_name="watchlist", blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"Auction #{self.id}: {self.title} ({self.creator})"


class Image(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="get_images"
    )
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"{self.image}"

    def save(self, *args, **kwargs):
        image_resize(self.image, 500, 500)
        super().save(*args, **kwargs)


class Bid(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="get_bids"
    )
    servis = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    opis_ponude = models.TextField(max_length=800, blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Bid #{self.id}: {self.amount} on {self.auction.title}"


class Comment(models.Model):
    vozac = models.ForeignKey(
        VozacProfile, on_delete=models.CASCADE, related_name="get_user"
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="get_comments"
    )
    comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def get_creation_date(self):
        return self.date_created.strftime("%B %d %Y")

    def __str__(self):
        return f"Comment #{self.id}: {self.vozac.id} on {self.auction.title}: {self.comment}"
