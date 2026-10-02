import streamlit as st

SECTIONS=['العملات|Currencies', 'أسعار الصرف|Exchange Rates', 'العملة الأساسية|Base Currency', 'سجل تغير السعر|Rate History']

def show_currencies(language):
    ar=language=="العربية"
    st.title("💱 " + ("العملات وأسعار الصرف" if ar else "Currencies & Exchange Rates"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_currencies_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_currencies_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_currencies_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_currencies_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_currencies_save_"+str(i), type="primary")
