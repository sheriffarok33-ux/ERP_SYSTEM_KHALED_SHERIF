import streamlit as st

SECTIONS=['الشركة|Company', 'الترقيم|Document Sequences', 'الضرائب|Taxes', 'اللغة والمظهر|Language & Appearance', 'المزامنة|Synchronization', 'النسخ الاحتياطي|Backup']

def show_settings(language):
    ar=language=="العربية"
    st.title("⚙️ " + ("إعدادات النظام" if ar else "System Settings"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_settings_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_settings_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_settings_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_settings_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_settings_save_"+str(i), type="primary")
