import streamlit as st

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

# -----------------------------
# Session State
# -----------------------------
if "language" not in st.session_state:
    st.session_state.language = "English"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------------
# Language
# -----------------------------
language = st.selectbox(
    "Language / اللغة",
    ["English", "العربية"],
    index=0 if st.session_state.language == "English" else 1
)

st.session_state.language = language


# -----------------------------
# Login Screen
# -----------------------------
if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1.5, 2, 1.5])

    with col_center:

        st.markdown(
            "<h1 style='text-align:center;'>ERP SYSTEM</h1>",
            unsafe_allow_html=True
        )

        if language == "العربية":
            st.markdown(
                "<h4 style='text-align:center;'>نظام تخطيط موارد المؤسسات</h4>",
                unsafe_allow_html=True
            )

            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")

            login_button = st.button(
                "تسجيل الدخول",
                use_container_width=True
            )

        else:
            st.markdown(
                "<h4 style='text-align:center;'>Enterprise Resource Planning System</h4>",
                unsafe_allow_html=True
            )

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            login_button = st.button(
                "Login",
                use_container_width=True
            )

        if login_button:

            # Temporary development login
            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.rerun()

            else:

                if language == "العربية":
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    st.error("Invalid username or password")

        st.markdown("---")

        st.markdown(
            """
            <div style="text-align:center; font-size:13px;">
                Supervised by: Mr. Khaled Al-Fitouri<br>
                Developed by: Eng. Sherif M. Farok
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# Main ERP Dashboard
# -----------------------------
else:

    if language == "العربية":
        st.title("نظام ERP")
        st.success("تم تسجيل الدخول بنجاح")
    else:
        st.title("ERP SYSTEM")
        st.success("Login successful")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🏢 Companies & Branches")

    with col2:
        st.info("📦 Inventory & Warehouses")

    with col3:
        st.info("💰 Finance & Accounting")

    st.divider()

    if st.button("Logout / تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
