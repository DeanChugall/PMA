import pytest

from pma_apps.users.models import Vozac


@pytest.fixture(autouse=False)
def novi_vozac_autorizovan_korisnik_fixture(db, client, django_user_model) -> Vozac:

    vozac = Vozac.objects.create(
        username="dejan",
        password="dejan",
        email="dejan@dejan.com",
        first_name="Dejan",
        last_name="Dejan",
    )

    client.force_login(vozac)

    return vozac
