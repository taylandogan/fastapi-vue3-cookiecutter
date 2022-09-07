# Import all the models, so that Base has them before being imported by Alembic
from db.base_class import BaseSchema  # noqa: F401
