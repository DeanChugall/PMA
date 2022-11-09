from django.db import models


class Kontakti(models.Model):
    ime = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    tema = models.CharField(max_length=255)
    pitanje = models.TextField()
    datum_kreiranja = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table: str = "kontakti"
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakti"

    def __str__(self):
        return f"{self.email}"
