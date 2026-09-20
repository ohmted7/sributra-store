import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "receipts.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_number TEXT,
                date TEXT,
                time TEXT,
                store_name TEXT DEFAULT 'ร้านโดนใจ',
                branch TEXT,
                total_amount REAL DEFAULT 0.0,
                subtotal_amount REAL DEFAULT 0.0,
                vat_amount REAL DEFAULT 0.0,
                payment_method TEXT,
                raw_file TEXT,
                markdown_file TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipt_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER,
                item_name TEXT NOT NULL,
                quantity REAL DEFAULT 1.0,
                unit_price REAL DEFAULT 0.0,
                total_price REAL DEFAULT 0.0,
                FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bank_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_no TEXT DEFAULT '6153107532',
                date TEXT,
                time TEXT,
                tx_type TEXT,
                description TEXT,
                withdrawal REAL DEFAULT 0.0,
                deposit REAL DEFAULT 0.0,
                balance REAL DEFAULT 0.0,
                channel TEXT,
                branch TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def insert_receipt(receipt_data: Dict[str, Any], items: List[Dict[str, Any]] = None) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Check if duplicate receipt exists
        existing = None
        rec_num = str(receipt_data.get("receipt_number", "")).strip()
        new_total = float(receipt_data.get("total_amount", 0.0))
        
        # 1. Primary: Receipt Number (if actual business invoice/receipt number)
        if rec_num and not rec_num.startswith("REC-") and not rec_num.startswith("IMG-") and not rec_num.startswith("INV-") and len(rec_num) >= 5:
            cursor.execute("SELECT id, total_amount, vat_amount, receipt_number FROM receipts WHERE receipt_number = ?", (rec_num,))
            existing = cursor.fetchone()
            
        # 2. Secondary: Raw file name
        if not existing and receipt_data.get("raw_file"):
            cursor.execute("SELECT id, total_amount, vat_amount, receipt_number FROM receipts WHERE raw_file = ?", (receipt_data["raw_file"],))
            existing = cursor.fetchone()

        # 3. Tertiary: Same store + Same date + Same total amount (prevent duplicate snaps of same bill)
        if not existing and new_total > 0 and receipt_data.get("store_name") not in ["ร้านค้าทั่วไป", "รูปถ่าย (รอระบุยอดเงิน)"]:
            cursor.execute("""
                SELECT id, total_amount, vat_amount, receipt_number FROM receipts 
                WHERE store_name = ? AND date = ? AND ABS(total_amount - ?) < 0.01
            """, (receipt_data.get("store_name", ""), receipt_data.get("date", ""), new_total))
            existing = cursor.fetchone()

        if existing:
            receipt_id = existing["id"]
            cur_total = float(existing["total_amount"] or 0.0)
            # If current total is already the full grand total, preserve it
            final_total = max(cur_total, new_total)
            final_vat = float(receipt_data.get("vat_amount", 0.0)) if new_total >= cur_total else float(existing["vat_amount"] or 0.0)
            final_subtotal = float(receipt_data.get("subtotal_amount", 0.0)) if new_total >= cur_total else round(final_total - final_vat, 2)
            final_store = receipt_data.get("store_name") if receipt_data.get("store_name") not in ["ร้านค้าทั่วไป", "รูปถ่าย (รอระบุยอดเงิน)"] else existing.get("store_name", "ร้านโดนใจ")
            final_rec_num = rec_num if (rec_num and not rec_num.startswith("IMG-")) else existing["receipt_number"]

            cursor.execute("""
                UPDATE receipts SET
                    receipt_number = ?, date = ?, time = ?, store_name = ?, branch = ?,
                    total_amount = ?, subtotal_amount = ?, vat_amount = ?, payment_method = ?,
                    raw_file = ?, markdown_file = ?, notes = ?
                WHERE id = ?
            """, (
                final_rec_num,
                receipt_data.get("date", datetime.today().strftime("%Y-%m-%d")),
                receipt_data.get("time", ""),
                final_store,
                receipt_data.get("branch", ""),
                final_total,
                final_subtotal,
                final_vat,
                receipt_data.get("payment_method", ""),
                receipt_data.get("raw_file", ""),
                receipt_data.get("markdown_file", ""),
                receipt_data.get("notes", ""),
                receipt_id
            ))
            if items:
                cursor.execute("DELETE FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        else:
            cursor.execute("""
                INSERT INTO receipts (
                    receipt_number, date, time, store_name, branch,
                    total_amount, subtotal_amount, vat_amount, payment_method,
                    raw_file, markdown_file, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                receipt_data.get("receipt_number", ""),
                receipt_data.get("date", datetime.today().strftime("%Y-%m-%d")),
                receipt_data.get("time", ""),
                receipt_data.get("store_name", "ร้านโดนใจ"),
                receipt_data.get("branch", ""),
                float(receipt_data.get("total_amount", 0.0)),
                float(receipt_data.get("subtotal_amount", 0.0)),
                float(receipt_data.get("vat_amount", 0.0)),
                receipt_data.get("payment_method", ""),
                receipt_data.get("raw_file", ""),
                receipt_data.get("markdown_file", ""),
                receipt_data.get("notes", "")
            ))
            receipt_id = cursor.lastrowid
        
        if items:
            for item in items:
                cursor.execute("""
                    INSERT INTO receipt_items (receipt_id, item_name, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    receipt_id,
                    item.get("item_name", "สินค้า"),
                    float(item.get("quantity", 1.0)),
                    float(item.get("unit_price", 0.0)),
                    float(item.get("total_price", 0.0))
                ))
                
        conn.commit()
        return receipt_id

def delete_receipt(receipt_id: int) -> bool:
    """Delete a receipt and its associated items from database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        cursor.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
        conn.commit()
        return True

def update_receipt(receipt_id: int, updated_data: Dict[str, Any]) -> bool:
    """Update receipt header information."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE receipts SET
                receipt_number = ?,
                date = ?,
                time = ?,
                store_name = ?,
                branch = ?,
                total_amount = ?,
                subtotal_amount = ?,
                vat_amount = ?,
                payment_method = ?,
                notes = ?
            WHERE id = ?
        """, (
            updated_data.get("receipt_number", ""),
            updated_data.get("date", ""),
            updated_data.get("time", ""),
            updated_data.get("store_name", "ร้านโดนใจ"),
            updated_data.get("branch", ""),
            float(updated_data.get("total_amount", 0.0)),
            float(updated_data.get("subtotal_amount", 0.0)),
            float(updated_data.get("vat_amount", 0.0)),
            updated_data.get("payment_method", ""),
            updated_data.get("notes", ""),
            receipt_id
        ))
        conn.commit()
        return True

def get_receipts(start_date: Optional[str] = None, end_date: Optional[str] = None, 
                 search: Optional[str] = None, store: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM receipts WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if store and store != "ทั้งหมด":
            if "การไฟฟ้า" in store:
                query += " AND store_name LIKE '%การไฟฟ้า%'"
            elif "แม็คโคร" in store or "Makro" in store:
                query += " AND (store_name LIKE '%แม็คโคร%' OR store_name LIKE '%Makro%')"
            elif "บิ๊กซี" in store or "Big C" in store:
                query += " AND (store_name LIKE '%บิ๊กซี%' OR store_name LIKE '%Big C%')"
            elif "เอส.อาร์" in store:
                query += " AND store_name LIKE '%เอส.อาร์%'"
            else:
                query += " AND store_name = ?"
                params.append(store)
        if search:
            query += " AND (receipt_number LIKE ? OR notes LIKE ? OR branch LIKE ?)"
            wildcard = f"%{search}%"
            params.extend([wildcard, wildcard, wildcard])
            
        query += " ORDER BY date DESC, id DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_receipt_detail(receipt_id: int) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,))
        receipt_row = cursor.fetchone()
        if not receipt_row:
            return {}
        
        receipt = dict(receipt_row)
        cursor.execute("SELECT * FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        receipt["items"] = [dict(row) for row in cursor.fetchall()]
        return receipt

def get_kpis(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total, COALESCE(SUM(vat_amount), 0) as total_vat, COALESCE(AVG(total_amount), 0) as avg_amount FROM receipts WHERE 1=1"
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else {"count": 0, "total": 0.0, "total_vat": 0.0, "avg_amount": 0.0}

def get_spending_trend(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT date, SUM(total_amount) as total_spent, COUNT(*) as receipt_count FROM receipts WHERE 1=1"
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
            
        query += " GROUP BY date ORDER BY date ASC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_top_items(limit: int = 10, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT ri.item_name, SUM(ri.quantity) as total_qty, SUM(ri.total_price) as total_spend
            FROM receipt_items ri
            JOIN receipts r ON ri.receipt_id = r.id
            WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND r.date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND r.date <= ?"
            params.append(end_date)
            
        query += " GROUP BY ri.item_name ORDER BY total_spend DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_store_breakdown() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT store_name, COUNT(*) as count, SUM(total_amount) as total_amount
            FROM receipts
            GROUP BY store_name
            ORDER BY total_amount DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_goods_purchases(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                COUNT(*) as receipt_count, 
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(vat_amount), 0) as total_vat,
                COALESCE(SUM(subtotal_amount), 0) as total_subtotal
            FROM receipts 
            WHERE store_name NOT LIKE '%การไฟฟ้า%'
        """
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else {"receipt_count": 0, "total_amount": 0.0, "total_vat": 0.0, "total_subtotal": 0.0}

def get_utility_expenses(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                COUNT(*) as bill_count, 
                COALESCE(SUM(total_amount), 0) as total_amount,
                COALESCE(SUM(vat_amount), 0) as total_vat,
                COALESCE(SUM(subtotal_amount), 0) as total_subtotal
            FROM receipts 
            WHERE store_name LIKE '%การไฟฟ้า%'
        """
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else {"bill_count": 0, "total_amount": 0.0, "total_vat": 0.0, "total_subtotal": 0.0}


def insert_bank_transactions_bulk(tx_list: List[Dict[str, Any]]) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        inserted = 0
        for tx in tx_list:
            cursor.execute("""
                SELECT id FROM bank_transactions 
                WHERE date = ? AND time = ? AND tx_type = ? AND withdrawal = ? AND deposit = ?
            """, (tx["date"], tx["time"], tx["type"], tx["withdrawal"], tx["deposit"]))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO bank_transactions (
                        account_no, date, time, tx_type, description,
                        withdrawal, deposit, balance, channel, branch
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tx.get("account_no", "6153107532"),
                    tx["date"], tx["time"], tx["type"], tx.get("desc", ""),
                    float(tx.get("withdrawal", 0.0)),
                    float(tx.get("deposit", 0.0)),
                    float(tx.get("balance", 0.0)),
                    tx.get("channel", "Other"),
                    tx.get("branch", "")
                ))
                inserted += 1
        conn.commit()
        return inserted

def get_bank_summary(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                COUNT(*) as tx_count,
                COALESCE(SUM(deposit), 0) as total_deposit,
                COALESCE(SUM(withdrawal), 0) as total_withdrawal,
                SUM(CASE WHEN deposit > 0 THEN 1 ELSE 0 END) as deposit_count,
                SUM(CASE WHEN withdrawal > 0 THEN 1 ELSE 0 END) as withdrawal_count
            FROM bank_transactions WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else {
            "tx_count": 0, "total_deposit": 0.0, "total_withdrawal": 0.0,
            "deposit_count": 0, "withdrawal_count": 0
        }

def get_revenue_by_channel(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT channel, COUNT(*) as count, SUM(deposit) as total_amount
            FROM bank_transactions
            WHERE deposit > 0
        """
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        query += " GROUP BY channel ORDER BY total_amount DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_daily_bank_inflows(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT date, SUM(deposit) as daily_inflow, SUM(withdrawal) as daily_outflow, COUNT(*) as tx_count
            FROM bank_transactions
            WHERE 1=1
        """
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        query += " GROUP BY date ORDER BY date ASC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_bank_transactions(start_date: Optional[str] = None, end_date: Optional[str] = None, channel: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM bank_transactions WHERE 1=1"
        params = []
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if channel and channel != "ทั้งหมด":
            query += " AND channel = ?"
            params.append(channel)
        query += " ORDER BY date ASC, time ASC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)

