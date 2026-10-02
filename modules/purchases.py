import streamlit as st

def show_purchases(language):
    ar = language == "العربية"
    st.title("🧾 " + ("المشتريات والتكلفة والتسعير" if ar else "Purchasing, Cost & Pricing"))
    tabs=st.tabs(
        ["📋 طلب شراء","📝 أمر شراء","🧾 فاتورة شراء","↩️ مرتجع مشتريات","📊 مقارنة التكلفة","🏷️ اعتماد الأسعار"]
        if ar else
        ["📋 Purchase Request","📝 Purchase Order","🧾 Purchase Invoice","↩️ Purchase Return","📊 Cost Comparison","🏷️ Price Approval"]
    )
    with tabs[0]:
        st.text_input("رقم الطلب" if ar else "Request No.", value="AUTO")
        st.date_input("التاريخ" if ar else "Date")
        st.text_input("طالب الشراء" if ar else "Requested By")
        st.data_editor([], num_rows="dynamic", use_container_width=True)
        st.button("حفظ الطلب" if ar else "Save Request", type="primary")
    with tabs[1]:
        c1,c2,c3=st.columns(3)
        c1.text_input("رقم أمر الشراء" if ar else "PO No.", value="AUTO")
        c2.text_input("المورد" if ar else "Supplier")
        c3.text_input("العملة" if ar else "Currency")
        st.data_editor([], num_rows="dynamic", use_container_width=True)
        st.button("حفظ أمر الشراء" if ar else "Save Purchase Order", type="primary")
    with tabs[2]:
        c1,c2,c3,c4=st.columns(4)
        c1.text_input("رقم الفاتورة الداخلي" if ar else "Internal Invoice No.", value="AUTO")
        c2.text_input("رقم فاتورة المورد" if ar else "Supplier Invoice No.")
        c3.text_input("المورد" if ar else "Supplier")
        c4.date_input("تاريخ الفاتورة" if ar else "Invoice Date")
        st.file_uploader("تحميل صورة/PDF/Excel للفاتورة" if ar else "Upload invoice image/PDF/Excel",
                         type=["pdf","png","jpg","jpeg","xlsx","xls"])
        st.data_editor(
            [{"الصنف":"","الكمية":0.0,"سعر الشراء":0.0,"خصم":0.0,"ضريبة":0.0,"الإجمالي":0.0}]
            if ar else
            [{"Item":"","Qty":0.0,"Purchase Price":0.0,"Discount":0.0,"Tax":0.0,"Total":0.0}],
            num_rows="dynamic", use_container_width=True
        )
        st.button("حفظ الفاتورة وإرسالها للمقارنة" if ar else "Save Invoice & Send to Cost Comparison", type="primary")
    with tabs[3]:
        st.text_input("رقم فاتورة الشراء الأصلية" if ar else "Original Purchase Invoice")
        st.data_editor([], num_rows="dynamic", use_container_width=True)
        st.button("حفظ المرتجع" if ar else "Save Return", type="primary")
    with tabs[4]:
        st.subheader("مقارنة الفاتورة الجديدة بآخر تكلفة شراء" if ar else "Compare New Invoice with Previous Purchase Cost")
        threshold=st.number_input("نسبة التنبيه عند تغير التكلفة %" if ar else "Cost Change Alert %", min_value=0.0, value=5.0)
        st.data_editor(
            [{"الصنف":"مثال","التكلفة السابقة":10.0,"التكلفة الجديدة":12.0,"فرق التكلفة %":20.0,
              "سعر البيع الحالي":15.0,"هامش الربح الحالي %":20.0,"السعر المقترح":18.0,"الهامش الجديد %":20.0,"القرار":"بانتظار الإدارة"}]
            if ar else
            [{"Item":"Example","Previous Cost":10.0,"New Cost":12.0,"Cost Change %":20.0,
              "Current Sale Price":15.0,"Current Margin %":20.0,"Suggested Price":18.0,"New Margin %":20.0,"Decision":"Pending Management"}],
            use_container_width=True, disabled=True
        )
        st.caption(("لا يتم تعديل سعر البيع تلقائيًا. يتم إنشاء طلب اعتماد للإدارة."
                    if ar else "Sale prices are never changed automatically. A management approval request is created."))
        st.button("إرسال طلب تعديل الأسعار للإدارة" if ar else "Send Price Change Request to Management", type="primary")
    with tabs[5]:
        st.subheader("طلبات تعديل الأسعار المعلقة" if ar else "Pending Price Change Requests")
        st.data_editor(
            [{"الصنف":"","السعر القديم":0.0,"السعر المقترح":0.0,"السعر المعتمد":0.0,"الحالة":"بانتظار الموافقة"}]
            if ar else
            [{"Item":"","Old Price":0.0,"Suggested Price":0.0,"Approved Price":0.0,"Status":"Pending Approval"}],
            num_rows="dynamic", use_container_width=True
        )
        c1,c2,c3=st.columns(3)
        c1.button("✅ اعتماد الأسعار" if ar else "✅ Approve Prices", type="primary")
        c2.button("✏️ تعديل المقترح" if ar else "✏️ Modify Proposal")
        c3.button("❌ رفض" if ar else "❌ Reject")
