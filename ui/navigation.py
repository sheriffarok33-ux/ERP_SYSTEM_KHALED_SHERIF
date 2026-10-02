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

        labels = [f"{icon} {ar_name if ar else en_name}"
                  for key, icon, ar_name, en_name in menu_options]

        selected = st.radio("Navigation", labels, label_visibility="collapsed")
        return menu_options[labels.index(selected)][0]
