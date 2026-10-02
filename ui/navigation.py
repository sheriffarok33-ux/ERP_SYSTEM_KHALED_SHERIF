import streamlit as st
from translations import t


def show_navigation(language):
    ar = language == "العربية"

    with st.sidebar:
        st.title(t("system_name", language))
        st.divider()

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
            for key, icon, ar_name, en_name in menu_options
        ]

        keys = [item[0] for item in menu_options]
        key_to_label = {
            item[0]: labels[index]
            for index, item in enumerate(menu_options)
        }

        # A dashboard button writes requested_page then calls st.rerun().
        # IMPORTANT: update the RADIO WIDGET'S OWN state before creating it.
        requested_page = st.session_state.pop("requested_page", None)

        if requested_page in keys:
            st.session_state["main_navigation_radio"] = key_to_label[requested_page]

        # Make sure an old value from another language cannot break the widget.
        current_widget_value = st.session_state.get("main_navigation_radio")
        if current_widget_value not in labels:
            st.session_state["main_navigation_radio"] = key_to_label["dashboard"]

        selected = st.radio(
            "Navigation",
            labels,
            key="main_navigation_radio",
            label_visibility="collapsed"
        )

        selected_index = labels.index(selected)
        return menu_options[selected_index][0]
