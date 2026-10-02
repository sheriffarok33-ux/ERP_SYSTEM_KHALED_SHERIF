import os
import sqlite3
from contextlib import contextmanager


# ============================================================
# ERP SYSTEM KHALED & SHERIF
# DATABASE CORE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

LOCAL_DATABASE_PATH = os.path.join(
    DATA_DIR,
    "erp_local.db"
)


# ============================================================
# DATABASE MODE
# ============================================================

DATABASE_MODE = os.getenv(
    "ERP_DATABASE_MODE",
    "local"
).lower()


# ============================================================
# LOCAL DATABASE CONNECTION
# SQLite
# ============================================================

def get_local_connection():

    connection = sqlite3.connect(
        LOCAL_DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


# ============================================================
# DATABASE CONTEXT MANAGER
# ============================================================

@contextmanager
def local_database():

    connection = get_local_connection()

    try:

        yield connection

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    with local_database() as db:

        # ----------------------------------------------------
        # COMPANIES
        # ----------------------------------------------------

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                company_uuid TEXT UNIQUE,

                company_code TEXT NOT NULL UNIQUE,

                name_ar TEXT,
                name_en TEXT,

                legal_name_ar TEXT,
                legal_name_en TEXT,

                commercial_registration_no TEXT,
                tax_number TEXT,

                base_currency TEXT NOT NULL DEFAULT 'LYD',

                fiscal_year_start_month INTEGER
                    NOT NULL DEFAULT 1,

                country TEXT,
                city TEXT,

                phone TEXT,
                email TEXT,
                website TEXT,

                address_ar TEXT,
                address_en TEXT,

                logo_path TEXT,

                status TEXT
                    NOT NULL DEFAULT 'active',

                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                created_by TEXT,

                updated_by TEXT,

                sync_status TEXT
                    NOT NULL DEFAULT 'pending',

                last_synced_at TEXT,

                is_deleted INTEGER
                    NOT NULL DEFAULT 0

            );
            """
        )

        # ----------------------------------------------------
        # BRANCHES
        # ----------------------------------------------------

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS branches (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                branch_uuid TEXT UNIQUE,

                company_id INTEGER NOT NULL,

                branch_code TEXT NOT NULL,

                name_ar TEXT,
                name_en TEXT,

                country TEXT,
                city TEXT,

                address_ar TEXT,
                address_en TEXT,

                phone TEXT,
                email TEXT,

                status TEXT
                    NOT NULL DEFAULT 'active',

                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                sync_status TEXT
                    NOT NULL DEFAULT 'pending',

                last_synced_at TEXT,

                is_deleted INTEGER
                    NOT NULL DEFAULT 0,

                FOREIGN KEY (company_id)
                    REFERENCES companies(id),

                UNIQUE(company_id, branch_code)

            );
            """
        )

        # ----------------------------------------------------
        # DOCUMENT SEQUENCES
        # ----------------------------------------------------

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS document_sequences (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                company_id INTEGER NOT NULL,

                branch_id INTEGER,

                document_type TEXT NOT NULL,

                prefix TEXT,

                current_number INTEGER
                    NOT NULL DEFAULT 0,

                padding INTEGER
                    NOT NULL DEFAULT 6,

                fiscal_year INTEGER,

                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (company_id)
                    REFERENCES companies(id),

                FOREIGN KEY (branch_id)
                    REFERENCES branches(id)

            );
            """
        )

        # ----------------------------------------------------
        # SYNC QUEUE
        # ----------------------------------------------------

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_queue (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                record_uuid TEXT NOT NULL,

                table_name TEXT NOT NULL,

                operation TEXT NOT NULL,

                payload TEXT,

                created_at TEXT
                    NOT NULL DEFAULT CURRENT_TIMESTAMP,

                synced INTEGER
                    NOT NULL DEFAULT 0,

                synced_at TEXT,

                retry_count INTEGER
                    NOT NULL DEFAULT 0,

                error_message TEXT

            );
            """
        )


# ============================================================
# HEALTH CHECK
# ============================================================

def database_health_check():

    try:

        with local_database() as db:

            result = db.execute(
                "SELECT 1"
            ).fetchone()

            return result[0] == 1

    except Exception:

        return False
