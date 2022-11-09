from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pma_apps.users.models import Servis


class KategorijaAutoServisa(models.Model):
    ime_kategorije_auto_servisa = models.CharField(max_length=50)

    class Meta:
        db_table: str = "kategorija_auto_servisa"
        verbose_name = "Kategorija Auto Serivs"
        verbose_name_plural = "Kategorija Auto Serivsa"

    def __str__(self):
        return f"{self.ime_kategorije_auto_servisa}"

    @property
    def count_active_auctions(self):
        return AutoServis.objects.filter(category=self).count()


class AutoServis(models.Model):
    auto_servis_name = CharField(_("Name of Auto Servis"), blank=True, max_length=255)
    description = models.TextField(max_length=800, null=True)
    creator = models.ForeignKey(
        Servis,
        on_delete=models.PROTECT,
        related_name="kreaator_auto_servisa",
        default=1,
    )
    category = models.ForeignKey(
        KategorijaAutoServisa,
        on_delete=models.CASCADE,
        related_name="kategorija_auto_servisa",
        default=1,
    )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table: str = "auto_servisi"
        verbose_name: str = "Auto Servis"
        verbose_name_plural: str = "Auto Servisi"
        ordering = ["-auto_servis_name"]
