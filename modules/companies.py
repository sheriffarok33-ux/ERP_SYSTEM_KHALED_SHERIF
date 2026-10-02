import streamlit as st


def show_companies(language):

    ar = language == "العربية"

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("🏢 " + ("إدارة الشركات" if ar else "Companies Management"))

    st.caption(
        "تعريف وإدارة الشركات المسجلة داخل نظام ERP"
        if ar
        else
        "Create and manage companies registered in the ERP system"
    )

    st.divider()

    # ==========================================
    # TABS
    # ==========================================

    tab1, tab2 = st.tabs(
        ["➕ إضافة شركة", "📋 الشركات المسجلة"]
        if ar
        else ["➕ Add Company", "📋 Companies List"]
    )

    # ==========================================
    # ADD COMPANY
    # ==========================================

    with tab1:

        st.subheader(
            "بيانات الشركة"
            if ar
            else "Company Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            company_code = st.text_input(
                "كود الشركة" if ar else "Company Code",
                placeholder="COMP-001"
            )

            name_ar = st.text_input(
                "اسم الشركة بالعربية"
                if ar
                else "Company Name (Arabic)"
            )

            legal_name_ar = st.text_input(
                "الاسم القانوني بالعربية"
                if ar
                else "Legal Name (Arabic)"
            )

        with col2:

            name_en = st.text_input(
                "اسم الشركة بالإنجليزية"
                if ar
                else "Company Name (English)"
            )

            legal_name_en = st.text_input(
                "الاسم القانوني بالإنجليزية"
                if ar
                else "Legal Name (English)"
            )

            status = st.selectbox(
                "حالة الشركة" if ar else "Company Status",
                ["نشطة", "غير نشطة"]
                if ar
                else ["Active", "Inactive"]
            )

        st.divider()

        # ======================================
        # LEGAL INFORMATION
        # ======================================

        st.subheader(
            "البيانات القانونية والمالية"
            if ar
            else "Legal & Financial Information"
        )

        col3, col4, col5 = st.columns(3)

        with col3:

            commercial_no = st.text_input(
                "رقم السجل التجاري"
                if ar
                else "Commercial Registration No."
            )

        with col4:

            tax_no = st.text_input(
                "الرقم الضريبي"
                if ar
                else "Tax Number"
            )

        with col5:

            base_currency = st.selectbox(
                "العملة الأساسية"
                if ar
                else "Base Currency",
                [
                    "LYD - Libyan Dinar",
                    "USD - US Dollar",
                    "EUR - Euro",
                    "EGP - Egyptian Pound",
                    "GBP - British Pound"
                ]
            )

        col6, col7 = st.columns(2)

        with col6:

            fiscal_month = st.selectbox(
                "شهر بداية السنة المالية"
                if ar
                else "Fiscal Year Start Month",
                list(range(1, 13)),
                index=0
            )

        with col7:

            country = st.text_input(
                "الدولة" if ar else "Country"
            )

        st.divider()

        # ======================================
        # CONTACT INFORMATION
        # ======================================

        st.subheader(
            "بيانات الاتصال"
            if ar
            else "Contact Information"
        )

        col8, col9 = st.columns(2)

        with col8:

            phone = st.text_input(
                "رقم الهاتف" if ar else "Phone"
            )

            email = st.text_input(
                "البريد الإلكتروني"
                if ar
                else "Email"
            )

        with col9:

            website = st.text_input(
                "الموقع الإلكتروني"
                if ar
                else "Website"
            )

            city = st.text_input(
                "المدينة" if ar else "City"
            )

        address_ar = st.text_area(
            "العنوان بالعربية"
            if ar
            else "Address (Arabic)"
        )

        address_en = st.text_area(
            "العنوان بالإنجليزية"
            if ar
            else "Address (English)"
        )

        st.divider()

        # ======================================
        # COMPANY LOGO
        # ======================================

        st.subheader(
            "شعار الشركة"
            if ar
            else "Company Logo"
        )

        logo = st.file_uploader(
            "اختر شعار الشركة"
            if ar
            else "Upload Company Logo",
            type=["png", "jpg", "jpeg", "webp"]
        )

        if logo:
            st.image(logo, width=180)

        st.divider()

        # ======================================
        # SAVE
        # ======================================

        if st.button(
            "💾 حفظ الشركة"
            if ar
            else "💾 Save Company",
            type="primary",
            use_container_width=True
        ):

            if not company_code:

                st.error(
                    "يجب إدخال كود الشركة."
                    if ar
                    else "Company Code is required."
                )

            elif not name_ar and not name_en:

                st.error(
                    "يجب إدخال اسم الشركة."
                    if ar
                    else "Company Name is required."
                )

            else:

                # Database saving will be connected
                # when PostgreSQL Core is implemented.

                st.success(
                    "تم التحقق من بيانات الشركة بنجاح. سيتم ربط الحفظ بقاعدة البيانات في المرحلة التالية."
                    if ar
                    else
                    "Company information validated successfully. Database saving will be connected in the next stage."
                )

    # ==========================================
    # COMPANIES LIST
    # ==========================================

    with tab2:

        st.subheader(
            "الشركات المسجلة"
            if ar
            else "Registered Companies"
        )

        st.info(
            "ستظهر هنا الشركات المسجلة بعد ربط قاعدة البيانات."
            if ar
            else
            "Registered companies will appear here after connecting the database."
        )
