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
        # WAREHOUSES
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS warehouses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                warehouse_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER NOT NULL,
                warehouse_code TEXT NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                warehouse_type TEXT NOT NULL DEFAULT 'general',
                country TEXT,
                city TEXT,
                address_ar TEXT,
                address_en TEXT,
                phone TEXT,
                manager_name TEXT,
                allow_negative_stock INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                updated_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                last_synced_at TEXT,
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                UNIQUE(company_id, branch_id, warehouse_code)
            );
        """)

        # ----------------------------------------------------
        # FISCAL YEARS / PERIODS
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS fiscal_years (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fiscal_year_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                year_code TEXT NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                is_current INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                updated_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                UNIQUE(company_id, year_code)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS accounting_periods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period_uuid TEXT UNIQUE,
                fiscal_year_id INTEGER NOT NULL,
                period_no INTEGER NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                closed_at TEXT,
                closed_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (fiscal_year_id) REFERENCES fiscal_years(id),
                UNIQUE(fiscal_year_id, period_no)
            );
        """)

        # ----------------------------------------------------
        # CURRENCIES / EXCHANGE RATES
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code TEXT NOT NULL UNIQUE,
                name_ar TEXT,
                name_en TEXT,
                symbol TEXT,
                decimal_places INTEGER NOT NULL DEFAULT 3,
                status TEXT NOT NULL DEFAULT 'active'
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                rate_date TEXT NOT NULL,
                rate REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (currency_id) REFERENCES currencies(id),
                UNIQUE(company_id, currency_id, rate_date)
            );
        """)

        # ----------------------------------------------------
        # COST CENTERS
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS cost_centers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cost_center_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER,
                parent_id INTEGER,
                center_code TEXT NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                FOREIGN KEY (parent_id) REFERENCES cost_centers(id),
                UNIQUE(company_id, center_code)
            );
        """)

        # ----------------------------------------------------
        # BUSINESS PARTIES: CUSTOMERS / SUPPLIERS
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS business_parties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                party_code TEXT NOT NULL,
                party_type TEXT NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                phone TEXT,
                email TEXT,
                tax_number TEXT,
                address TEXT,
                credit_limit REAL NOT NULL DEFAULT 0,
                opening_balance REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                UNIQUE(company_id, party_code)
            );
        """)

        # ----------------------------------------------------
        # ITEMS / INVENTORY
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                item_code TEXT NOT NULL,
                barcode TEXT,
                name_ar TEXT,
                name_en TEXT,
                category TEXT,
                unit TEXT,
                purchase_cost REAL NOT NULL DEFAULT 0,
                average_cost REAL NOT NULL DEFAULT 0,
                sale_price REAL NOT NULL DEFAULT 0,
                reorder_level REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                is_deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                UNIQUE(company_id, item_code)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS inventory_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movement_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER,
                warehouse_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit_cost REAL NOT NULL DEFAULT 0,
                reference_type TEXT,
                reference_id INTEGER,
                movement_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        """)

        # ----------------------------------------------------
        # PURCHASE INVOICES
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS purchase_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER,
                warehouse_id INTEGER,
                supplier_id INTEGER,
                internal_number TEXT NOT NULL,
                supplier_invoice_number TEXT,
                invoice_date TEXT NOT NULL,
                currency_code TEXT NOT NULL DEFAULT 'LYD',
                exchange_rate REAL NOT NULL DEFAULT 1,
                subtotal REAL NOT NULL DEFAULT 0,
                discount_total REAL NOT NULL DEFAULT 0,
                tax_total REAL NOT NULL DEFAULT 0,
                grand_total REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'draft',
                attachment_name TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                approved_at TEXT,
                approved_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
                FOREIGN KEY (supplier_id) REFERENCES business_parties(id),
                UNIQUE(company_id, internal_number)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS purchase_invoice_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity REAL NOT NULL DEFAULT 0,
                unit_cost REAL NOT NULL DEFAULT 0,
                discount REAL NOT NULL DEFAULT 0,
                tax REAL NOT NULL DEFAULT 0,
                line_total REAL NOT NULL DEFAULT 0,
                previous_cost REAL,
                cost_change_percent REAL,
                FOREIGN KEY (invoice_id) REFERENCES purchase_invoices(id) ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        """)

        # ----------------------------------------------------
        # PRICE CHANGE APPROVAL WORKFLOW
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS price_change_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                purchase_invoice_id INTEGER,
                item_id INTEGER NOT NULL,
                old_cost REAL NOT NULL DEFAULT 0,
                new_cost REAL NOT NULL DEFAULT 0,
                cost_change_percent REAL NOT NULL DEFAULT 0,
                old_sale_price REAL NOT NULL DEFAULT 0,
                target_margin_percent REAL NOT NULL DEFAULT 0,
                suggested_sale_price REAL NOT NULL DEFAULT 0,
                approved_sale_price REAL,
                status TEXT NOT NULL DEFAULT 'pending',
                requested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                requested_by TEXT,
                reviewed_at TEXT,
                reviewed_by TEXT,
                review_note TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (purchase_invoice_id) REFERENCES purchase_invoices(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS item_price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                old_price REAL NOT NULL,
                new_price REAL NOT NULL,
                reason TEXT,
                source_request_id INTEGER,
                changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                changed_by TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (item_id) REFERENCES items(id),
                FOREIGN KEY (source_request_id) REFERENCES price_change_requests(id)
            );
        """)

        # ----------------------------------------------------
        # SALES
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS sales_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER,
                warehouse_id INTEGER,
                customer_id INTEGER,
                invoice_number TEXT NOT NULL,
                invoice_date TEXT NOT NULL,
                subtotal REAL NOT NULL DEFAULT 0,
                discount_total REAL NOT NULL DEFAULT 0,
                tax_total REAL NOT NULL DEFAULT 0,
                grand_total REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'draft',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
                FOREIGN KEY (customer_id) REFERENCES business_parties(id),
                UNIQUE(company_id, invoice_number)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS sales_invoice_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity REAL NOT NULL DEFAULT 0,
                unit_price REAL NOT NULL DEFAULT 0,
                discount REAL NOT NULL DEFAULT 0,
                tax REAL NOT NULL DEFAULT 0,
                line_total REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (invoice_id) REFERENCES sales_invoices(id) ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES items(id)
            );
        """)

        # ----------------------------------------------------
        # ACCOUNTING
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                parent_id INTEGER,
                account_code TEXT NOT NULL,
                name_ar TEXT,
                name_en TEXT,
                account_type TEXT NOT NULL,
                allow_posting INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'active',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (parent_id) REFERENCES accounts(id),
                UNIQUE(company_id, account_code)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_uuid TEXT UNIQUE,
                company_id INTEGER NOT NULL,
                branch_id INTEGER,
                entry_number TEXT NOT NULL,
                entry_date TEXT NOT NULL,
                reference_type TEXT,
                reference_id INTEGER,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                posted_at TEXT,
                posted_by TEXT,
                sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id),
                UNIQUE(company_id, entry_number)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS journal_entry_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                journal_entry_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                cost_center_id INTEGER,
                description TEXT,
                debit REAL NOT NULL DEFAULT 0,
                credit REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (journal_entry_id) REFERENCES journal_entries(id) ON DELETE CASCADE,
                FOREIGN KEY (account_id) REFERENCES accounts(id),
                FOREIGN KEY (cost_center_id) REFERENCES cost_centers(id)
            );
        """)

        # ----------------------------------------------------
        # USERS / ROLES / USER APPEARANCE
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS app_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_uuid TEXT UNIQUE,
                username TEXT NOT NULL UNIQUE,
                full_name TEXT,
                password_hash TEXT,
                role_name TEXT,
                company_id INTEGER,
                branch_id INTEGER,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                FOREIGN KEY (branch_id) REFERENCES branches(id)
            );
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                language TEXT NOT NULL DEFAULT 'English',
                primary_color TEXT NOT NULL DEFAULT '#0B66C3',
                button_color TEXT NOT NULL DEFAULT '#E7F1FD',
                background_color TEXT NOT NULL DEFAULT '#FFFFFF',
                sidebar_color TEXT NOT NULL DEFAULT '#F5F7FA',
                text_color TEXT NOT NULL DEFAULT '#1F2937',
                font_family TEXT NOT NULL DEFAULT 'Arial',
                font_size INTEGER NOT NULL DEFAULT 16,
                theme_mode TEXT NOT NULL DEFAULT 'light',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # ----------------------------------------------------
        # AUDIT LOG
        # ----------------------------------------------------
        db.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT NOT NULL,
                table_name TEXT,
                record_id TEXT,
                old_values TEXT,
                new_values TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)


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
