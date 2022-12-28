from django.db import models


class RadniDaniServisa(models.TextChoices):
    ponedeljak = "Ponedeljak", "Ponedeljak"
    utorak = "Utorak", "Utorak"
    sreda = "Sreda", "Sreda"
    cetvrtak = "Četvrtak", "Četvrtak"
    petak = "Petak", "Petak"
    subota = "Subota", "Subota"
    nedelja = "Nedelja", "Nedelja"


class RadniSatiServisa(models.TextChoices):
    NERADAN_DAN = "NERADAN DAN"
    NULA = "00:00", "00:00"
    JEDAN = "01:00", "01:00"
    DVA = "02:00", "02:00"
    TRI = "03:00", "03:00"
    CETIRI = "04:00", "04:00"
    PET = "05:00", "05:00"
    SEST = "06:00", "06:00"
    SEDAM = "07:00", "07:00"
    OSAM = "08:00", "08:00"
    DEVET = "09:00", "09:00"
    DESET = "10:00", "10:00"
    JEDANAEST = "11:00", "11:00"
    DVANAEST = "12:00", "12:00"
    TRINAEST = "13:00", "13:00"
    CETRNAEST = "14:00", "14:00"
    PETNAEST = "15:00", "15:00"
    SESNAEST = "16:00", "16:00"
    SEDAMNAEST = "17:00", "17:00"
    OSAMNAEST = "18:00", "18:00"
    DEVETNAEST = "19:00", "19:00"
    DVADESET = "20:00", "20:00"
    DVADESETJEDAN = "21:00", "21:00"
    DVADESETDVA = "22:00", "22:00"
    DVADESETTRI = "23:00", "23:00"
    DVADESETCETIRI = "24:00", "24:00"
