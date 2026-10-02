import streamlit as st
from translations import t


def show_dashboard(language):

    st.title(t("system_name", language))
    st.success(t("login_success", language))
    st.subheader(t("dashboard", language))

    st.divider()

    # ==========================================
    # MAIN ERP MODULES
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🏢 " + t("companies_branches", language))

    with col2:
        st.info("📦 " + t("inventory_warehouses", language))

    with col3:
        st.info("💰 " + t("finance_accounting", language))

    col4, col5, col6 = st.columns(3)

    with col4:
        st.info("🛒 " + t("sales", language))

    with col5:
        st.info("🧾 " + t("purchasing", language))

    with col6:
        st.info("🏪 " + t("pos", language))

    col7, col8, col9 = st.columns(3)

    with col7:
        st.info("🏭 " + t("manufacturing", language))

    with col8:
        st.info("🚢 " + t("import_export", language))

    with col9:
        st.info("👥 " + t("crm", language))

    col10, col11, col12 = st.columns(3)

    with col10:
        st.info("🏷️ " + t("assets", language))

    with col11:
        st.info("👨‍💼 " + t("hr_payroll", language))

    with col12:
        st.info("🤝 " + t("partners_equity", language))

    # ==========================================
    # ADMINISTRATION
    # ==========================================

    st.divider()

    col13, col14, col15 = st.columns(3)

    with col13:
        st.info("📊 " + t("reports", language))

    with col14:
        st.info("🔐 " + t("users_permissions", language))

    with col15:
        st.info("⚙️ " + t("settings", language))
