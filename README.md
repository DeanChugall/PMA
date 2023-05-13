# PMA project

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python](https://img.shields.io/badge/HTML%20code%20style-djhtml-orange?logo=html5)](https://github.com/rtts/djhtml)
[![Python](https://img.shields.io/badge/python-3.11.0-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/)
[![Python](https://img.shields.io/badge/no%20package%20install-only%20with%20consensus-green?logo=1001Tracklists&logoColor=yellow)](https://www.python.org/)

---

<p align="left">
  <img width="500" src="https://github.com/DeanChugall/PMA/assets/4832847/774ac0c3-e8c7-4a05-958b-a2bd94bbaa2d" alt="Material Bread logo">
</p>




## Integracija sa Digital Ocean APP platformom

- Napravljen **STAGE server** na APP Digital Ocean platformi [Link ka APP-u](https://popravimojauto.com/).
- U
  sekciji [APP / SETTINGS / DOMAIN](https://cloud.digitalocean.com/apps/8058ee2c-a1c4-420f-bb1c-534672111037/settings?i=8d2545)
  dodati domain name: **popravimojauto.com**.
- Zatim na CloudFlare dodati ponudjenu CNAME varijablu !

---

## Korisne komande:
- Brisanje svih paketa iz PIP-a: ```pip freeze | xargs pip uninstall -y```
- Pre-Commit run: ```pre-commit run```
- HTML pre-commit: ```djhtml -i pma_apps/templates/ .```
- Generisanje hash lozinke:
```python
from django.contrib.auth.hashers import make_password
make_password('pa_ovde_lozinka')
```


---

## Inicijalizacija svih podataka ukoliko mora da se obriše DB (djnago fixture):
[@see reference](https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata)
- <b>Čuvanje svih podataka iz DB-a (fixtures):</b>
- - Prvo se ode u DIR: ``` tests/fixtures_from_db ```
- - Pa iz to dir-a komanda ispod:

```bash
  python ../../manage.py dumpdata --exclude auth.permission --exclude contenttypes  --indent 2 > pma-data.json
```

- <b>Učitavanje inicijalnih podataka u novu bazu:</b>
- - ``` python ../../manage.py loaddata pma-data.json ```

---

## Restore i Bckp svih podataka iz DB-a (postgres pg_dump, psql):

### BCKP (pg_dump)

---

```shell
 /usr/bin/pg_dump --data-only --file=/putanja/do/dump/fajla/dump.sql --username=pma-database --host=app-61dd23fa-68f7-4bee-9f34-46e041c53f8a-do-user-10633050-0.b.db.ondigitalocean.com --port=25060
 ```

### Restore (psql)

---

```shell
 /usr/bin/psql --file=/putanja/do/dump/fajla/dump.sql --username=pma_database --host=0.0.0.0 --port=5432
 ```

---

## Change Git username and email

```shell
git config --global user.name "your_username"
git config --global user.email "your_email"
```
