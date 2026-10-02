import streamlit as st
from modules.review_helpers import review_header, status_box

FIELDS = ['كود الحساب|Account Code', 'الاسم|Name', 'النوع|Type', 'الهاتف|Phone', 'الرقم الضريبي|Tax Number', 'الحد الائتماني|Credit Limit', 'الرصيد الافتتاحي|Opening Balance']

def show_crm(language):
    ar = review_header(
        language, "👥", "إدارة العملاء والموردين", "CRM - Customers & Suppliers",
        "إدارة بيانات العملاء والموردين والحدود الائتمانية والأرصدة.", "Manage customers, suppliers, credit limits and balances"
    )
    status_box(ar)
    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["➕ إدخال / تعريف", "📋 السجلات", "⚙️ خيارات"]
        if ar else
        ["➕ Create / Define", "📋 Records", "⚙️ Options"]
    )

    with tab1:
        st.subheader("البيانات الأساسية" if ar else "Basic Information")
        for i in range(0, len(FIELDS), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(FIELDS):
                    ar_label, en_label = FIELDS[idx].split("|")
                    with col:
                        st.text_input(
                            ar_label if ar else en_label,
                            key=f"show_crm_field_{idx}"
                        )

        st.text_area(
            "ملاحظات" if ar else "Notes",
            key="show_crm_notes"
        )
        st.button(
            "💾 حفظ (نسخة المراجعة)" if ar else "💾 Save (Review Version)",
            key="show_crm_save",
            type="primary",
            use_container_width=True
        )

    with tab2:
        st.subheader("السجلات" if ar else "Records")
        st.text_input(
            "🔎 بحث" if ar else "🔎 Search",
            key="show_crm_search"
        )
        st.info(
            "سيظهر هنا جدول السجلات بعد اعتماد الشاشة وربط قاعدة البيانات."
            if ar else
            "Records will appear here after screen approval and database integration."
        )

    with tab3:
        st.subheader("خيارات الشاشة" if ar else "Screen Options")
        st.checkbox("السماح بالتعديل" if ar else "Allow Editing", value=True, key="show_crm_edit")
        st.checkbox("السماح بالحذف" if ar else "Allow Deletion", value=False, key="show_crm_delete")
        st.checkbox("تسجيل العمليات في سجل المراجعة" if ar else "Write actions to Audit Log", value=True, key="show_crm_audit")
