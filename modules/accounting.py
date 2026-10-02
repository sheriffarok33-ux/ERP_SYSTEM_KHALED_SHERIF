import streamlit as st

def show_accounting(language):
    ar = language == "العربية"
    st.title("💰 " + ("المالية والحسابات" if ar else "Finance & Accounting"))
    tabs = st.tabs(
        ["📚 دليل الحسابات","🧾 القيود اليومية","💵 سند قبض","💸 سند صرف","🏦 الصندوق والبنوك",
         "🎯 مراكز التكلفة","📥 الأرصدة الافتتاحية","📒 الأستاذ العام","⚖️ ميزان المراجعة",
         "📈 قائمة الدخل","🏢 الميزانية"]
        if ar else
        ["📚 Chart of Accounts","🧾 Journal Entries","💵 Receipt Voucher","💸 Payment Voucher","🏦 Cash & Banks",
         "🎯 Cost Centers","📥 Opening Balances","📒 General Ledger","⚖️ Trial Balance",
         "📈 Income Statement","🏢 Balance Sheet"]
    )
    with tabs[0]:
        c1,c2,c3=st.columns(3)
        c1.text_input("كود الحساب" if ar else "Account Code")
        c2.text_input("اسم الحساب" if ar else "Account Name")
        c3.selectbox("نوع الحساب" if ar else "Account Type",
                     ["أصول","خصوم","حقوق ملكية","إيرادات","مصروفات"] if ar else
                     ["Assets","Liabilities","Equity","Revenue","Expenses"])
        st.checkbox("حساب رئيسي" if ar else "Parent Account")
        st.button("💾 حفظ الحساب" if ar else "💾 Save Account", type="primary")
    with tabs[1]:
        c1,c2,c3=st.columns(3)
        c1.text_input("رقم القيد" if ar else "Journal No.", value="AUTO")
        c2.date_input("التاريخ" if ar else "Date")
        c3.text_input("المرجع" if ar else "Reference")
        st.data_editor(
            [{"الحساب":"","البيان":"","مدين":0.0,"دائن":0.0,"مركز التكلفة":""}]
            if ar else
            [{"Account":"","Description":"","Debit":0.0,"Credit":0.0,"Cost Center":""}],
            num_rows="dynamic", use_container_width=True
        )
        st.button("حفظ مسودة" if ar else "Save Draft")
        st.button("اعتماد وترحيل" if ar else "Approve & Post", type="primary")
    for idx, title in [(2,"سند قبض"),(3,"سند صرف")]:
        with tabs[idx]:
            c1,c2,c3=st.columns(3)
            c1.text_input(("رقم السند" if ar else "Voucher No."), value="AUTO", key=f"vno{idx}")
            c2.date_input("التاريخ" if ar else "Date", key=f"vdate{idx}")
            c3.number_input("المبلغ" if ar else "Amount", min_value=0.0, key=f"vamt{idx}")
            st.text_input("الحساب / الطرف" if ar else "Account / Party", key=f"party{idx}")
            st.text_area("البيان" if ar else "Description", key=f"desc{idx}")
            st.button("حفظ" if ar else "Save", key=f"save{idx}", type="primary")
    with tabs[4]:
        st.subheader("الصندوق والحسابات البنكية" if ar else "Cash & Bank Accounts")
        st.dataframe([], use_container_width=True)
    with tabs[5]:
        st.info("إدارة وربط مراكز التكلفة بالحركات المحاسبية." if ar else "Manage and assign cost centers to accounting transactions.")
    with tabs[6]:
        st.subheader("إدخال الأرصدة الافتتاحية" if ar else "Opening Balances")
        st.data_editor([], num_rows="dynamic", use_container_width=True)
    with tabs[7]:
        st.subheader("كشف الأستاذ العام" if ar else "General Ledger")
        st.text_input("الحساب" if ar else "Account")
        st.date_input("من تاريخ" if ar else "From Date")
        st.date_input("إلى تاريخ" if ar else "To Date")
        st.button("عرض" if ar else "View")
    with tabs[8]:
        st.subheader("ميزان المراجعة" if ar else "Trial Balance")
        st.button("إعداد التقرير" if ar else "Generate Report")
    with tabs[9]:
        st.subheader("قائمة الدخل" if ar else "Income Statement")
        st.button("إعداد التقرير" if ar else "Generate Report")
    with tabs[10]:
        st.subheader("قائمة المركز المالي" if ar else "Balance Sheet")
        st.button("إعداد التقرير" if ar else "Generate Report")
