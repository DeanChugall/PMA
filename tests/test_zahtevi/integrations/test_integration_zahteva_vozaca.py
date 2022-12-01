from pma_apps.auctions.models import Auction, Category
from pma_apps.users.models import Vozac


class TestIntegrationsZahtevaVozaca:
    def test_kreiranje_liste_zahteva_vozaca(
        self, tri_vozaca_autorizovan_korisnik_fixture, jedan_zahtev_fixture
    ):
        # TODO: VIDETI TEST FILTERA ZAHTEVA
        svi_zahtevi = Auction.objects.all()
        eee = svi_zahtevi[0].creator.id  # noqa: F841
        rrr = Vozac.objects.all()
        filteriran_zahtev = Auction.objects.filter(creator=rrr[3])  # noqa: F841
        assert Vozac.objects.count() == 4
        assert Auction.objects.count() == 1
        assert Category.objects.count() == 1
