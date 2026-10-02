import streamlit as st

from translations import t
from modules.dashboard import show_dashboard


# ==========================================
# ERP SYSTEM KHALED & SHERIF
# MAIN APPLICATION
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
            f"""
            <h1 style="text-align:center;">
                {t("system_name", language)}
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h4 style="text-align:center;">
                {t("system_description", language)}
            </h4>
            """,
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

            # ==================================
            # TEMPORARY DEVELOPMENT LOGIN
            # Will be replaced by database users
            # ==================================

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
            <div style="
                text-align:center;
                font-size:13px;
                line-height:1.8;
            ">
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

    # --------------------------------------
    # Load Dashboard
    # --------------------------------------

    show_dashboard(language)

    st.divider()

    # --------------------------------------
    # Logout
    # --------------------------------------

    if st.button(
        t("logout", language)
    ):

        st.session_state.logged_in = False

        if "username" in st.session_state:
            del st.session_state.username

        st.rerun()
