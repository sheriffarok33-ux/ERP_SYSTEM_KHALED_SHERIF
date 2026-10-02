import streamlit as st

SECTIONS=['شاشة البيع|Sales Screen', 'الورديات|Shifts', 'المرتجعات|Returns', 'طرق الدفع|Payment Methods', 'إقفال الكاشير|Cashier Closing']

def show_pos(language):
    ar=language=="العربية"
    st.title("🏪 " + ("نقاط البيع" if ar else "Point of Sale"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_pos_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_pos_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_pos_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_pos_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_pos_save_"+str(i), type="primary")
