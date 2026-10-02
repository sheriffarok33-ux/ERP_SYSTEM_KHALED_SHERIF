import streamlit as st

SECTIONS=['الموظفون|Employees', 'العقود|Contracts', 'الحضور|Attendance', 'الإجازات|Leave', 'الرواتب|Payroll', 'السلف والخصومات|Loans & Deductions']

def show_hr(language):
    ar=language=="العربية"
    st.title("👨‍💼 " + ("الموارد البشرية والرواتب" if ar else "HR & Payroll"))
    labels=[x.split("|")[0] if ar else x.split("|")[1] for x in SECTIONS]
    tabs=st.tabs(labels)
    for i,tab in enumerate(tabs):
        with tab:
            st.subheader(labels[i])
            c1,c2=st.columns(2)
            c1.text_input("الكود / الرقم" if ar else "Code / Number", key="show_hr_code_"+str(i))
            c2.text_input("الاسم / المرجع" if ar else "Name / Reference", key="show_hr_name_"+str(i))
            st.text_area("البيانات / الملاحظات" if ar else "Details / Notes", key="show_hr_details_"+str(i))
            st.data_editor([], num_rows="dynamic", use_container_width=True, key="show_hr_grid_"+str(i))
            st.button("💾 حفظ" if ar else "💾 Save", key="show_hr_save_"+str(i), type="primary")
