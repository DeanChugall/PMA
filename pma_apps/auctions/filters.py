import django_filters

from pma_apps.auctions.models import Auction


class FilterZahtevaPoGradovima(django_filters.FilterSet):
    class Meta:
        model = Auction
        fields = ["creator__grad"]
