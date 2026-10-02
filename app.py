import streamlit as st
from translations import t

# ==========================================
# ERP SYSTEM KHALED & SHERIF
# Main Application
# ==========================================

st.set_page_config(
    page_title="ERP System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# SESSION STATE
# ==========================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ==========================================
# LANGUAGE SELECTOR
# ==========================================

language = st.selectbox(
    "Language / اللغة",
    ["English", "العربية"],
    index=0 if st.session_state.language == "English" else 1
)

st.session_state.language = language


# ==========================================
# LOGIN SCREEN
# ==========================================

if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1.5, 2, 1.5])

    with center:

        st.markdown(
            f"<h1 style='text-align:center;'>{t('system_name', language)}</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<h4 style='text-align:center;'>{t('system_description', language)}</h4>",
            unsafe_allow_html=True
        )

        username = st.text_input(
            t("username", language)
        )

        password = st.text_input(
            t("password", language),
            type="password"
        )

        login_button = st.button(
            t("login", language),
            use_container_width=True
        )

        if login_button:

            # TEMPORARY LOGIN FOR DEVELOPMENT ONLY
            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error(
                    t("invalid_login", language)
                )

        st.markdown("---")

        st.markdown(
            f"""
            <div style="text-align:center; font-size:13px;">
                {t("supervised_by", language)}: Mr. Khaled Al-Fitouri
                <br>
                {t("developed_by", language)}: Eng. Sherif M. Farok
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# MAIN ERP DASHBOARD
# ==========================================

else:

    st.title(
        t("system_name", language)
    )

    st.success(
        t("login_success", language)
    )

    st.subheader(
        t("dashboard", language)
    )

    st.divider()

    # --------------------------
    # MAIN MODULES - ROW 1
    # --------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "🏢 " + t("companies_branches", language)
        )

    with col2:
        st.info(
            "📦 " + t("inventory_warehouses", language)
        )

    with col3:
        st.info(
            "💰 " + t("finance_accounting", language)
        )

    # --------------------------
    # MAIN MODULES - ROW 2
    # --------------------------

    col4, col5, col6 = st.columns(3)

    with col4:
        st.info(
            "🛒 " + t("sales", language)
        )

    with col5:
        st.info(
            "🧾 " + t("purchasing", language)
        )

    with col6:
        st.info(
            "🏪 " + t("pos", language)
        )

    # --------------------------
    # MAIN MODULES - ROW 3
    # --------------------------

    col7, col8, col9 = st.columns(3)

    with col7:
        st.info(
            "🏭 " + t("manufacturing", language)
        )

    with col8:
        st.info(
            "🚢 " + t("import_export", language)
        )

    with col9:
        st.info(
            "👥 " + t("crm", language)
        )

    # --------------------------
    # MAIN MODULES - ROW 4
    # --------------------------

    col10, col11, col12 = st.columns(3)

    with col10:
        st.info(
            "🏷️ " + t("assets", language)
        )

    with col11:
        st.info(
            "👨‍💼 " + t("hr_payroll", language)
        )

    with col12:
        st.info(
            "🤝 " + t("partners_equity", language)
        )

    # --------------------------
    # ADMINISTRATION
    # --------------------------

    st.divider()

    col13, col14, col15 = st.columns(3)

    with col13:
        st.info(
            "📊 " + t("reports", language)
        )

    with col14:
        st.info(
            "🔐 " + t("users_permissions", language)
        )

    with col15:
        st.info(
            "⚙️ " + t("settings", language)
        )

    st.divider()

    # --------------------------
    # LOGOUT
    # --------------------------

    if st.button(
        t("logout", language)
    ):
        st.session_state.logged_in = False
        st.rerun()
