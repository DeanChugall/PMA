from django.db import models


class Gradovi(models.TextChoices):
    beograd = "Beograd", "Beograd"
    novi_sad = "Novi Sad", "Novi Sad"
