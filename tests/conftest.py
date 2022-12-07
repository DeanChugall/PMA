import pytest

from pma_apps.auctions.models import Auction, Category
from pma_apps.users.models import Servis, Vozac, VozacProfile


@pytest.fixture(autouse=False)
def novi_jedan_servis_ne_autorizovan_fixture(db, django_user_model) -> Servis:
    jedan_servis_no_auth = Servis.objects.create(
        username="servis1",
        password="servis1",
        email="servis1@servis1.com",
        first_name="servis1",
        last_name="servis1",
    )
    return jedan_servis_no_auth


@pytest.fixture(autouse=False)
def novi_jedan_vozac_ne_autorizovan_korisnik_fixture(db, django_user_model) -> Vozac:
    jedan_vozac_no_auth = Vozac.objects.create(
        username="dejan_no_auth_vozac",
        password="dejan_no_auth_vozac",
        email="dejan_no_auth_vozac@dejan_no_auth_vozac.com",
        first_name="dejan_no_auth_vozac",
        last_name="dejan_no_auth_vozac",
    )
    return jedan_vozac_no_auth


@pytest.fixture(autouse=False)
def novi_jedan_vozac_autorizovan_korisnik_fixture(
    db, client, django_user_model
) -> Vozac:
    vozac = Vozac.objects.create(
        username="dejan",
        password="dejan",
        email="dejan@dejan.com",
        first_name="Dejan",
        last_name="Dejan",
    )
    client.force_login(vozac)
    return vozac


@pytest.fixture(autouse=False)
def novi_jedan_vozac_sa_autom_autorizovan_korisnik_fixture(
    db, django_user_model, novi_jedan_vozac_autorizovan_korisnik_fixture
) -> VozacProfile:

    VozacProfile.objects.update(
        user=novi_jedan_vozac_autorizovan_korisnik_fixture,
        broj_telefona="Dejan",
        vin="WAUZZZ4BZWN049194",
        marka="Renault",
        modell="cenic II",
        godiste="2012",
        kilometraza="195.500",
        zapremina_motora="1900 ccm",
        snaga_motora="120 KS",
    )

    profil_vozaca = VozacProfile.objects.first()
    return profil_vozaca


@pytest.fixture(autouse=False)
def tri_vozaca_autorizovan_korisnik_fixture(db, client, django_user_model) -> Vozac:
    vozaci = Vozac.objects.bulk_create(
        [
            Vozac(
                username="dex",
                password="dex",
                email="dex@dex.com",
                first_name="dex",
                last_name="dex",
            ),
            Vozac(
                username="dea",
                password="dea",
                email="dea@dea.com",
                first_name="dea",
                last_name="Dejdeaan",
            ),
            Vozac(
                username="vea",
                password="vea",
                email="vea@vea.com",
                first_name="vea",
                last_name="vea",
            ),
        ]
    )
    # client.force_login(vozaci)
    return vozaci


@pytest.fixture(autouse=False)
def jedna_kategorija_zahteva_fixture(db) -> Category:
    kategorija = Category.objects.create(
        category_name="MALI SERVIS",
    )

    return kategorija


@pytest.fixture(autouse=False)
def jedan_zahtev_fixture(
    db, novi_jedan_vozac_autorizovan_korisnik_fixture, jedna_kategorija_zahteva_fixture
) -> Auction:
    zahtev = Auction.objects.create(
        title="Pregled Kočnica GOLF 6",
        description="Pregled Kočnica GOLF 6",
        creator=novi_jedan_vozac_autorizovan_korisnik_fixture,
        category=jedna_kategorija_zahteva_fixture,
        date_created="2022-11-29T22:14:02.713Z",
        active=True,
    )

    return zahtev
