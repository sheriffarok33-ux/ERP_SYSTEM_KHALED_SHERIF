import streamlit as st

from translations import t
from modules.dashboard import show_dashboard
from modules.companies import show_companies
from modules.ask_ai import show_ask_ai
from ui.navigation import show_navigation
from core.database import initialize_database, database_health_check


# ==========================================
# ERP SYSTEM KHALED & SHERIF
# MAIN APPLICATION
# ==========================================

st.set_page_config(
    page_title="ERP System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

try:
    initialize_database()
    database_ready = database_health_check()

except Exception as error:
    database_ready = False
    database_error = str(error)


# ==========================================
# DATABASE ERROR
# ==========================================

if not database_ready:

    st.error(
        "Database initialization failed. / فشل تشغيل قاعدة البيانات."
    )

    if "database_error" in globals():
        st.code(database_error)

    st.stop()


# ==========================================
# SESSION STATE
# ==========================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# ==========================================
# LANGUAGE
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

        if st.button(
            t("login", language),
            use_container_width=True
        ):

            # TEMPORARY LOGIN
            # Later this will be replaced with
            # database users + hashed passwords

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    t("invalid_login", language)
                )

        st.markdown("---")

        st.markdown(
            f"""
            <div style="text-align:center; font-size:13px; line-height:1.8;">
                {t("supervised_by", language)}:
                Mr. Khaled Al-Fitouri
                <br>

                {t("developed_by", language)}:
                Eng. Sherif M. Farok
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# ERP SYSTEM
# ==========================================

else:

    # ======================================
    # NAVIGATION
    # ======================================

    selected_page = show_navigation(language)


    # ======================================
    # SCREEN ROUTER
    # ======================================

    if selected_page == "dashboard":

        show_dashboard(language)

    elif selected_page == "companies_branches":

        show_companies(language)

    elif selected_page == "ask_ai":

        show_ask_ai(language)

    else:

        st.title(
            t(selected_page, language)
        )

        if language == "العربية":

            st.info(
                "هذه الشاشة قيد التطوير."
            )

        else:

            st.info(
                "This screen is under development."
            )


    # ======================================
    # SIDEBAR USER INFORMATION
    # ======================================

    with st.sidebar:

        st.divider()

        st.caption(
            f"User: {st.session_state.username}"
        )

        if st.button(
            t("logout", language),
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = None

            st.rerun()
