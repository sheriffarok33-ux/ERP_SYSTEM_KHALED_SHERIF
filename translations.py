# ==========================================
# ERP SYSTEM KHALED & SHERIF
# Central Translation Dictionary
# Arabic / English
# ==========================================

TRANSLATIONS = {

    "English": {
        "system_name": "ERP SYSTEM",
        "system_description": "Enterprise Resource Planning System",

        "language": "Language",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "logout": "Logout",

        "login_success": "Login successful",
        "invalid_login": "Invalid username or password",

        "dashboard": "Dashboard",

        "companies_branches": "Companies & Branches",
        "inventory_warehouses": "Inventory & Warehouses",
        "finance_accounting": "Finance & Accounting",

        "sales": "Sales",
        "purchasing": "Purchasing",
        "pos": "Point of Sale",
        "crm": "CRM",

        "manufacturing": "Manufacturing",
        "import_export": "Import & Export",

        "assets": "Assets",
        "hr_payroll": "HR & Payroll",

        "partners_equity": "Partners & Equity",
        "reports": "Reports",

        "users_permissions": "Users & Permissions",
        "settings": "Settings",
        "appearance": "Appearance",

        "company": "Company",
        "branch": "Branch",
        "warehouse": "Warehouse",

        "customers": "Customers",
        "suppliers": "Suppliers",

        "cash_receipt": "Cash Receipt",
        "cash_payment": "Cash Payment",

        "sales_invoice": "Sales Invoice",
        "purchase_invoice": "Purchase Invoice",

        "fiscal_year": "Fiscal Year",
        "cost_centers": "Cost Centers",

        "currency": "Currency",
        "currencies": "Currencies",

        "audit_log": "Audit Log",

        "supervised_by": "Supervised by",
        "developed_by": "Developed by"
    },

    "العربية": {
        "system_name": "نظام ERP",
        "system_description": "نظام تخطيط موارد المؤسسات",

        "language": "اللغة",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "logout": "تسجيل الخروج",

        "login_success": "تم تسجيل الدخول بنجاح",
        "invalid_login": "اسم المستخدم أو كلمة المرور غير صحيحة",

        "dashboard": "لوحة التحكم",

        "companies_branches": "الشركات والفروع",
        "inventory_warehouses": "المخزون والمخازن",
        "finance_accounting": "المالية والمحاسبة",

        "sales": "المبيعات",
        "purchasing": "المشتريات",
        "pos": "نقاط البيع",
        "crm": "إدارة علاقات العملاء",

        "manufacturing": "التصنيع",
        "import_export": "الاستيراد والتصدير",

        "assets": "الأصول",
        "hr_payroll": "الموارد البشرية والرواتب",

        "partners_equity": "الشركاء وحقوق الملكية",
        "reports": "التقارير",

        "users_permissions": "المستخدمون والصلاحيات",
        "settings": "الإعدادات",
        "appearance": "مظهر البرنامج",

        "company": "الشركة",
        "branch": "الفرع",
        "warehouse": "المخزن",

        "customers": "العملاء",
        "suppliers": "الموردون",

        "cash_receipt": "سند قبض",
        "cash_payment": "سند صرف",

        "sales_invoice": "فاتورة مبيعات",
        "purchase_invoice": "فاتورة مشتريات",

        "fiscal_year": "السنة المالية",
        "cost_centers": "مراكز التكلفة",

        "currency": "العملة",
        "currencies": "العملات",

        "audit_log": "سجل العمليات",

        "supervised_by": "إشراف",
        "developed_by": "تنفيذ"
    }
}


def t(key, language="English"):
    """
    Returns the translated text for the selected language.
    If the key does not exist, the key itself is returned.
    """
    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["English"]
    ).get(key, key)
