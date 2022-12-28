"""Kreiranje Korisnika (Servisa & Vozaca)

Kreiranje Korisnika putem Django PROXY nacina.
"""
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Avg, CharField, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pma_apps.utils.godista_automobila import GodisteAutomobila
from pma_apps.utils.gradovi import Gradovi
from pma_apps.utils.image_resize import image_resize
from pma_apps.utils.marke_automobila import MarkeAutomobila
from pma_apps.utils.radno_vreme_servisa import RadniSatiServisa


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        VOZAC = "VOZAC", "Vozac"
        SERVIS = "SERVIS", "Servis"

    base_role = Role.VOZAC

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.VOZAC)
    first_name = CharField(_("first_name"), blank=True, max_length=255)
    last_name = CharField(_("last_name"), blank=True, max_length=255)
    grad = CharField(
        null=False,
        blank=False,
        max_length=100,
        choices=Gradovi.choices,
    )
    is_first_login = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        else:
            return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("email",)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return f"{self.username}"

    @property
    def get_grad_servisa(self):
        """Returns grad Vozaca izostavljene geografske koordinate."""
        return self.grad.split("|")[0]


# ###########################################################
# ##################### VOZACI ##############################
# ###########################################################
class VozacManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.VOZAC)


class Vozac(User):

    base_role = User.Role.VOZAC
    vozac = VozacManager()

    class Meta:
        proxy = True

    def welcome(self):
        return Vozac.objects.get(id=self.id).last_login


class VozacProfile(models.Model):
    class VrstaGoriva(models.TextChoices):
        DIZEL = "Dizel", "Dizel"
        BENZIN = "Benzin", "Benzin"
        HIBRID = "Hibrid", "Hibrid"
        TNG = "Benzin + Gas (TNG)", "Benzin + Gas (TNG)"
        CNG = "Benzin + Metan (CNG)", "Benzin + Metan (CNG)"
        EV = "EV", "EV"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    broj_telefona = CharField(null=True, blank=True, max_length=100)

    # Automobil Vozaca
    vin = CharField(null=True, blank=True, max_length=100)
    marka = CharField(
        null=True, blank=True, max_length=50, choices=MarkeAutomobila.choices
    )
    modell = CharField(null=True, blank=True, max_length=100)
    godiste = CharField(
        null=True, blank=True, max_length=5, choices=GodisteAutomobila.choices
    )
    kilometraza = CharField(null=True, blank=True, max_length=100)
    zapremina_motora = CharField(null=True, blank=True, max_length=100)
    snaga_motora = CharField(null=True, blank=True, max_length=100)
    vrsta_goriva = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=VrstaGoriva.choices,
    )

    class Meta:
        db_table: str = "vozaci"
        verbose_name: str = "Vozac"
        verbose_name_plural: str = "Vozaci"
        ordering = ["-user"]

    @property
    def get_grad_vozaca(self):
        """Returns grad Vozaca izostavljene geografske koordinate."""
        return self.user.grad.split("|")[0]

    @property
    def get_grad_vozaca_latitude(self):
        """Returns grad Vozaca LATITUDE."""
        return self.user.grad.split("|")[1]

    @property
    def get_grad_vozaca_longitude(self):
        """Returns grad Vozaca LONGITUDE."""
        return self.user.grad.split("|")[2]

    def get_absolute_url(self):
        return reverse("users:detalji_vozaca", args=[str(self.username)])


# flake8: noqa: F811
@receiver(post_save, sender=Vozac)
def create_vozac_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.VOZAC:
        VozacProfile.objects.create(user=instance)


# ###########################################################
# ##################### SERVISI #############################
# ###########################################################
class ServisManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SERVIS)


class Servis(User):
    base_role = User.Role.SERVIS
    servis = ServisManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for SERVISe"


class ServisProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    aktivan_servis = models.BooleanField(default=True)
    verifikovan_servis = models.BooleanField(default=False)

    pib_servisa = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    maticni_broj_servisa = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    grad_auto_servisa = CharField(
        null=True,
        blank=True,
        max_length=100,
        choices=Gradovi.choices,
    )

    broj_telefona_vlasnika = CharField(null=True, blank=True, max_length=100)
    broj_telefona_servisa = CharField(null=True, blank=True, max_length=100)

    ime_servisa = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    slogan_servisa = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    email_servisa = models.EmailField(
        max_length=250,
        null=True,
        blank=True,
    )

    opis_servisa = models.TextField(max_length=800, null=True, blank=True)

    adresa_servisa = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    datum_osnivanja = models.CharField(
        null=True, blank=True, max_length=5, choices=GodisteAutomobila.choices
    )

    specijalizovan_za_marku = CharField(
        null=True, blank=True, max_length=50, choices=MarkeAutomobila.choices
    )

    otvoreno_od_ponedeljak_petak = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.OSAM,
    )
    otvoreno_do_ponedeljak_petak = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.SESNAEST,
    )

    otvoreno_od_subota = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.OSAM,
    )

    otvoreno_do_subota = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.SESNAEST,
    )

    otvoreno_od_nedelja = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.NERADAN_DAN,
    )

    otvoreno_do_nedelja = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=RadniSatiServisa.choices,
        default=RadniSatiServisa.NERADAN_DAN,
    )

    web_site_servisa = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    facebook_link = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    youtube_link = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    twitter_link = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    linkedin_link = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    # Za rejting polje
    header = models.CharField(
        max_length=100,
        default="Header",
        null=True,
        blank=True,
    )

    class Meta:
        db_table: str = "servisi"
        verbose_name: str = "Servis"
        verbose_name_plural: str = "Servisi"
        ordering = ["-user"]

    def get_datum_osnivanja(self):
        return self.datum_osnivanja.strftime("%Y")

    @property
    def get_grad_servisa(self):
        """Returns grad Vozaca izostavljene geografske koordinate."""
        return self.grad_auto_servisa.split("|")[0]

    @property
    def get_grad_servisa_latitude(self):
        """Returns grad Vozaca LATITUDE."""
        return self.grad_auto_servisa.split("|")[1]

    @property
    def get_grad_servisa_longitude(self):
        """Returns grad Vozaca LONGITUDE."""
        return self.grad_auto_servisa.split("|")[2]

    # @property
    # def get_logo_servisa(self):
    #     logo_servisa = SlikaLogoServisa.objects.filter(servis=self).first()
    #     return logo_servisa

    @property
    def averageReview(self):
        reviews = RatingServisa.objects.filter(servis=self, status=True).aggregate(
            average=Avg("rating")
        )
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        rounded_avg = round(avg, 2)
        return rounded_avg

    @property
    def countReview(self):
        reviews = RatingServisa.objects.filter(servis=self, status=True).aggregate(
            count=Count("id")
        )
        count = 0
        if reviews["count"] is not None:
            count = int(reviews["count"])
        return count

    @property
    def count_ponude(self):
        from pma_apps.auctions.models import Bid

        ponude = Bid.objects.filter(servis=self).aggregate(count=Count("id"))
        count_ponude = 0
        if ponude["count"] is not None:
            count_ponude = int(ponude["count"])
        return count_ponude

    @property
    def count_prihvacene_poonude(self):
        """
        Prebroj sve prihvacene ponude Vozaca.
        :return: broj prihvacenih ponuda Vozaca.
        """
        from pma_apps.auctions.models import Auction

        prihvacene_poonude = Auction.objects.filter(buyer=self.user).aggregate(
            count=Count("id")
        )
        count_prihvacene_ponude = 0
        if prihvacene_poonude["count"] is not None:
            count_prihvacene_ponude = int(prihvacene_poonude["count"])
        return count_prihvacene_ponude

    def __str__(self):
        return (
            f"Profil Servisa #"
            f"{self.id}: {self.user.username} on {self.ime_servisa}: {self.adresa_servisa}"
        )


class RatingServisa(models.Model):

    servis = models.ForeignKey(
        ServisProfile, on_delete=models.CASCADE, related_name="get_servis_rating"
    )
    vozac = models.ForeignKey(Vozac, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table: str = "rating_servisa"
        verbose_name: str = "Rejting Servisa"
        verbose_name_plural: str = "Rejting Servisa"
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject


class SlikeServisa(models.Model):
    servis = models.ForeignKey(
        ServisProfile, on_delete=models.CASCADE, related_name="get_slika_servisa"
    )
    slika_servisa = models.ImageField(upload_to="slike_servisa/")

    def __str__(self):
        return f"{self.slika_servisa}"

    class Meta:
        db_table: str = "slike_servisa"
        verbose_name: str = "Slike Servisa"
        verbose_name_plural: str = "Slika Servisa"
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        image_resize(self.slika_servisa, 500, 500)
        super().save(*args, **kwargs)


class SlikaLogoServisa(models.Model):
    servis = models.ForeignKey(
        ServisProfile, on_delete=models.CASCADE, related_name="get_slika_logo_servisa"
    )
    slika_logo_servisa = models.ImageField(upload_to="slike_logo_servisa/")

    def __str__(self):
        return f"{self.slika_logo_servisa}"

    class Meta:
        db_table: str = "slika_logo_servisa"
        verbose_name: str = "Slika Logo Servisa"
        verbose_name_plural: str = "Slika Logo Servisa"
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        image_resize(self.slika_logo_servisa, 500, 500)
        super().save(*args, **kwargs)


class KomentariVozacaZaServis(models.Model):
    vozac = models.ForeignKey(Vozac, on_delete=models.CASCADE)
    servis = models.ForeignKey(
        Servis, on_delete=models.CASCADE, related_name="get_comments"
    )
    komentar = models.TextField(max_length=500)
    datum_kreiranja = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table: str = "komentari_vozaca_za_servis"
        verbose_name: str = "Komentari Vozaca Za Servise"
        verbose_name_plural: str = "Komentar Vozaca Za Servis"
        ordering = ["-datum_kreiranja"]

    def __str__(self):
        return f"Komentar Vozaca# {self.id}: {self.vozac.user.username} on {self.servis.ime_servisa}: {self.komentar}"

    def get_creation_date(self):
        return self.datum_kreiranja.strftime("%B %d %Y")


# flake8: noqa: F811
@receiver(post_save, sender=Servis)
def create_servis_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.SERVIS:
        ServisProfile.objects.create(user=instance)
