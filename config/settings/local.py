from .base import *
from .base import env

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

print(f'ROOT DIR from local.py = {ROOT_DIR}')



DEBUG = env.bool("DJANGO_DEBUG", False)

