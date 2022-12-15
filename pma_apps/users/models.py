"""Kreiranje Korisnika (Servisa & Vozaca)

Kreiranje Korisnika putem Django PROXY nacina.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import CharField, ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
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

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


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

    opis_servisa = models.TextField(null=True, blank=True)

    class Meta:
        db_table: str = "servisi"
        verbose_name: str = "Servis"
        verbose_name_plural: str = "Servisi"
        ordering = ["-user"]


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


# flake8: noqa: F811
@receiver(post_save, sender=Servis)
def create_servis_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.SERVIS:
        ServisProfile.objects.create(user=instance)
