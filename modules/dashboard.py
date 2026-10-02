import streamlit as st
from translations import t


def _request_page(page_key):
    st.session_state["requested_page"] = page_key


def _card(label, icon, page_key, key):
    st.button(
        f"{icon}  {label}",
        key=key,
        use_container_width=True,
        on_click=_request_page,
        args=(page_key,)
    )


def show_dashboard(language):
    ar = language == "العربية"

    st.title(t("system_name", language))
    st.success(t("login_success", language))
    st.subheader(t("dashboard", language))

    # Dashboard card styling: true center horizontally + vertically.
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] {
            width: 100%;
        }

        div[data-testid="stButton"] > button,
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-primary"] {
            width: 100% !important;
            min-height: 84px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            border-radius: 12px !important;
        }

        div[data-testid="stButton"] > button > div,
        div[data-testid="stButton"] > button p,
        button[data-testid="stBaseButton-secondary"] p,
        button[data-testid="stBaseButton-primary"] p {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            font-size: 20px !important;
            font-weight: 600 !important;
            line-height: 1.5 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    cards = [
        ("🏢", t("companies_branches", language), "companies_branches"),
        ("📦", t("inventory_warehouses", language), "inventory"),
        ("💰", t("finance_accounting", language), "accounting"),
        ("🛒", t("sales", language), "sales"),
        ("🧾", t("purchasing", language), "purchasing"),
        ("🏪", t("pos", language), "pos"),
        ("🏭", t("manufacturing", language), "manufacturing"),
        ("🚢", t("import_export", language), "import_export"),
        ("👥", t("crm", language), "crm"),
        ("🏷️", t("assets", language), "assets"),
        ("👨‍💼", t("hr_payroll", language), "hr"),
        ("🤝", t("partners_equity", language), "partners"),
    ]

    for row in range(0, len(cards), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row + i
            if idx < len(cards):
                icon, label, page = cards[idx]
                with col:
                    _card(label, icon, page, f"dashboard_{page}")

    st.divider()

    admin_cards = [
        ("📊", t("reports", language), "reports"),
        ("🔐", t("users_permissions", language), "users"),
        ("⚙️", t("settings", language), "settings"),
    ]

    cols = st.columns(3)
    for col, (icon, label, page) in zip(cols, admin_cards):
        with col:
            _card(label, icon, page, f"dashboard_{page}")
