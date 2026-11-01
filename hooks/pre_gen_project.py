import re
import sys

SLUG = '{{ cookiecutter.project_slug }}'
SCHEMA = '{{ cookiecutter.db_schema }}'

if not re.fullmatch(r'[a-z][a-z0-9-]*', SLUG):
    print(f'Ошибка: слаг {SLUG!r} должен начинаться с буквы и содержать только a-z, 0-9 и "-".')
    sys.exit(1)

if not re.fullmatch(r'[a-z_][a-z0-9_]*', SCHEMA):
    print(f'Ошибка: схема {SCHEMA!r} должна быть идентификатором Postgres (a-z, 0-9, "_").')
    sys.exit(1)
