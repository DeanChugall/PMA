import pytest
from django.urls import reverse, reverse_lazy
from pytest_django.asserts import assertTemplateUsed

from pma_apps.auctions.models import Auction


class TestUZahtevi:
    @pytest.mark.django_db
    def test_kreiraj_zahtev_autorizovani_korisnik(
        self, client, novi_jedan_vozac_autorizovan_korisnik_fixture
    ):
        url_kreiraj_vozaca = reverse("ponude:kreiranje_zahteva")
        response = client.get(url_kreiraj_vozaca)
        assert response.status_code == 200
        assertTemplateUsed(response, "auctions/kreiranje_zahteva.html")

    @pytest.mark.django_db
    def test_kreiraj_zahtev_ne_autorizovani_korisnik(
        self, client, novi_jedan_vozac_ne_autorizovan_korisnik_fixture
    ):
        url_kreiraj_vozaca = reverse("ponude:kreiranje_zahteva")
        response = client.get(url_kreiraj_vozaca)
        assert response.status_code == 302

    def test_obrisi_zahtev(
        self,
        client,
        jedan_zahtev_fixture,
        novi_jedan_vozac_autorizovan_korisnik_fixture,
    ):

        # Proveri koliko je zahteva u bazi (treba da ima 1 zahtev)
        broj_zahteva_u_bazi = Auction.objects.all().count()
        assert broj_zahteva_u_bazi == 1

        url_obrisi_stan = reverse(
            "ponude:obrisi_zahtev", args=[jedan_zahtev_fixture.id]
        )

        response = client.delete(url_obrisi_stan)

        assert response.status_code == 302  # imamo 302 zbog get_success_url u View-u

        assert reverse_lazy("ponude:ponude")  # test get_success_url(ponude:ponude)

        # Proveri koliko je zahteva u bazi (treba da ima 0 zahteva)
        broj_zahteva_u_bazi = Auction.objects.all().count()
        assert broj_zahteva_u_bazi == 0
