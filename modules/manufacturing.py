import streamlit as st

SECTIONS=['BOM|BOM', 'أوامر الإنتاج|Production Orders', 'صرف خامات|Material Issue', 'استلام إنتاج|Finished Goods Receipt', 'تكلفة الإنتاج|Production Cost']

def show_manufacturing(language):
    ar=language=="العربية"
    st.title("🏭 " + ("التصنيع" if ar else "Manufacturing"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_manufacturing_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_manufacturing_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_manufacturing_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_manufacturing_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_manufacturing_save_"+str(i), type="primary")
