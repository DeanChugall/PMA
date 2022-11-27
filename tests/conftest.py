import pytest

from pma_apps.users.models import Servis, Vozac


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
