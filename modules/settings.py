import streamlit as st
from ui.theme import get_theme, set_theme, DEFAULT_THEME


SECTIONS = [
    "الشركة|Company",
    "الترقيم|Document Sequences",
    "الضرائب|Taxes",
    "اللغة والمظهر|Language & Appearance",
    "المزامنة|Synchronization",
    "النسخ الاحتياطي|Backup",
]


def show_settings(language):
    ar = language == "العربية"

    st.title("⚙️ " + ("إعدادات النظام" if ar else "System Settings"))

    labels = [
        item.split("|")[0] if ar else item.split("|")[1]
        for item in SECTIONS
    ]

    tabs = st.tabs(labels)

    with tabs[0]:
        st.subheader("إعدادات الشركة" if ar else "Company Settings")
        c1, c2 = st.columns(2)
        c1.text_input("اسم الشركة الافتراضية" if ar else "Default Company")
        c2.text_input("الرقم الضريبي" if ar else "Tax Number")
        st.text_area("العنوان" if ar else "Address")
        st.button("💾 حفظ إعدادات الشركة" if ar else "💾 Save Company Settings")

    with tabs[1]:
        st.subheader("ترقيم المستندات" if ar else "Document Sequences")
        st.data_editor(
            [
                {
                    ("المستند" if ar else "Document"): "",
                    ("البادئة" if ar else "Prefix"): "",
                    ("الرقم التالي" if ar else "Next Number"): 1,
                }
            ],
            num_rows="dynamic",
            use_container_width=True,
        )

    with tabs[2]:
        st.subheader("الضرائب" if ar else "Taxes")
        st.data_editor(
            [
                {
                    ("اسم الضريبة" if ar else "Tax Name"): "",
                    ("النسبة %" if ar else "Rate %"): 0.0,
                    ("نشطة" if ar else "Active"): True,
                }
            ],
            num_rows="dynamic",
            use_container_width=True,
        )

    with tabs[3]:
        st.subheader("🎨 " + ("اللغة والمظهر" if ar else "Language & Appearance"))

        current = get_theme()

        st.caption(
            "التغييرات تطبق على النظام بالكامل بعد الضغط على تطبيق المظهر."
            if ar
            else "Changes are applied across the system after pressing Apply Theme."
        )

        c1, c2 = st.columns(2)

        with c1:
            primary_color = st.color_picker(
                "اللون الرئيسي" if ar else "Primary Color",
                current["primary_color"],
            )

            button_color = st.color_picker(
                "لون الأزرار" if ar else "Button Color",
                current["button_color"],
            )

            background_color = st.color_picker(
                "لون الخلفية" if ar else "Background Color",
                current["background_color"],
            )

        with c2:
            sidebar_color = st.color_picker(
                "لون القائمة الجانبية" if ar else "Sidebar Color",
                current["sidebar_color"],
            )

            text_color = st.color_picker(
                "لون النص" if ar else "Text Color",
                current["text_color"],
            )

            font_family = st.selectbox(
                "نوع الخط" if ar else "Font Family",
                ["Arial", "Tahoma", "Verdana", "Trebuchet MS", "Georgia"],
                index=["Arial", "Tahoma", "Verdana", "Trebuchet MS", "Georgia"].index(
                    current["font_family"]
                    if current["font_family"] in ["Arial", "Tahoma", "Verdana", "Trebuchet MS", "Georgia"]
                    else "Arial"
                ),
            )

        font_size = st.slider(
            "حجم الخط" if ar else "Font Size",
            12,
            24,
            int(current["font_size"]),
        )

        mode = st.radio(
            "الوضع" if ar else "Mode",
            ["فاتح", "داكن"] if ar else ["Light", "Dark"],
            horizontal=True,
        )

        col_apply, col_reset = st.columns(2)

        with col_apply:
            if st.button(
                "🎨 تطبيق المظهر" if ar else "🎨 Apply Theme",
                type="primary",
                use_container_width=True,
            ):
                set_theme(
                    {
                        "primary_color": primary_color,
                        "button_color": button_color,
                        "background_color": background_color,
                        "sidebar_color": sidebar_color,
                        "text_color": text_color,
                        "font_family": font_family,
                        "font_size": font_size,
                        "mode": "dark" if mode in ["داكن", "Dark"] else "light",
                    }
                )
                st.success("تم تطبيق المظهر." if ar else "Theme applied.")
                st.rerun()

        with col_reset:
            if st.button(
                "↩️ استعادة الافتراضي" if ar else "↩️ Reset Default",
                use_container_width=True,
            ):
                set_theme(DEFAULT_THEME)
                st.rerun()

    with tabs[4]:
        st.subheader("المزامنة" if ar else "Synchronization")
        st.checkbox("تفعيل المزامنة التلقائية" if ar else "Enable Automatic Sync", value=True)
        st.number_input(
            "فترة المزامنة بالدقائق" if ar else "Sync Interval (minutes)",
            min_value=1,
            value=5,
        )

    with tabs[5]:
        st.subheader("النسخ الاحتياطي" if ar else "Backup")
        st.checkbox("نسخ احتياطي تلقائي" if ar else "Automatic Backup", value=True)
        st.selectbox(
            "التكرار" if ar else "Frequency",
            ["يومي", "أسبوعي", "شهري"] if ar else ["Daily", "Weekly", "Monthly"],
        )
        st.button("إنشاء نسخة احتياطية الآن" if ar else "Create Backup Now")
