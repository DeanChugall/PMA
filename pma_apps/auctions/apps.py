from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AuctionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pma_apps.auctions"
    verbose_name = _("Auctions")

    def ready(self):
        try:
            import pma_apps.auctions.signals  # noqa F401
        except ImportError:
            pass
