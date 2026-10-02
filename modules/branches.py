import streamlit as st
import uuid

from core.database import local_database


# ============================================================
# ERP SYSTEM KHALED & SHERIF
# BRANCHES MANAGEMENT
# ============================================================


def get_active_companies():

    with local_database() as db:

        return db.execute(
            """
            SELECT
                id,
                company_code,
                name_ar,
                name_en
            FROM companies
            WHERE is_deleted = 0
            AND status = 'active'
            ORDER BY company_code
            """
        ).fetchall()


def save_branch(
    company_id,
    branch_code,
    name_ar,
    name_en,
    country,
    city,
    address_ar,
    address_en,
    phone,
    email,
    status
):

    branch_uuid = str(uuid.uuid4())

    status_value = (
        "active"
        if status in ["Active", "نشط"]
        else "inactive"
    )

    with local_database() as db:

        existing = db.execute(
            """
            SELECT id
            FROM branches
            WHERE company_id = ?
            AND branch_code = ?
            AND is_deleted = 0
            """,
            (
                company_id,
                branch_code.strip()
            )
        ).fetchone()

        if existing:
            return False, "duplicate"

        db.execute(
            """
            INSERT INTO branches
            (
                branch_uuid,
                company_id,
                branch_code,
                name_ar,
                name_en,
                country,
                city,
                address_ar,
                address_en,
                phone,
                email,
                status,
                sync_status
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                branch_uuid,
                company_id,
                branch_code.strip(),
                name_ar.strip(),
                name_en.strip(),
                country.strip(),
                city.strip(),
                address_ar.strip(),
                address_en.strip(),
                phone.strip(),
                email.strip(),
                status_value,
                "pending"
            )
        )

    return True, branch_uuid


def get_branches(search_text=""):

    with local_database() as db:

        query = """
            SELECT
                branches.id,
                branches.branch_uuid,
                branches.branch_code,
                branches.name_ar,
                branches.name_en,
                branches.country,
                branches.city,
                branches.phone,
                branches.email,
                branches.status,
                branches.created_at,

                companies.company_code,
                companies.name_ar AS company_name_ar,
                companies.name_en AS company_name_en

            FROM branches

            INNER JOIN companies
                ON companies.id = branches.company_id

            WHERE branches.is_deleted = 0
        """

        parameters = []

        if search_text:

            search_value = f"%{search_text}%"

            query += """
                AND
                (
                    branches.branch_code LIKE ?
                    OR branches.name_ar LIKE ?
                    OR branches.name_en LIKE ?
                    OR branches.city LIKE ?
                    OR companies.company_code LIKE ?
                    OR companies.name_ar LIKE ?
                    OR companies.name_en LIKE ?
                )
            """

            parameters = [search_value] * 7

        query += """
            ORDER BY branches.id DESC
        """

        return db.execute(
            query,
            parameters
        ).fetchall()


def change_branch_status(
    branch_id,
    new_status
):

    with local_database() as db:

        db.execute(
            """
            UPDATE branches
            SET
                status = ?,
                updated_at = CURRENT_TIMESTAMP,
                sync_status = 'pending'
            WHERE id = ?
            """,
            (
                new_status,
                branch_id
            )
        )


# ============================================================
# MAIN SCREEN
# ============================================================

def show_branches(language):

    ar = language == "العربية"

    st.title(
        "🏢 " +
        (
            "إدارة الفروع"
            if ar
            else "Branches Management"
        )
    )

    st.caption(
        (
            "تعريف وإدارة فروع الشركات المسجلة داخل نظام ERP"
            if ar
            else
            "Create and manage company branches in the ERP system"
        )
    )

    st.divider()

    companies = get_active_companies()

    if not companies:

        st.warning(
            (
                "يجب تسجيل شركة نشطة أولاً قبل إضافة الفروع."
                if ar
                else
                "You must create an active company before adding branches."
            )
        )

        return

    tab1, tab2 = st.tabs(
        [
            "➕ إضافة فرع",
            "📋 الفروع المسجلة"
        ]
        if ar
        else
        [
            "➕ Add Branch",
            "📋 Branches List"
        ]
    )


    # ========================================================
    # ADD BRANCH
    # ========================================================

    with tab1:

        st.subheader(
            "بيانات الفرع"
            if ar
            else "Branch Information"
        )

        company_options = {}

        for company in companies:

            company_name = (
                company["name_ar"]
                if ar and company["name_ar"]
                else company["name_en"]
            )

            if not company_name:
                company_name = company["company_code"]

            label = (
                f"{company['company_code']} - "
                f"{company_name}"
            )

            company_options[label] = company["id"]

        selected_company = st.selectbox(
            "الشركة"
            if ar
            else "Company",
            list(company_options.keys())
        )

        company_id = company_options[
            selected_company
        ]

        col1, col2 = st.columns(2)

        with col1:

            branch_code = st.text_input(
                "كود الفرع"
                if ar
                else "Branch Code",
                placeholder="BR-001"
            )

            name_ar = st.text_input(
                "اسم الفرع بالعربية"
                if ar
                else "Branch Name (Arabic)"
            )

            country = st.text_input(
                "الدولة"
                if ar
                else "Country"
            )

            phone = st.text_input(
                "رقم الهاتف"
                if ar
                else "Phone"
            )

        with col2:

            name_en = st.text_input(
                "اسم الفرع بالإنجليزية"
                if ar
                else "Branch Name (English)"
            )

            city = st.text_input(
                "المدينة"
                if ar
                else "City"
            )

            email = st.text_input(
                "البريد الإلكتروني"
                if ar
                else "Email"
            )

            status = st.selectbox(
                "حالة الفرع"
                if ar
                else "Branch Status",
                [
                    "نشط",
                    "غير نشط"
                ]
                if ar
                else
                [
                    "Active",
                    "Inactive"
                ]
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

        if st.button(
            "💾 حفظ الفرع"
            if ar
            else "💾 Save Branch",
            type="primary",
            use_container_width=True
        ):

            if not branch_code.strip():

                st.error(
                    "يجب إدخال كود الفرع."
                    if ar
                    else
                    "Branch Code is required."
                )

            elif (
                not name_ar.strip()
                and not name_en.strip()
            ):

                st.error(
                    (
                        "يجب إدخال اسم الفرع "
                        "بالعربية أو الإنجليزية."
                    )
                    if ar
                    else
                    (
                        "Arabic or English "
                        "Branch Name is required."
                    )
                )

            else:

                try:

                    success, result = save_branch(
                        company_id,
                        branch_code,
                        name_ar,
                        name_en,
                        country,
                        city,
                        address_ar,
                        address_en,
                        phone,
                        email,
                        status
                    )

                    if success:

                        st.success(
                            "تم حفظ الفرع بنجاح."
                            if ar
                            else
                            "Branch saved successfully."
                        )

                        st.caption(
                            f"UUID: {result}"
                        )

                    elif result == "duplicate":

                        st.error(
                            (
                                "كود الفرع مستخدم بالفعل "
                                "داخل هذه الشركة."
                            )
                            if ar
                            else
                            (
                                "Branch Code already exists "
                                "for this company."
                            )
                        )

                except Exception as error:

                    st.error(
                        "حدث خطأ أثناء حفظ الفرع."
                        if ar
                        else
                        "An error occurred while saving the branch."
                    )

                    st.code(str(error))


    # ========================================================
    # BRANCHES LIST
    # ========================================================

    with tab2:

        st.subheader(
            "الفروع المسجلة"
            if ar
            else "Registered Branches"
        )

        search_text = st.text_input(
            "🔎 بحث"
            if ar
            else "🔎 Search",
            key="branch_search"
        )

        try:

            branches = get_branches(
                search_text.strip()
            )

            if not branches:

                st.info(
                    "لا توجد فروع مسجلة."
                    if ar
                    else
                    "No branches registered."
                )

            else:

                st.caption(
                    (
                        f"عدد الفروع: {len(branches)}"
                        if ar
                        else
                        f"Branches: {len(branches)}"
                    )
                )

                for branch in branches:

                    branch_name = (
                        branch["name_ar"]
                        if ar and branch["name_ar"]
                        else branch["name_en"]
                    )

                    if not branch_name:
                        branch_name = branch["branch_code"]

                    company_name = (
                        branch["company_name_ar"]
                        if ar and branch["company_name_ar"]
                        else branch["company_name_en"]
                    )

                    if not company_name:
                        company_name = branch["company_code"]

                    with st.expander(
                        f"🏢 {branch['branch_code']} - {branch_name}"
                    ):

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.write(
                                "**" +
                                (
                                    "الشركة"
                                    if ar
                                    else "Company"
                                ) +
                                ":**",
                                company_name
                            )

                            st.write(
                                "**" +
                                (
                                    "كود الفرع"
                                    if ar
                                    else "Branch Code"
                                ) +
                                ":**",
                                branch["branch_code"]
                            )

                        with col2:

                            st.write(
                                "**" +
                                (
                                    "الدولة"
                                    if ar
                                    else "Country"
                                ) +
                                ":**",
                                branch["country"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "المدينة"
                                    if ar
                                    else "City"
                                ) +
                                ":**",
                                branch["city"] or "-"
                            )

                        with col3:

                            st.write(
                                "**" +
                                (
                                    "الهاتف"
                                    if ar
                                    else "Phone"
                                ) +
                                ":**",
                                branch["phone"] or "-"
                            )

                            current_status = branch["status"]

                            status_text = (
                                "نشط"
                                if ar and current_status == "active"
                                else
                                "غير نشط"
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
                                "⛔ إيقاف الفرع"
                                if ar
                                else "⛔ Deactivate Branch",
                                key=f"deactivate_branch_{branch['id']}"
                            ):

                                change_branch_status(
                                    branch["id"],
                                    "inactive"
                                )

                                st.rerun()

                        else:

                            if st.button(
                                "✅ تفعيل الفرع"
                                if ar
                                else "✅ Activate Branch",
                                key=f"activate_branch_{branch['id']}"
                            ):

                                change_branch_status(
                                    branch["id"],
                                    "active"
                                )

                                st.rerun()

        except Exception as error:

            st.error(
                "حدث خطأ أثناء تحميل الفروع."
                if ar
                else
                "An error occurred while loading branches."
            )

            st.code(str(error))
