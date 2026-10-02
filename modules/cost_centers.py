import streamlit as st

SECTIONS=['شجرة مراكز التكلفة|Cost Center Tree', 'ربط الفروع|Branch Assignment', 'ربط الحسابات|Account Assignment', 'تقارير المراكز|Cost Center Reports']

def show_cost_centers(language):
    ar=language=="العربية"
    st.title("🎯 " + ("مراكز التكلفة" if ar else "Cost Centers"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_cost_centers_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_cost_centers_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_cost_centers_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_cost_centers_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_cost_centers_save_"+str(i), type="primary")
