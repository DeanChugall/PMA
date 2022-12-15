"""Kreiranje Korisnika (Servisa & Vozaca)

Kreiranje Korisnika putem Django PROXY nacina.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Avg, CharField, ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pma_apps.utils.godista_automobila import GodisteAutomobila
from pma_apps.utils.gradovi import Gradovi
from pma_apps.utils.radno_vreme_servisa import RadniDaniServisa


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
        default=Gradovi.beograd,
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
        EV = "EV", "EV"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    broj_telefona = CharField(null=True, blank=True, max_length=100)

    # Automobil Vozaca
    vin = CharField(null=True, blank=True, max_length=100)
    marka = CharField(null=True, blank=True, max_length=100)
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
    radni_dan = models.CharField(
        max_length=50,
        choices=RadniDaniServisa.choices,
        default=RadniDaniServisa.ponedeljak,
        null=True,
        blank=True,
    )
    otvoreno_do = models.TimeField(null=True, blank=True)
    otvoreno_od = models.TimeField(null=True, blank=True)

    ime_servisa = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    opis_servisa = models.TextField(null=True, blank=True)

    adresa_servisa = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    datum_osnivanja = models.DateTimeField(null=True, blank=True)

    facebook_link = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    youtube_link = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    twitter_link = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    linkedin_link = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    # Za rejting polje
    header = models.CharField(max_length=100, default="Header")

    class Meta:
        db_table: str = "servisi"
        verbose_name: str = "Servis"
        verbose_name_plural: str = "Servisi"
        ordering = ["-user"]

    def get_datum_osnivanja(self):
        return self.datum_kreiranja.strftime("%Y")

    def average_rating(self) -> float:
        return (
            RatingServisa.objects.filter(user=self).aggregate(Avg("rating"))[
                "rating__avg"
            ]
            or 0
        )

    def __str__(self):
        return (
            f"Profil Servisa #"
            f"{self.id}: {self.user.username} on {self.ime_servisa}: {self.adresa_servisa}"
            f"{self.header}: {self.average_rating()}"
        )


class RatingServisa(models.Model):
    """
    Referenca @see: https://medium.com/geekculture/django-implementing-star-rating-e1deff03bb1c
    """

    vozac = models.ForeignKey(Vozac, on_delete=models.CASCADE)
    servis = models.ForeignKey(ServisProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    datum_kreiranja_rating = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table: str = "rating_servisa"
        verbose_name: str = "Rejting Servisa"
        verbose_name_plural: str = "Rejting Servisa"
        ordering = ["-datum_kreiranja_rating"]

    def __str__(self):
        return f"{self.servis.header}: {self.rating}"


class SlikeServisa(models.Model):
    servis = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_slika_servisa"
    )
    slika_servisa = models.ImageField(upload_to="slike_servisa/")

    def __str__(self):
        return f"{self.slika_servisa}"

    class Meta:
        db_table: str = "slike_servisa"
        verbose_name: str = "Slike Servisa"
        verbose_name_plural: str = "Slika Servisa"
        ordering = ["-slika_servisa"]

    # def save(self, *args, **kwargs):
    #     image_resize(self.image, 500, 500)
    #     super().save(*args, **kwargs)


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
