from django.db import models


class RadniDaniServisa(models.TextChoices):
    ponedeljak = "Ponedeljak", "Ponedeljak"
    utorak = "Utorak", "Utorak"
    sreda = "Sreda", "Sreda"
    cetvrtak = "Četvrtak", "Četvrtak"
    petak = "Petak", "Petak"
    subota = "Subota", "Subota"
    nedelja = "Nedelja", "Nedelja"
