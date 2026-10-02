import streamlit as st

SECTIONS=['الشحنات|Shipments', 'الاعتمادات|L/C', 'المصاريف|Landed Costs', 'التخليص الجمركي|Customs Clearance', 'الحاويات|Containers']

def show_import_export(language):
    ar=language=="العربية"
    st.title("🚢 " + ("الاستيراد والتصدير" if ar else "Import & Export"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_import_export_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_import_export_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_import_export_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_import_export_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_import_export_save_"+str(i), type="primary")
