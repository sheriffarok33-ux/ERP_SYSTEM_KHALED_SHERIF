import streamlit as st
import uuid
from datetime import date
from core.database import local_database


def _rows(sql, params=()):
    with local_database() as db:
        return [dict(r) for r in db.execute(sql, params).fetchall()]


def _next_number(company_id, branch_id, document_type, prefix):
    with local_database() as db:
        row = db.execute(
            """SELECT id, current_number, padding FROM document_sequences
               WHERE company_id=? AND (branch_id=? OR (branch_id IS NULL AND ? IS NULL))
               AND document_type=? ORDER BY id DESC LIMIT 1""",
            (company_id, branch_id, branch_id, document_type),
        ).fetchone()
        if row:
            number = int(row["current_number"]) + 1
            db.execute("UPDATE document_sequences SET current_number=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                       (number, row["id"]))
            padding = int(row["padding"] or 6)
        else:
            number, padding = 1, 6
            db.execute(
                """INSERT INTO document_sequences
                   (company_id, branch_id, document_type, prefix, current_number, padding)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (company_id, branch_id, document_type, prefix, number, padding),
            )
        return f"{prefix}{str(number).zfill(padding)}"


def _margin(price, cost):
    return ((price - cost) / price * 100) if price else 0.0


def show_purchases(language):
    ar = language == "العربية"
    st.title("🧾 " + ("المشتريات والتكلفة والتسعير" if ar else "Purchasing, Cost & Pricing"))

    companies = _rows("SELECT id, company_code, name_ar, name_en FROM companies WHERE status='active' AND is_deleted=0 ORDER BY company_code")
    if not companies:
        st.warning("أضف شركة أولًا." if ar else "Please add a company first.")
        return

    company_labels = {
        f'{c["company_code"]} - {(c["name_ar"] if ar else c["name_en"]) or c["name_ar"] or c["name_en"] or ""}': c["id"]
        for c in companies
    }
    selected_company = st.selectbox("الشركة" if ar else "Company", list(company_labels))
    company_id = company_labels[selected_company]

    branches = _rows("SELECT id, branch_code, name_ar, name_en FROM branches WHERE company_id=? AND status='active' AND is_deleted=0 ORDER BY branch_code", (company_id,))
    branch_labels = {
        f'{b["branch_code"]} - {(b["name_ar"] if ar else b["name_en"]) or b["name_ar"] or b["name_en"] or ""}': b["id"]
        for b in branches
    }
    branch_id = branch_labels[st.selectbox("الفرع" if ar else "Branch", list(branch_labels))] if branch_labels else None

    tabs = st.tabs(
        ["📋 طلب شراء","📝 أمر شراء","🧾 فاتورة شراء","↩️ مرتجع مشتريات","📊 مقارنة التكلفة","🏷️ اعتماد الأسعار"]
        if ar else
        ["📋 Purchase Request","📝 Purchase Order","🧾 Purchase Invoice","↩️ Purchase Return","📊 Cost Comparison","🏷️ Price Approval"]
    )

    with tabs[0]:
        st.info("سيتم ربط طلبات الشراء وأوامر الشراء في المرحلة التالية بعد تثبيت دورة فاتورة الشراء والمخزون."
                if ar else "Purchase Requests and Purchase Orders will be connected after the purchase-invoice/inventory workflow is stabilized.")

    with tabs[1]:
        st.info("سيتم ربط أوامر الشراء في المرحلة التالية."
                if ar else "Purchase Orders will be connected in the next stage.")

    with tabs[2]:
        warehouses = _rows("""SELECT id, warehouse_code, name_ar, name_en FROM warehouses
                              WHERE company_id=? AND status='active' AND is_deleted=0
                              ORDER BY warehouse_code""", (company_id,))
        suppliers = _rows("""SELECT id, party_code, name_ar, name_en FROM business_parties
                             WHERE company_id=? AND party_type IN ('supplier','both')
                             AND status='active' AND is_deleted=0 ORDER BY party_code""", (company_id,))
        items = _rows("""SELECT id, item_code, name_ar, name_en, purchase_cost, sale_price
                         FROM items WHERE company_id=? AND status='active' AND is_deleted=0 ORDER BY item_code""", (company_id,))

        if not warehouses:
            st.warning("لا يوجد مخزن نشط لهذه الشركة." if ar else "No active warehouse exists for this company.")
        if not suppliers:
            st.warning("لا يوجد مورد مسجل بعد. أضف المورد من العملاء والموردين." if ar else "No supplier exists yet. Add one from CRM.")
        if not items:
            st.warning("لا توجد أصناف مسجلة بعد. أضف الأصناف من المخزون." if ar else "No items exist yet. Add items from Inventory.")

        c1,c2,c3 = st.columns(3)
        supplier_map = {f'{x["party_code"]} - {(x["name_ar"] if ar else x["name_en"]) or x["name_ar"] or x["name_en"] or ""}': x["id"] for x in suppliers}
        warehouse_map = {f'{x["warehouse_code"]} - {(x["name_ar"] if ar else x["name_en"]) or x["name_ar"] or x["name_en"] or ""}': x["id"] for x in warehouses}
        supplier_label = c1.selectbox("المورد" if ar else "Supplier", list(supplier_map) if supplier_map else [""])
        warehouse_label = c2.selectbox("المخزن" if ar else "Warehouse", list(warehouse_map) if warehouse_map else [""])
        invoice_date = c3.date_input("تاريخ الفاتورة" if ar else "Invoice Date", value=date.today())

        c4,c5,c6 = st.columns(3)
        supplier_invoice = c4.text_input("رقم فاتورة المورد" if ar else "Supplier Invoice No.")
        currency = c5.text_input("العملة" if ar else "Currency", value="LYD")
        exchange_rate = c6.number_input("سعر الصرف" if ar else "Exchange Rate", min_value=0.000001, value=1.0)

        uploaded = st.file_uploader("تحميل صورة/PDF/Excel للفاتورة" if ar else "Upload invoice image/PDF/Excel",
                                    type=["pdf","png","jpg","jpeg","xlsx","xls"])

        item_map = {f'{x["item_code"]} - {(x["name_ar"] if ar else x["name_en"]) or x["name_ar"] or x["name_en"] or ""}': x["id"] for x in items}
        blank_item = next(iter(item_map), "")
        columns = ["الصنف","الكمية","سعر الشراء","خصم","ضريبة"] if ar else ["Item","Qty","Purchase Price","Discount","Tax"]
        initial = [{columns[0]: blank_item, columns[1]: 1.0, columns[2]: 0.0, columns[3]: 0.0, columns[4]: 0.0}]
        edited = st.data_editor(
            initial, num_rows="dynamic", use_container_width=True,
            column_config={
                columns[0]: st.column_config.SelectboxColumn(columns[0], options=list(item_map), required=True),
                columns[1]: st.column_config.NumberColumn(columns[1], min_value=0.0),
                columns[2]: st.column_config.NumberColumn(columns[2], min_value=0.0),
                columns[3]: st.column_config.NumberColumn(columns[3], min_value=0.0),
                columns[4]: st.column_config.NumberColumn(columns[4], min_value=0.0),
            },
            key="purchase_invoice_lines_editor",
        )

        threshold = st.number_input("نسبة التنبيه عند تغير التكلفة %" if ar else "Cost Change Alert %", min_value=0.0, value=5.0, key="purchase_threshold")
        target_margin = st.number_input("هامش الربح المستهدف %" if ar else "Target Margin %", min_value=0.0, max_value=99.0, value=20.0)

        if st.button("💾 حفظ الفاتورة وترحيلها للمخزون والمقارنة" if ar else "💾 Save Invoice, Post Inventory & Compare Costs",
                     type="primary", disabled=not (supplier_map and warehouse_map and item_map)):
            try:
                supplier_id = supplier_map[supplier_label]
                warehouse_id = warehouse_map[warehouse_label]
                valid = []
                for row in edited:
                    item_label = row.get(columns[0])
                    qty = float(row.get(columns[1]) or 0)
                    unit_cost = float(row.get(columns[2]) or 0)
                    discount = float(row.get(columns[3]) or 0)
                    tax = float(row.get(columns[4]) or 0)
                    if item_label in item_map and qty > 0:
                        valid.append((item_map[item_label], qty, unit_cost, discount, tax))
                if not valid:
                    st.error("أدخل صنفًا وكمية صحيحة." if ar else "Enter at least one valid item and quantity.")
                else:
                    username = st.session_state.get("username", "system")
                    with local_database() as db:
                        # Allocate sequence inside the same DB transaction manually.
                        seq = db.execute("""SELECT id,current_number,padding FROM document_sequences
                                          WHERE company_id=? AND (branch_id=? OR (branch_id IS NULL AND ? IS NULL))
                                          AND document_type='purchase_invoice' ORDER BY id DESC LIMIT 1""",
                                         (company_id, branch_id, branch_id)).fetchone()
                        if seq:
                            n = int(seq["current_number"]) + 1
                            db.execute("UPDATE document_sequences SET current_number=?,updated_at=CURRENT_TIMESTAMP WHERE id=?", (n,seq["id"]))
                            padding = int(seq["padding"] or 6)
                        else:
                            n,padding = 1,6
                            db.execute("""INSERT INTO document_sequences
                                      (company_id,branch_id,document_type,prefix,current_number,padding)
                                      VALUES (?,?,?,?,?,?)""",
                                      (company_id,branch_id,"purchase_invoice","PI-",n,padding))
                        internal_no = "PI-" + str(n).zfill(padding)

                        subtotal = sum(q*c for _,q,c,_,_ in valid)
                        discount_total = sum(d for *_,d,t in valid)
                        tax_total = sum(t for *_,d,t in valid)
                        grand_total = subtotal - discount_total + tax_total

                        cur = db.execute("""INSERT INTO purchase_invoices
                            (invoice_uuid,company_id,branch_id,warehouse_id,supplier_id,internal_number,
                             supplier_invoice_number,invoice_date,currency_code,exchange_rate,subtotal,
                             discount_total,tax_total,grand_total,status,attachment_name,created_by,sync_status)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (str(uuid.uuid4()),company_id,branch_id,warehouse_id,supplier_id,internal_no,
                             supplier_invoice,str(invoice_date),currency,exchange_rate,subtotal,discount_total,
                             tax_total,grand_total,"posted",uploaded.name if uploaded else None,username,"pending"))
                        invoice_id = cur.lastrowid

                        for item_id, qty, new_cost, discount, tax in valid:
                            item = db.execute("SELECT purchase_cost,sale_price FROM items WHERE id=?", (item_id,)).fetchone()
                            old_cost = float(item["purchase_cost"] or 0)
                            old_price = float(item["sale_price"] or 0)
                            change = ((new_cost-old_cost)/old_cost*100) if old_cost else (100.0 if new_cost else 0.0)
                            line_total = qty*new_cost-discount+tax
                            db.execute("""INSERT INTO purchase_invoice_lines
                                (invoice_id,item_id,quantity,unit_cost,discount,tax,line_total,previous_cost,cost_change_percent)
                                VALUES (?,?,?,?,?,?,?,?,?)""",
                                (invoice_id,item_id,qty,new_cost,discount,tax,line_total,old_cost,change))
                            db.execute("""INSERT INTO inventory_movements
                                (movement_uuid,company_id,branch_id,warehouse_id,item_id,movement_type,quantity,
                                 unit_cost,reference_type,reference_id,created_by,sync_status)
                                VALUES (?,?,?,?,?,'purchase',?,?,?,?,?,?)""",
                                (str(uuid.uuid4()),company_id,branch_id,warehouse_id,item_id,qty,new_cost,
                                 "purchase_invoice",invoice_id,username,"pending"))

                            # Purchase cost is updated; sale price remains untouched until management approval.
                            db.execute("UPDATE items SET purchase_cost=?,updated_at=CURRENT_TIMESTAMP,sync_status='pending' WHERE id=?",
                                       (new_cost,item_id))

                            if abs(change) >= threshold:
                                suggested = new_cost / (1 - target_margin/100) if target_margin < 100 else old_price
                                db.execute("""INSERT INTO price_change_requests
                                    (request_uuid,company_id,purchase_invoice_id,item_id,old_cost,new_cost,cost_change_percent,
                                     old_sale_price,target_margin_percent,suggested_sale_price,status,requested_by,sync_status)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,'pending',?,'pending')""",
                                    (str(uuid.uuid4()),company_id,invoice_id,item_id,old_cost,new_cost,change,
                                     old_price,target_margin,suggested,username))

                        db.execute("""INSERT INTO audit_log(username,action,table_name,record_id,new_values)
                                      VALUES (?,?,?,?,?)""",
                                   (username,"POST_PURCHASE_INVOICE","purchase_invoices",str(invoice_id),
                                    f"internal_number={internal_no}; total={grand_total}"))
                    st.success(("تم حفظ وترحيل الفاتورة: " if ar else "Invoice saved and posted: ") + internal_no)
                    st.rerun()
            except Exception as e:
                st.error(("تعذر حفظ الفاتورة: " if ar else "Could not save invoice: ") + str(e))

    with tabs[3]:
        st.info("مرتجع المشتريات سيُربط بعد تثبيت دورة الفاتورة الأساسية." if ar else "Purchase Returns will be connected after the base invoice workflow is stabilized.")

    with tabs[4]:
        st.subheader("مقارنة التكلفة الفعلية" if ar else "Actual Cost Comparison")
        comparisons = _rows("""SELECT r.id, i.item_code, i.name_ar, i.name_en, r.old_cost, r.new_cost,
                                      r.cost_change_percent, r.old_sale_price, r.target_margin_percent,
                                      r.suggested_sale_price, r.status
                               FROM price_change_requests r JOIN items i ON i.id=r.item_id
                               WHERE r.company_id=? ORDER BY r.id DESC""", (company_id,))
        if comparisons:
            st.dataframe(comparisons, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مقارنات تكلفة بعد." if ar else "No cost comparisons yet.")

    with tabs[5]:
        st.subheader("طلبات تعديل الأسعار المعلقة" if ar else "Pending Price Change Requests")
        pending = _rows("""SELECT r.id, i.item_code, i.name_ar, i.name_en, r.old_sale_price,
                                  r.suggested_sale_price, r.cost_change_percent
                           FROM price_change_requests r JOIN items i ON i.id=r.item_id
                           WHERE r.company_id=? AND r.status='pending' ORDER BY r.id""", (company_id,))
        if not pending:
            st.info("لا توجد طلبات معلقة." if ar else "No pending requests.")
        else:
            labels = {
                f'#{r["id"]} - {r["item_code"]} - {(r["name_ar"] if ar else r["name_en"]) or r["name_ar"] or r["name_en"] or ""}': r
                for r in pending
            }
            selected = st.selectbox("طلب التسعير" if ar else "Price Request", list(labels))
            req = labels[selected]
            approved_price = st.number_input("السعر المعتمد" if ar else "Approved Price",
                                             min_value=0.0, value=float(req["suggested_sale_price"] or 0))
            note = st.text_input("ملاحظة الإدارة" if ar else "Management Note")
            c1,c2 = st.columns(2)

            if c1.button("✅ اعتماد السعر" if ar else "✅ Approve Price", type="primary"):
                username = st.session_state.get("username","system")
                with local_database() as db:
                    row = db.execute("SELECT * FROM price_change_requests WHERE id=? AND status='pending'", (req["id"],)).fetchone()
                    if row:
                        db.execute("UPDATE items SET sale_price=?,updated_at=CURRENT_TIMESTAMP,sync_status='pending' WHERE id=?",
                                   (approved_price,row["item_id"]))
                        db.execute("""INSERT INTO item_price_history
                            (company_id,item_id,old_price,new_price,reason,source_request_id,changed_by)
                            VALUES (?,?,?,?,?,?,?)""",
                            (company_id,row["item_id"],row["old_sale_price"],approved_price,note,req["id"],username))
                        db.execute("""UPDATE price_change_requests SET approved_sale_price=?,status='approved',
                                      reviewed_at=CURRENT_TIMESTAMP,reviewed_by=?,review_note=?,sync_status='pending'
                                      WHERE id=?""",
                                   (approved_price,username,note,req["id"]))
                        db.execute("""INSERT INTO audit_log(username,action,table_name,record_id,old_values,new_values)
                                      VALUES (?,?,?,?,?,?)""",
                                   (username,"APPROVE_SALE_PRICE","price_change_requests",str(req["id"]),
                                    str(row["old_sale_price"]),str(approved_price)))
                st.success("تم اعتماد السعر وتحديث الصنف." if ar else "Price approved and item updated.")
                st.rerun()

            if c2.button("❌ رفض الطلب" if ar else "❌ Reject Request"):
                username = st.session_state.get("username","system")
                with local_database() as db:
                    db.execute("""UPDATE price_change_requests SET status='rejected',reviewed_at=CURRENT_TIMESTAMP,
                                  reviewed_by=?,review_note=?,sync_status='pending' WHERE id=?""",
                               (username,note,req["id"]))
                    db.execute("""INSERT INTO audit_log(username,action,table_name,record_id,new_values)
                                  VALUES (?,?,?,?,?)""",
                               (username,"REJECT_SALE_PRICE","price_change_requests",str(req["id"]),note))
                st.success("تم رفض الطلب." if ar else "Request rejected.")
                st.rerun()
