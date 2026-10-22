import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://user:pass@localhost:5432/caregiver_db",
)

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database only when the users table does not exist.
    Existing database tables and records are preserved.
    """
    with engine.begin() as conn:
        table_exists = conn.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'users'
                )
            """)
        ).scalar()

        if table_exists:
            print(
                "Database schema already exists. "
                "Skipping initialization."
            )
            return

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        migration_path = os.path.join(
            project_root,
            "migrations",
            "001_init.sql",
        )

        if not os.path.isfile(migration_path):
            raise FileNotFoundError(
                f"Migration file not found: {migration_path}"
            )

        with open(migration_path, "r", encoding="utf-8") as file:
            sql = file.read()

        if not sql.strip():
            raise ValueError("The initial migration file is empty.")

        conn.execute(text(sql))

        print("Database schema initialized successfully.")
