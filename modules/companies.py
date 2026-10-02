import streamlit as st
import uuid

from core.database import local_database


# ============================================================
# ERP SYSTEM KHALED & SHERIF
# COMPANIES MANAGEMENT
# ============================================================


def save_company(
    company_code,
    name_ar,
    name_en,
    legal_name_ar,
    legal_name_en,
    commercial_no,
    tax_no,
    base_currency,
    fiscal_month,
    country,
    city,
    phone,
    email,
    website,
    address_ar,
    address_en,
    status,
    username
):

    company_uuid = str(uuid.uuid4())

    currency_code = base_currency.split(" - ")[0]

    status_value = (
        "active"
        if status in ["Active", "نشطة"]
        else "inactive"
    )

    with local_database() as db:

        existing = db.execute(
            """
            SELECT id
            FROM companies
            WHERE company_code = ?
            AND is_deleted = 0
            """,
            (company_code.strip(),)
        ).fetchone()

        if existing:
            return False, "duplicate"

        db.execute(
            """
            INSERT INTO companies
            (
                company_uuid,
                company_code,

                name_ar,
                name_en,

                legal_name_ar,
                legal_name_en,

                commercial_registration_no,
                tax_number,

                base_currency,
                fiscal_year_start_month,

                country,
                city,

                phone,
                email,
                website,

                address_ar,
                address_en,

                status,

                created_by,
                updated_by,

                sync_status
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?
            )
            """,
            (
                company_uuid,
                company_code.strip(),

                name_ar.strip(),
                name_en.strip(),

                legal_name_ar.strip(),
                legal_name_en.strip(),

                commercial_no.strip(),
                tax_no.strip(),

                currency_code,
                fiscal_month,

                country.strip(),
                city.strip(),

                phone.strip(),
                email.strip(),
                website.strip(),

                address_ar.strip(),
                address_en.strip(),

                status_value,

                username,
                username,

                "pending"
            )
        )

    return True, company_uuid


# ============================================================
# GET COMPANIES
# ============================================================

def get_companies(search_text=""):

    with local_database() as db:

        if search_text:

            search_value = f"%{search_text}%"

            rows = db.execute(
                """
                SELECT
                    id,
                    company_uuid,
                    company_code,
                    name_ar,
                    name_en,
                    commercial_registration_no,
                    tax_number,
                    base_currency,
                    country,
                    city,
                    phone,
                    email,
                    status,
                    created_at
                FROM companies
                WHERE is_deleted = 0
                AND
                (
                    company_code LIKE ?
                    OR name_ar LIKE ?
                    OR name_en LIKE ?
                    OR commercial_registration_no LIKE ?
                    OR tax_number LIKE ?
                )
                ORDER BY id DESC
                """,
                (
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value
                )
            ).fetchall()

        else:

            rows = db.execute(
                """
                SELECT
                    id,
                    company_uuid,
                    company_code,
                    name_ar,
                    name_en,
                    commercial_registration_no,
                    tax_number,
                    base_currency,
                    country,
                    city,
                    phone,
                    email,
                    status,
                    created_at
                FROM companies
                WHERE is_deleted = 0
                ORDER BY id DESC
                """
            ).fetchall()

    return rows


# ============================================================
# CHANGE COMPANY STATUS
# ============================================================

def change_company_status(company_id, new_status, username):

    with local_database() as db:

        db.execute(
            """
            UPDATE companies
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = ?,
                sync_status = 'pending'
            WHERE id = ?
            """,
            (
                new_status,
                username,
                company_id
            )
        )


# ============================================================
# MAIN SCREEN
# ============================================================

def show_companies(language):

    ar = language == "العربية"

    username = st.session_state.get(
        "username",
        "system"
    )

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title(
        "🏢 " +
        (
            "إدارة الشركات"
            if ar
            else "Companies Management"
        )
    )

    st.caption(
        "تعريف وإدارة الشركات المسجلة داخل نظام ERP"
        if ar
        else
        "Create and manage companies registered in the ERP system"
    )

    st.divider()

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2 = st.tabs(
        [
            "➕ إضافة شركة",
            "📋 الشركات المسجلة"
        ]
        if ar
        else
        [
            "➕ Add Company",
            "📋 Companies List"
        ]
    )

    # ========================================================
    # ADD COMPANY
    # ========================================================

    with tab1:

        st.subheader(
            "بيانات الشركة"
            if ar
            else "Company Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            company_code = st.text_input(
                "كود الشركة"
                if ar
                else "Company Code",
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
                "حالة الشركة"
                if ar
                else "Company Status",
                [
                    "نشطة",
                    "غير نشطة"
                ]
                if ar
                else
                [
                    "Active",
                    "Inactive"
                ]
            )

        st.divider()

        # ====================================================
        # LEGAL & FINANCIAL INFORMATION
        # ====================================================

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
                "الدولة"
                if ar
                else "Country"
            )

        st.divider()

        # ====================================================
        # CONTACT INFORMATION
        # ====================================================

        st.subheader(
            "بيانات الاتصال"
            if ar
            else "Contact Information"
        )

        col8, col9 = st.columns(2)

        with col8:

            phone = st.text_input(
                "رقم الهاتف"
                if ar
                else "Phone"
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
                "المدينة"
                if ar
                else "City"
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

        # ====================================================
        # COMPANY LOGO
        # ====================================================

        st.subheader(
            "شعار الشركة"
            if ar
            else "Company Logo"
        )

        logo = st.file_uploader(
            "اختر شعار الشركة"
            if ar
            else "Upload Company Logo",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ]
        )

        if logo:

            st.image(
                logo,
                width=180
            )

        st.divider()

        # ====================================================
        # SAVE COMPANY
        # ====================================================

        if st.button(
            "💾 حفظ الشركة"
            if ar
            else "💾 Save Company",
            type="primary",
            use_container_width=True
        ):

            if not company_code.strip():

                st.error(
                    "يجب إدخال كود الشركة."
                    if ar
                    else
                    "Company Code is required."
                )

            elif not name_ar.strip() and not name_en.strip():

                st.error(
                    "يجب إدخال اسم الشركة بالعربية أو الإنجليزية."
                    if ar
                    else
                    "Arabic or English Company Name is required."
                )

            else:

                try:

                    success, result = save_company(
                        company_code,
                        name_ar,
                        name_en,
                        legal_name_ar,
                        legal_name_en,
                        commercial_no,
                        tax_no,
                        base_currency,
                        fiscal_month,
                        country,
                        city,
                        phone,
                        email,
                        website,
                        address_ar,
                        address_en,
                        status,
                        username
                    )

                    if success:

                        st.success(
                            "تم حفظ الشركة بنجاح."
                            if ar
                            else
                            "Company saved successfully."
                        )

                        st.caption(
                            f"UUID: {result}"
                        )

                    elif result == "duplicate":

                        st.error(
                            "كود الشركة مستخدم بالفعل."
                            if ar
                            else
                            "Company Code already exists."
                        )

                except Exception as error:

                    st.error(
                        "حدث خطأ أثناء حفظ الشركة."
                        if ar
                        else
                        "An error occurred while saving the company."
                    )

                    st.code(str(error))

    # ========================================================
    # COMPANIES LIST
    # ========================================================

    with tab2:

        st.subheader(
            "الشركات المسجلة"
            if ar
            else "Registered Companies"
        )

        search_text = st.text_input(
            "🔎 بحث"
            if ar
            else "🔎 Search",
            key="company_search"
        )

        try:

            companies = get_companies(
                search_text.strip()
            )

            if not companies:

                st.info(
                    "لا توجد شركات مسجلة حتى الآن."
                    if ar
                    else
                    "No companies registered yet."
                )

            else:

                st.caption(
                    (
                        f"عدد الشركات: {len(companies)}"
                        if ar
                        else
                        f"Companies: {len(companies)}"
                    )
                )

                for company in companies:

                    company_name = (
                        company["name_ar"]
                        if ar and company["name_ar"]
                        else company["name_en"]
                    )

                    if not company_name:
                        company_name = company["company_code"]

                    with st.expander(
                        f"🏢 {company['company_code']} - {company_name}"
                    ):

                        col_a, col_b, col_c = st.columns(3)

                        with col_a:

                            st.write(
                                "**" +
                                (
                                    "الكود"
                                    if ar
                                    else "Code"
                                ) +
                                ":**",
                                company["company_code"]
                            )

                            st.write(
                                "**" +
                                (
                                    "الاسم العربي"
                                    if ar
                                    else "Arabic Name"
                                ) +
                                ":**",
                                company["name_ar"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "الاسم الإنجليزي"
                                    if ar
                                    else "English Name"
                                ) +
                                ":**",
                                company["name_en"] or "-"
                            )

                        with col_b:

                            st.write(
                                "**" +
                                (
                                    "السجل التجاري"
                                    if ar
                                    else "Commercial No."
                                ) +
                                ":**",
                                company["commercial_registration_no"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "الرقم الضريبي"
                                    if ar
                                    else "Tax Number"
                                ) +
                                ":**",
                                company["tax_number"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "العملة"
                                    if ar
                                    else "Currency"
                                ) +
                                ":**",
                                company["base_currency"]
                            )

                        with col_c:

                            st.write(
                                "**" +
                                (
                                    "الدولة"
                                    if ar
                                    else "Country"
                                ) +
                                ":**",
                                company["country"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "المدينة"
                                    if ar
                                    else "City"
                                ) +
                                ":**",
                                company["city"] or "-"
                            )

                            current_status = company["status"]

                            status_text = (
                                "نشطة"
                                if ar and current_status == "active"
                                else
                                "غير نشطة"
                                if ar
                                else
                                "Active"
                                if current_status == "active"
                                else
                                "Inactive"
                            )

                            st.write(
                                "**" +
                                (
                                    "الحالة"
                                    if ar
                                    else "Status"
                                ) +
                                ":**",
                                status_text
                            )

                        st.divider()

                        if current_status == "active":

                            if st.button(
                                "⛔ إيقاف الشركة"
                                if ar
                                else "⛔ Deactivate Company",
                                key=f"deactivate_{company['id']}"
                            ):

                                change_company_status(
                                    company["id"],
                                    "inactive",
                                    username
                                )

                                st.rerun()

                        else:

                            if st.button(
                                "✅ تفعيل الشركة"
                                if ar
                                else "✅ Activate Company",
                                key=f"activate_{company['id']}"
                            ):

                                change_company_status(
                                    company["id"],
                                    "active",
                                    username
                                )

                                st.rerun()

        except Exception as error:

            st.error(
                "حدث خطأ أثناء تحميل الشركات المسجلة."
                if ar
                else
                "An error occurred while loading registered companies."
            )

            st.code(str(error))

