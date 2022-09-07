{% if cookiecutter.use_postgres == 'y' -%}
from db.database import SessionLocal


class DBSessionContextManager:
    def __init__(self):
        self.db_session = SessionLocal()

    def __enter__(self):
        return self.db_session

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_session.close()
{%- endif %}