import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertURLEqual


class TestZahteviVozaca:
    @pytest.mark.django_db
    def test_lista_zahteva_autorizovani_vozac(
        self, client, novi_jedan_vozac_autorizovan_korisnik_fixture
    ):
        url_kreiraj_vozaca = reverse(
            "ponude:aktivni_zahtevi_vozaca",
            args=[novi_jedan_vozac_autorizovan_korisnik_fixture.username],
        )
        response = client.get(url_kreiraj_vozaca)
        assert response.status_code == 200
        assertTemplateUsed(response, "auctions/aktivni_zahtevi_vozaca.html")

    @pytest.mark.django_db
    def test_lista_zahteva_ne_autorizovani_vozac(
        self, client, novi_jedan_vozac_ne_autorizovan_korisnik_fixture
    ):
        url_kreiraj_vozaca = reverse(
            "ponude:aktivni_zahtevi_vozaca",
            args=[novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username],
        )
        response = client.get(url_kreiraj_vozaca)
        assert response.status_code == 302
        expected_url = (
            f"/prijava?next=/ponude/zahtevi/"
            f"{novi_jedan_vozac_ne_autorizovan_korisnik_fixture.username}/aktivni"
        )
        assertURLEqual(response.url, expected_url)
