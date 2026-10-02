import streamlit as st
from translations import t


def show_navigation(language):

    with st.sidebar:

        st.title(t("system_name", language))

        st.divider()

        menu_options = [
            ("dashboard", "🏠"),
            ("companies_branches", "🏢"),
            ("crm", "👥"),
            ("sales", "🛒"),
            ("pos", "🏪"),
            ("purchasing", "🧾"),
            ("inventory_warehouses", "📦"),
            ("manufacturing", "🏭"),
            ("import_export", "🚢"),
            ("finance_accounting", "💰"),
            ("assets", "🏷️"),
            ("hr_payroll", "👨‍💼"),
            ("partners_equity", "🤝"),
            ("reports", "📊"),
            ("ask_ai", "🤖"),
            ("users_permissions", "🔐"),
            ("settings", "⚙️"),
        ]

        labels = []

        for key, icon in menu_options:

            if key == "ask_ai":

                label = (
                    "اسأل الذكاء الاصطناعي"
                    if language == "العربية"
                    else "Ask AI"
                )

            else:

                label = t(key, language)

            labels.append(
                f"{icon} {label}"
            )

        selected_label = st.radio(
            "Navigation",
            labels,
            label_visibility="collapsed"
        )

        selected_index = labels.index(
            selected_label
        )

        selected_page = menu_options[
            selected_index
        ][0]

        return selected_page
