# Alembic Placeholder

This project currently uses automatic SQLAlchemy table creation on startup.

If you want migration-based workflows:
1. `pip install alembic`
2. `alembic init alembic`
3. Configure `alembic.ini` and `env.py` to use `app.database.Base.metadata`
4. Generate revisions with `alembic revision --autogenerate -m "init"`
5. Apply with `alembic upgrade head`
