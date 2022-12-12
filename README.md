# PMA project

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python](https://img.shields.io/badge/HTML%20code%20style-djhtml-orange?logo=html5)](https://github.com/rtts/djhtml)
[![Python](https://img.shields.io/badge/python-3.11.0-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/)
[![Python](https://img.shields.io/badge/no%20package%20install-only%20with%20consensus-green?logo=1001Tracklists&logoColor=yellow)](https://www.python.org/)

---

<p align="left">
  <img width="500" src="https://user-images.githubusercontent.com/4832847/206937496-6f031876-26e6-49a8-a144-19f59801c048.png" alt="Material Bread logo">
</p>




## Integracija sa Digital Ocean APP platformom

- Napravljen **STAGE server** na APP Digital Ocean platformi [Link ka APP-u](https://pma-app-k89y6.ondigitalocean.app/).
- U
  sekciji [APP / SETTINGS / DOMAIN](https://cloud.digitalocean.com/apps/8058ee2c-a1c4-420f-bb1c-534672111037/settings?i=8d2545)
  dodati domain name: **popravimojauto.com**.
- Zatim na CloudFlare dodati ponudjenu CNAME varijablu !

---

## Korisne komande:
- Ciscenje svi paketa iz PIP-a: ```pip freeze | xargs pip uninstall -y```
- Pre-Commit run: ```pre-commit run```
- HTML pre-commit: ```djhtml -i pma_apps/templates/.```

---

## Inicijalizacija svih podataka ukoliko mora da se obriše DB:
[@see reference](https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata)
- <b>Čuvanje svih podataka iz DB-a (fixtures):</b>
- - Prvo se ode u DIR: ``` tests/fixtures_from_db ```
- - Pa iz to dir-a komanda ispod:

```bash
  python ../../manage.py dumpdata --exclude auth.permission --exclude contenttypes  --indent 2 > pma-data.json
```

- <b>Učitavanje inicijalnih podataka u novu bazu:</b>
- - ``` python ../../manage.py loaddata pma-data.json ```
