import os
import sys

REMOVE_PATHS = [
    '{% if cookiecutter.use_postgres != "y" -%} ./backend/alembic.ini {% endif %}',
    '{% if cookiecutter.use_postgres != "y" -%} ./backend/src/db {% endif %}',
    '{% if cookiecutter.use_redis != "y" -%} ./backend/src/config/cache.py {% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.unlink(path)
