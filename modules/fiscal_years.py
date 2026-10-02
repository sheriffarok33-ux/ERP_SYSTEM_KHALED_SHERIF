import streamlit as st

SECTIONS=['تعريف سنة مالية|Define Fiscal Year', 'الفترات الشهرية|Accounting Periods', 'فتح وإغلاق الفترات|Open / Close Periods', 'إقفال السنة|Year Closing']

def show_fiscal_years(language):
    ar=language=="العربية"
    st.title("📅 " + ("السنوات والفترات المالية" if ar else "Fiscal Years & Periods"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_fiscal_years_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_fiscal_years_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_fiscal_years_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_fiscal_years_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_fiscal_years_save_"+str(i), type="primary")
