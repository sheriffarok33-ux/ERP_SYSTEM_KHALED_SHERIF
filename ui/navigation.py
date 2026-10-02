import streamlit as st
from translations import t


def show_navigation(language):
    ar = language == "العربية"

    menu_options = [
        ("dashboard", "🏠", "لوحة التحكم", "Dashboard"),
        ("companies_branches", "🏢", "الشركات", "Companies"),
        ("branches", "🏢", "الفروع", "Branches"),
        ("warehouses", "🏬", "المخازن", "Warehouses"),
        ("fiscal_years", "📅", "السنوات والفترات المالية", "Fiscal Years & Periods"),
        ("currencies", "💱", "العملات وأسعار الصرف", "Currencies & Exchange Rates"),
        ("cost_centers", "🎯", "مراكز التكلفة", "Cost Centers"),
        ("crm", "👥", "العملاء والموردون", "CRM"),
        ("inventory", "📦", "الأصناف والمخزون", "Inventory"),
        ("purchasing", "🧾", "المشتريات", "Purchasing"),
        ("sales", "🛒", "المبيعات", "Sales"),
        ("pos", "🏪", "نقاط البيع", "POS"),
        ("accounting", "💰", "المالية والحسابات", "Finance & Accounting"),
        ("manufacturing", "🏭", "التصنيع", "Manufacturing"),
        ("import_export", "🚢", "الاستيراد والتصدير", "Import & Export"),
        ("assets", "🏷️", "الأصول", "Assets"),
        ("hr", "👨‍💼", "الموارد البشرية والرواتب", "HR & Payroll"),
        ("partners", "🤝", "الشركاء وحقوق الملكية", "Partners & Equity"),
        ("reports", "📊", "التقارير", "Reports"),
        ("ask_ai", "🤖", "اسأل الذكاء الاصطناعي", "Ask AI"),
        ("users", "🔐", "المستخدمون والصلاحيات", "Users & Permissions"),
        ("settings", "⚙️", "الإعدادات", "Settings"),
    ]

    labels = [
        f"{icon} {ar_name if ar else en_name}"
        for _, icon, ar_name, en_name in menu_options
    ]
    keys = [item[0] for item in menu_options]
    page_to_label = dict(zip(keys, labels))

    # Consume any click coming from the dashboard BEFORE the radio is created.
    requested = st.session_state.pop("requested_page", None)
    if requested in page_to_label:
        st.session_state["erp_navigation"] = page_to_label[requested]

    # Protect against changing Arabic/English while a previous label is stored.
    if st.session_state.get("erp_navigation") not in labels:
        st.session_state["erp_navigation"] = page_to_label["dashboard"]

    with st.sidebar:
        st.title(t("system_name", language))
        st.divider()

        selected_label = st.radio(
            "Navigation",
            labels,
            key="erp_navigation",
            label_visibility="collapsed"
        )

    return menu_options[labels.index(selected_label)][0]
