from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value_tags(name):
    """
    Prosledjivanje settings konstanti u template.
    Usage: {% load settings_value_tags %}.
    Reference: https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/
    :param name: ime settings konstante.
    :return: vrednost settings konstante.
    """
    return getattr(settings, name, "")
