import django_filters

from pma_apps.users.models import ServisProfile


class FilterServisaPoGradovima(django_filters.FilterSet):
    class Meta:
        model = ServisProfile
        fields = ["grad_auto_servisa"]
