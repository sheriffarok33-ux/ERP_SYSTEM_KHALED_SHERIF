import streamlit as st

st.set_page_config(
    page_title="ERP System Khaled & Sherif",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ERP SYSTEM - MAIN APP
# =========================

st.title("ERP SYSTEM")
st.subheader("Integrated Enterprise Resource Planning System")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🏢 Companies & Branches")

with col2:
    st.info("📦 Inventory & Warehouses")

with col3:
    st.info("💰 Finance & Accounting")

st.write("")
st.write("### System Status")
st.success("ERP Core Foundation - Development Started")

st.divider()

st.caption("Supervised by: Mr. Khaled Al-Fitouri")
st.caption("Developed by: Eng. Sherif M. Farok")
