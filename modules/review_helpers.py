import streamlit as st

def review_header(language, icon, ar_title, en_title, ar_desc, en_desc):
    ar = language == "العربية"
    st.title(f"{icon} {ar_title if ar else en_title}")
    st.caption(ar_desc if ar else en_desc)
    st.info(
        "نسخة مراجعة للواجهة والحقول قبل تفعيل العمليات والترحيل النهائي."
        if ar else
        "Review-stage screen for approving fields and workflow before final posting logic."
    )
    return ar

def status_box(ar):
    c1, c2, c3 = st.columns(3)
    c1.metric("الحالة" if ar else "Status", "مراجعة" if ar else "Review")
    c2.metric("الربط" if ar else "Integration", "لاحقًا" if ar else "Next phase")
    c3.metric("الصلاحيات" if ar else "Permissions", "مخطط" if ar else "Planned")

def text_pair(ar, key, left_ar, left_en, right_ar, right_en):
    c1, c2 = st.columns(2)
    with c1:
        a = st.text_input(left_ar if ar else left_en, key=f"{key}_1")
    with c2:
        b = st.text_input(right_ar if ar else right_en, key=f"{key}_2")
    return a, b
