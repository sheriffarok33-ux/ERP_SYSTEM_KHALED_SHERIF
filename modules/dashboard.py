import streamlit as st
from translations import t


def _go_to(page_key):
    """
    Store the requested page so navigation.py can consume it.
    """
    st.session_state["requested_page"] = page_key
    st.rerun()


def _module_button(label, icon, page_key, key):
    """
    Dashboard module button.
    """
    if st.button(
        f"{icon}  {label}",
        key=key,
        use_container_width=True
    ):
        _go_to(page_key)


def show_dashboard(language):

    st.title(t("system_name", language))
    st.success(t("login_success", language))
    st.subheader(t("dashboard", language))

    # Center the text/icons inside all dashboard buttons.
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            min-height: 84px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 20px;
            font-weight: 600;
            border-radius: 12px;
            white-space: normal;
        }

        div[data-testid="stButton"] > button p {
            width: 100%;
            text-align: center;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ==========================================
    # MAIN ERP MODULES
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:
        _module_button(
            t("companies_branches", language),
            "🏢",
            "companies_branches",
            "dash_companies"
        )

    with col2:
        _module_button(
            t("inventory_warehouses", language),
            "📦",
            "inventory",
            "dash_inventory"
        )

    with col3:
        _module_button(
            t("finance_accounting", language),
            "💰",
            "accounting",
            "dash_accounting"
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        _module_button(
            t("sales", language),
            "🛒",
            "sales",
            "dash_sales"
        )

    with col5:
        _module_button(
            t("purchasing", language),
            "🧾",
            "purchasing",
            "dash_purchasing"
        )

    with col6:
        _module_button(
            t("pos", language),
            "🏪",
            "pos",
            "dash_pos"
        )

    col7, col8, col9 = st.columns(3)

    with col7:
        _module_button(
            t("manufacturing", language),
            "🏭",
            "manufacturing",
            "dash_manufacturing"
        )

    with col8:
        _module_button(
            t("import_export", language),
            "🚢",
            "import_export",
            "dash_import_export"
        )

    with col9:
        _module_button(
            t("crm", language),
            "👥",
            "crm",
            "dash_crm"
        )

    col10, col11, col12 = st.columns(3)

    with col10:
        _module_button(
            t("assets", language),
            "🏷️",
            "assets",
            "dash_assets"
        )

    with col11:
        _module_button(
            t("hr_payroll", language),
            "👨‍💼",
            "hr",
            "dash_hr"
        )

    with col12:
        _module_button(
            t("partners_equity", language),
            "🤝",
            "partners",
            "dash_partners"
        )

    # ==========================================
    # ADMINISTRATION
    # ==========================================

    st.divider()

    col13, col14, col15 = st.columns(3)

    with col13:
        _module_button(
            t("reports", language),
            "📊",
            "reports",
            "dash_reports"
        )

    with col14:
        _module_button(
            t("users_permissions", language),
            "🔐",
            "users",
            "dash_users"
        )

    with col15:
        _module_button(
            t("settings", language),
            "⚙️",
            "settings",
            "dash_settings"
        )
