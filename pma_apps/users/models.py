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


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        VOZAC = "VOZAC", "Vozac"
        SERVIS = "SERVIS", "Servis"

    base_role = Role.VOZAC

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.VOZAC)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("first_name"), blank=True, max_length=255)
    last_name = CharField(_("last_name"), blank=True, max_length=255)

    class Meta:
        unique_together = ("email",)

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


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
        return "Only for VOZACe"


class VozacProfile(models.Model):
    class VrstaGoriva(models.TextChoices):
        DIZEL = "Dizel", "Dizel"
        BENZIN = "Benzin", "Benzin"
        HIBRID = "Hibrid", "Hibrid"
        EV = "EV", "EV"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vozac_id = models.IntegerField(null=True, blank=True)
    broj_telefona = CharField(null=True, blank=True, max_length=100)

    # Automobil Vozaca
    vin = CharField(null=True, blank=True, max_length=100)
    marka = CharField(null=True, blank=True, max_length=100)
    modell = CharField(null=True, blank=True, max_length=100)
    godiste = CharField(null=True, blank=True, max_length=100)
    kilometraza = CharField(null=True, blank=True, max_length=100)
    zapremina_motora = CharField(null=True, blank=True, max_length=100)
    snaga_motora = CharField(null=True, blank=True, max_length=100)
    vrsta_goriva = models.CharField(
        max_length=20, choices=VrstaGoriva.choices, default=VrstaGoriva.DIZEL
    )

    class Meta:
        db_table: str = "vozaci"
        verbose_name: str = "Vozac"
        verbose_name_plural: str = "Vozaci"
        ordering = ["-vozac_id"]


# flake8: noqa: F811
@receiver(post_save, sender=Vozac)
def create_vozac_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.VOZAC:
        VozacProfile.objects.create(user=instance)


# ###########################################################
# ###########################################################
# ###########################################################
# ###########################################################
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
    servis_id = models.IntegerField(null=True, blank=True)
    slika_servisa = ImageField(null=True, blank=True)

    class Meta:
        db_table: str = "servisi"
        verbose_name: str = "Servis"
        verbose_name_plural: str = "Servisi"
        ordering = ["-servis_id"]


# flake8: noqa: F811
@receiver(post_save, sender=Servis)
def create_servis_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.SERVIS:
        ServisProfile.objects.create(user=instance)
