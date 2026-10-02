import streamlit as st


# ============================================================
# ERP SYSTEM KHALED & SHERIF
# ASK AI MODULE
# ============================================================


def show_ask_ai(language):

    ar = language == "العربية"

    st.title(
        "🤖 " +
        (
            "اسأل الذكاء الاصطناعي"
            if ar
            else "Ask AI"
        )
    )

    st.caption(
        (
            "مساعد ذكي لتحليل بيانات نظام ERP والإجابة عن أسئلتك."
        )
        if ar
        else
        (
            "AI assistant for analyzing ERP data and answering your questions."
        )
    )

    st.divider()

    # ==========================================
    # WELCOME MESSAGE
    # ==========================================

    st.info(
        (
            "يمكنك لاحقًا سؤال النظام عن المبيعات والمشتريات "
            "والمخزون والحسابات والعملاء والموردين والتقارير."
        )
        if ar
        else
        (
            "You will be able to ask about sales, purchases, "
            "inventory, accounting, customers, suppliers and reports."
        )
    )

    # ==========================================
    # EXAMPLE QUESTIONS
    # ==========================================

    st.subheader(
        "أمثلة للأسئلة"
        if ar
        else "Example Questions"
    )

    if ar:

        st.markdown(
            """
            - ما إجمالي المبيعات هذا الشهر؟
            - ما الأصناف التي قاربت على النفاد؟
            - من العملاء المتأخرين في السداد؟
            - ما إجمالي أرصدة الموردين؟
            - قارن مبيعات هذا الشهر بالشهر السابق.
            - ما أكثر المنتجات مبيعًا؟
            - اعرض ملخص الأرباح والمصروفات.
            """
        )

    else:

        st.markdown(
            """
            - What are total sales this month?
            - Which products are running low?
            - Which customers have overdue balances?
            - What are the total supplier balances?
            - Compare this month's sales with last month.
            - What are the best-selling products?
            - Show a summary of profit and expenses.
            """
        )

    st.divider()

    # ==========================================
    # AI QUESTION
    # ==========================================

    question = st.text_area(
        "اكتب سؤالك هنا"
        if ar
        else "Ask your question",
        height=120,
        placeholder=(
            "مثال: ما إجمالي مبيعات فرع مصراتة هذا الشهر؟"
            if ar
            else
            "Example: What are total sales for Misrata branch this month?"
        )
    )

    # ==========================================
    # ASK BUTTON
    # ==========================================

    if st.button(
        "🤖 اسأل AI"
        if ar
        else "🤖 Ask AI",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "اكتب السؤال أولًا."
                if ar
                else
                "Please enter a question first."
            )

        else:

            st.info(
                (
                    "تم تجهيز واجهة Ask AI بنجاح. "
                    "سيتم ربط محرك الذكاء الاصطناعي وبيانات ERP "
                    "في مرحلة الربط القادمة."
                )
                if ar
                else
                (
                    "Ask AI interface is ready. "
                    "The AI engine and ERP data will be connected "
                    "in the integration stage."
                )
            )


# ============================================================
# FUTURE AI FEATURES
# ============================================================
#
# 1. ERP database context
# 2. User permissions
# 3. Sales analysis
# 4. Inventory analysis
# 5. Accounting analysis
# 6. Customer / Supplier analysis
# 7. Report generation
# 8. PDF / Excel reports
# 9. AI provider selection
# 10. Audit logging
#
# IMPORTANT:
# AI must never access ERP information outside
# the logged-in user's permissions.
#
# Any AI action that changes ERP data must require
# explicit user confirmation before execution.
#
# ============================================================
