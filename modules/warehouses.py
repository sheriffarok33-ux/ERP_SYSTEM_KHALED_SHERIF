import streamlit as st
import uuid

from core.database import local_database


# ============================================================
# ERP SYSTEM KHALED & SHERIF
# WAREHOUSES MANAGEMENT
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


def get_active_branches(company_id):

    with local_database() as db:

        return db.execute(
            """
            SELECT
                id,
                branch_code,
                name_ar,
                name_en
            FROM branches
            WHERE company_id = ?
            AND is_deleted = 0
            AND status = 'active'
            ORDER BY branch_code
            """,
            (company_id,)
        ).fetchall()


def save_warehouse(
    company_id,
    branch_id,
    warehouse_code,
    name_ar,
    name_en,
    warehouse_type,
    country,
    city,
    address_ar,
    address_en,
    phone,
    manager_name,
    allow_negative_stock,
    status,
    username
):

    warehouse_uuid = str(uuid.uuid4())

    status_value = (
        "active"
        if status in ["Active", "نشط"]
        else "inactive"
    )

    type_map = {
        "General": "general",
        "Main": "main",
        "Raw Materials": "raw_materials",
        "Finished Goods": "finished_goods",
        "Spare Parts": "spare_parts",
        "Transit": "transit",
        "Returns": "returns",
        "عام": "general",
        "رئيسي": "main",
        "مواد خام": "raw_materials",
        "منتجات تامة": "finished_goods",
        "قطع غيار": "spare_parts",
        "ترانزيت": "transit",
        "مرتجعات": "returns"
    }

    warehouse_type_value = type_map.get(
        warehouse_type,
        "general"
    )

    with local_database() as db:

        existing = db.execute(
            """
            SELECT id
            FROM warehouses
            WHERE company_id = ?
            AND branch_id = ?
            AND warehouse_code = ?
            AND is_deleted = 0
            """,
            (
                company_id,
                branch_id,
                warehouse_code.strip()
            )
        ).fetchone()

        if existing:
            return False, "duplicate"

        db.execute(
            """
            INSERT INTO warehouses
            (
                warehouse_uuid,
                company_id,
                branch_id,
                warehouse_code,
                name_ar,
                name_en,
                warehouse_type,
                country,
                city,
                address_ar,
                address_en,
                phone,
                manager_name,
                allow_negative_stock,
                status,
                created_by,
                updated_by,
                sync_status
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                warehouse_uuid,
                company_id,
                branch_id,
                warehouse_code.strip(),
                name_ar.strip(),
                name_en.strip(),
                warehouse_type_value,
                country.strip(),
                city.strip(),
                address_ar.strip(),
                address_en.strip(),
                phone.strip(),
                manager_name.strip(),
                1 if allow_negative_stock else 0,
                status_value,
                username,
                username,
                "pending"
            )
        )

    return True, warehouse_uuid


def get_warehouses(search_text=""):

    with local_database() as db:

        query = """
            SELECT
                warehouses.id,
                warehouses.warehouse_uuid,
                warehouses.warehouse_code,
                warehouses.name_ar,
                warehouses.name_en,
                warehouses.warehouse_type,
                warehouses.country,
                warehouses.city,
                warehouses.phone,
                warehouses.manager_name,
                warehouses.allow_negative_stock,
                warehouses.status,
                warehouses.created_at,

                companies.company_code,
                companies.name_ar AS company_name_ar,
                companies.name_en AS company_name_en,

                branches.branch_code,
                branches.name_ar AS branch_name_ar,
                branches.name_en AS branch_name_en

            FROM warehouses

            INNER JOIN companies
                ON companies.id = warehouses.company_id

            INNER JOIN branches
                ON branches.id = warehouses.branch_id

            WHERE warehouses.is_deleted = 0
        """

        parameters = []

        if search_text:

            search_value = f"%{search_text}%"

            query += """
                AND
                (
                    warehouses.warehouse_code LIKE ?
                    OR warehouses.name_ar LIKE ?
                    OR warehouses.name_en LIKE ?
                    OR warehouses.city LIKE ?
                    OR warehouses.manager_name LIKE ?
                    OR companies.company_code LIKE ?
                    OR branches.branch_code LIKE ?
                )
            """

            parameters = [search_value] * 7

        query += """
            ORDER BY warehouses.id DESC
        """

        return db.execute(
            query,
            parameters
        ).fetchall()


def change_warehouse_status(
    warehouse_id,
    new_status,
    username
):

    with local_database() as db:

        db.execute(
            """
            UPDATE warehouses
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
                warehouse_id
            )
        )


# ============================================================
# MAIN SCREEN
# ============================================================

def show_warehouses(language):

    ar = language == "العربية"

    username = st.session_state.get(
        "username",
        "system"
    )

    st.title(
        "🏬 " +
        (
            "إدارة المخازن"
            if ar
            else "Warehouses Management"
        )
    )

    st.caption(
        (
            "تعريف وإدارة مخازن الشركات والفروع داخل نظام ERP"
            if ar
            else
            "Create and manage company and branch warehouses"
        )
    )

    st.divider()

    companies = get_active_companies()

    if not companies:

        st.warning(
            (
                "يجب تسجيل شركة نشطة أولاً."
                if ar
                else
                "You must create an active company first."
            )
        )

        return

    tab1, tab2 = st.tabs(
        [
            "➕ إضافة مخزن",
            "📋 المخازن المسجلة"
        ]
        if ar
        else
        [
            "➕ Add Warehouse",
            "📋 Warehouses List"
        ]
    )

    # ========================================================
    # ADD WAREHOUSE
    # ========================================================

    with tab1:

        st.subheader(
            "بيانات المخزن"
            if ar
            else "Warehouse Information"
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
            list(company_options.keys()),
            key="warehouse_company"
        )

        company_id = company_options[
            selected_company
        ]

        branches = get_active_branches(
            company_id
        )

        if not branches:

            st.warning(
                (
                    "لا توجد فروع نشطة لهذه الشركة. "
                    "يجب إضافة فرع أولاً."
                )
                if ar
                else
                (
                    "No active branches exist for this company. "
                    "Please create a branch first."
                )
            )

        else:

            branch_options = {}

            for branch in branches:

                branch_name = (
                    branch["name_ar"]
                    if ar and branch["name_ar"]
                    else branch["name_en"]
                )

                if not branch_name:
                    branch_name = branch["branch_code"]

                label = (
                    f"{branch['branch_code']} - "
                    f"{branch_name}"
                )

                branch_options[label] = branch["id"]

            selected_branch = st.selectbox(
                "الفرع"
                if ar
                else "Branch",
                list(branch_options.keys())
            )

            branch_id = branch_options[
                selected_branch
            ]

            col1, col2 = st.columns(2)

            with col1:

                warehouse_code = st.text_input(
                    "كود المخزن"
                    if ar
                    else "Warehouse Code",
                    placeholder="WH-001"
                )

                name_ar = st.text_input(
                    "اسم المخزن بالعربية"
                    if ar
                    else "Warehouse Name (Arabic)"
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
                    "اسم المخزن بالإنجليزية"
                    if ar
                    else "Warehouse Name (English)"
                )

                warehouse_type = st.selectbox(
                    "نوع المخزن"
                    if ar
                    else "Warehouse Type",
                    [
                        "عام",
                        "رئيسي",
                        "مواد خام",
                        "منتجات تامة",
                        "قطع غيار",
                        "ترانزيت",
                        "مرتجعات"
                    ]
                    if ar
                    else
                    [
                        "General",
                        "Main",
                        "Raw Materials",
                        "Finished Goods",
                        "Spare Parts",
                        "Transit",
                        "Returns"
                    ]
                )

                city = st.text_input(
                    "المدينة"
                    if ar
                    else "City"
                )

                manager_name = st.text_input(
                    "مسؤول المخزن"
                    if ar
                    else "Warehouse Manager"
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

            col3, col4 = st.columns(2)

            with col3:

                allow_negative_stock = st.checkbox(
                    "السماح بالمخزون السالب"
                    if ar
                    else "Allow Negative Stock",
                    value=False
                )

            with col4:

                status = st.selectbox(
                    "حالة المخزن"
                    if ar
                    else "Warehouse Status",
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

            st.divider()

            if st.button(
                "💾 حفظ المخزن"
                if ar
                else "💾 Save Warehouse",
                type="primary",
                use_container_width=True
            ):

                if not warehouse_code.strip():

                    st.error(
                        "يجب إدخال كود المخزن."
                        if ar
                        else
                        "Warehouse Code is required."
                    )

                elif (
                    not name_ar.strip()
                    and not name_en.strip()
                ):

                    st.error(
                        (
                            "يجب إدخال اسم المخزن "
                            "بالعربية أو الإنجليزية."
                        )
                        if ar
                        else
                        (
                            "Arabic or English Warehouse "
                            "Name is required."
                        )
                    )

                else:

                    try:

                        success, result = save_warehouse(
                            company_id,
                            branch_id,
                            warehouse_code,
                            name_ar,
                            name_en,
                            warehouse_type,
                            country,
                            city,
                            address_ar,
                            address_en,
                            phone,
                            manager_name,
                            allow_negative_stock,
                            status,
                            username
                        )

                        if success:

                            st.success(
                                "تم حفظ المخزن بنجاح."
                                if ar
                                else
                                "Warehouse saved successfully."
                            )

                            st.caption(
                                f"UUID: {result}"
                            )

                        elif result == "duplicate":

                            st.error(
                                (
                                    "كود المخزن مستخدم بالفعل "
                                    "داخل هذا الفرع."
                                )
                                if ar
                                else
                                (
                                    "Warehouse Code already exists "
                                    "for this branch."
                                )
                            )

                    except Exception as error:

                        st.error(
                            "حدث خطأ أثناء حفظ المخزن."
                            if ar
                            else
                            "An error occurred while saving the warehouse."
                        )

                        st.code(str(error))

    # ========================================================
    # WAREHOUSES LIST
    # ========================================================

    with tab2:

        st.subheader(
            "المخازن المسجلة"
            if ar
            else "Registered Warehouses"
        )

        search_text = st.text_input(
            "🔎 بحث"
            if ar
            else "🔎 Search",
            key="warehouse_search"
        )

        try:

            warehouses = get_warehouses(
                search_text.strip()
            )

            if not warehouses:

                st.info(
                    "لا توجد مخازن مسجلة."
                    if ar
                    else
                    "No warehouses registered."
                )

            else:

                st.caption(
                    (
                        f"عدد المخازن: {len(warehouses)}"
                        if ar
                        else
                        f"Warehouses: {len(warehouses)}"
                    )
                )

                type_labels_ar = {
                    "general": "عام",
                    "main": "رئيسي",
                    "raw_materials": "مواد خام",
                    "finished_goods": "منتجات تامة",
                    "spare_parts": "قطع غيار",
                    "transit": "ترانزيت",
                    "returns": "مرتجعات"
                }

                for warehouse in warehouses:

                    warehouse_name = (
                        warehouse["name_ar"]
                        if ar and warehouse["name_ar"]
                        else warehouse["name_en"]
                    )

                    if not warehouse_name:
                        warehouse_name = warehouse["warehouse_code"]

                    company_name = (
                        warehouse["company_name_ar"]
                        if ar and warehouse["company_name_ar"]
                        else warehouse["company_name_en"]
                    )

                    if not company_name:
                        company_name = warehouse["company_code"]

                    branch_name = (
                        warehouse["branch_name_ar"]
                        if ar and warehouse["branch_name_ar"]
                        else warehouse["branch_name_en"]
                    )

                    if not branch_name:
                        branch_name = warehouse["branch_code"]

                    with st.expander(
                        f"🏬 {warehouse['warehouse_code']} - "
                        f"{warehouse_name}"
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
                                    "الفرع"
                                    if ar
                                    else "Branch"
                                ) +
                                ":**",
                                branch_name
                            )

                            st.write(
                                "**" +
                                (
                                    "كود المخزن"
                                    if ar
                                    else "Warehouse Code"
                                ) +
                                ":**",
                                warehouse["warehouse_code"]
                            )

                        with col2:

                            warehouse_type_text = (
                                type_labels_ar.get(
                                    warehouse["warehouse_type"],
                                    warehouse["warehouse_type"]
                                )
                                if ar
                                else warehouse["warehouse_type"]
                                .replace("_", " ")
                                .title()
                            )

                            st.write(
                                "**" +
                                (
                                    "نوع المخزن"
                                    if ar
                                    else "Warehouse Type"
                                ) +
                                ":**",
                                warehouse_type_text
                            )

                            st.write(
                                "**" +
                                (
                                    "المدينة"
                                    if ar
                                    else "City"
                                ) +
                                ":**",
                                warehouse["city"] or "-"
                            )

                            st.write(
                                "**" +
                                (
                                    "مسؤول المخزن"
                                    if ar
                                    else "Manager"
                                ) +
                                ":**",
                                warehouse["manager_name"] or "-"
                            )

                        with col3:

                            negative_stock_text = (
                                "مسموح"
                                if ar and warehouse["allow_negative_stock"]
                                else
                                "غير مسموح"
                                if ar
                                else
                                "Allowed"
                                if warehouse["allow_negative_stock"]
                                else
                                "Not Allowed"
                            )

                            st.write(
                                "**" +
                                (
                                    "المخزون السالب"
                                    if ar
                                    else "Negative Stock"
                                ) +
                                ":**",
                                negative_stock_text
                            )

                            current_status = warehouse["status"]

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
                                "⛔ إيقاف المخزن"
                                if ar
                                else "⛔ Deactivate Warehouse",
                                key=f"deactivate_warehouse_{warehouse['id']}"
                            ):

                                change_warehouse_status(
                                    warehouse["id"],
                                    "inactive",
                                    username
                                )

                                st.rerun()

                        else:

                            if st.button(
                                "✅ تفعيل المخزن"
                                if ar
                                else "✅ Activate Warehouse",
                                key=f"activate_warehouse_{warehouse['id']}"
                            ):

                                change_warehouse_status(
                                    warehouse["id"],
                                    "active",
                                    username
                                )

                                st.rerun()

        except Exception as error:

            st.error(
                "حدث خطأ أثناء تحميل المخازن."
                if ar
                else
                "An error occurred while loading warehouses."
            )

            st.code(str(error))
