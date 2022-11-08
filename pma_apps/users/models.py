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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    #: First and last name do not cover name patterns around the globe
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.VOZAC)

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("first_name"), blank=True, max_length=255)
    last_name = CharField(_("last_name"), blank=True, max_length=255)

    class Meta:
        unique_together = ("email",)

    def __str__(self):
        return f"{self.username} {self.role}"

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


# flake8: noqa: F811
@receiver(post_save, sender=Vozac)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "VOZAC":
        VozacProfile.objects.create(user=instance)


class VozacProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vozac_id = models.IntegerField(null=True, blank=True)

    slika_vozaca = ImageField(null=True, blank=True)

    class Meta:
        db_table: str = "vozaci"
        verbose_name: str = "Vozac"
        verbose_name_plural: str = "Voozaci"
        ordering = ["-vozac_id"]


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

    class Meta:
        db_table: str = "servisi"
        verbose_name: str = "Servis"
        verbose_name_plural: str = "Servisi"
        ordering = ["-servis_id"]


# flake8: noqa: F811
@receiver(post_save, sender=Servis)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "SERVIS":
        ServisProfile.objects.create(user=instance)
