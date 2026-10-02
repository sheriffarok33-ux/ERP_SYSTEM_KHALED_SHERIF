import streamlit as st

from translations import t
from modules.dashboard import show_dashboard
from modules.companies import show_companies
from modules.branches import show_branches
from modules.warehouses import show_warehouses
from modules.fiscal_years import show_fiscal_years
from modules.currencies import show_currencies
from modules.cost_centers import show_cost_centers
from modules.crm import show_crm
from modules.inventory import show_inventory
from modules.purchases import show_purchases
from modules.sales import show_sales
from modules.pos import show_pos
from modules.accounting import show_accounting
from modules.manufacturing import show_manufacturing
from modules.import_export import show_import_export
from modules.assets import show_assets
from modules.hr import show_hr
from modules.partners import show_partners
from modules.reports import show_reports
from modules.ask_ai import show_ask_ai
from modules.users import show_users
from modules.settings import show_settings
from ui.navigation import show_navigation
from core.database import initialize_database, database_health_check

st.set_page_config(page_title="ERP System", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

try:
    initialize_database()
    database_ready = database_health_check()
except Exception as error:
    database_ready = False
    database_error = str(error)

if not database_ready:
    st.error("Database initialization failed. / فشل تشغيل قاعدة البيانات.")
    if "database_error" in globals():
        st.code(database_error)
    st.stop()

if "language" not in st.session_state:
    st.session_state.language = "English"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

language = st.selectbox(
    "Language / اللغة", ["English", "العربية"],
    index=0 if st.session_state.language == "English" else 1
)
st.session_state.language = language

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    left, center, right = st.columns([1.5, 2, 1.5])
    with center:
        st.markdown(f"<h1 style='text-align:center;'>{t('system_name', language)}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align:center;'>{t('system_description', language)}</h4>", unsafe_allow_html=True)
        username = st.text_input(t("username", language))
        password = st.text_input(t("password", language), type="password")
        if st.button(t("login", language), use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error(t("invalid_login", language))
        st.markdown("---")
        st.markdown(
            f"""<div style="text-align:center; font-size:13px; line-height:1.8;">
            {t("supervised_by", language)}: Mr. Khaled Al-Fitouri<br>
            {t("developed_by", language)}: Eng. Sherif M. Farok
            </div>""",
            unsafe_allow_html=True
        )
else:
    selected_page = show_navigation(language)

    routes = {
        "dashboard": show_dashboard,
        "companies_branches": show_companies,
        "branches": show_branches,
        "warehouses": show_warehouses,
        "fiscal_years": show_fiscal_years,
        "currencies": show_currencies,
        "cost_centers": show_cost_centers,
        "crm": show_crm,
        "inventory": show_inventory,
        "purchasing": show_purchases,
        "sales": show_sales,
        "pos": show_pos,
        "accounting": show_accounting,
        "manufacturing": show_manufacturing,
        "import_export": show_import_export,
        "assets": show_assets,
        "hr": show_hr,
        "partners": show_partners,
        "reports": show_reports,
        "ask_ai": show_ask_ai,
        "users": show_users,
        "settings": show_settings,
    }

    screen = routes.get(selected_page)
    if screen:
        screen(language)
    else:
        st.error("Unknown screen / شاشة غير معروفة")

    with st.sidebar:
        st.divider()
        st.caption(f"User: {st.session_state.username}")
        if st.button(t("logout", language), use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
