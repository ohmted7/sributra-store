import os
import sys
import re
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from markitdown import MarkItDown
import fitz
import db

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent
EXTRACTED_DIR = PROJECT_DIR / "extracted_receipts"
CONVERTED_DIR = PROJECT_DIR / "converted_markdown"

THAI_MONTHS = {
    "มกราคม": "01", "กุมภาพันธ์": "02", "มีนาคม": "03", "เมษายน": "04",
    "พฤษภาคม": "05", "มิถุนายน": "06", "กรกฎาคม": "07", "สิงหาคม": "08",
    "กันยายน": "09", "ตุลาคม": "10", "พฤศจิกายน": "11", "ธันวาคม": "12",
    "ม.ค.": "01", "ก.พ.": "02", "มี.ค.": "03", "เม.ย.": "04",
    "พ.ค.": "05", "มิ.ย.": "06", "ก.ค.": "07", "ส.ค.": "08",
    "ก.ย.": "09", "ต.ค.": "10", "พ.ย.": "11", "ธ.ค.": "12"
}

_ocr_reader = None

def get_ocr_reader():
    global _ocr_reader
    if _ocr_reader is None:
        import easyocr
        _ocr_reader = easyocr.Reader(['en'], gpu=False)
    return _ocr_reader

def parse_thai_date(text: Optional[str]) -> str:
    if not text:
        return datetime.today().strftime("%Y-%m-%d")

    # Try YYYY-MM-DD
    match_iso = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', text)
    if match_iso:
        y, m, d = match_iso.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"
        
    # Try DD/MM/YYYY
    match_dm = re.search(r'(\d{1,2})[/](\d{1,2})[/](\d{4})', text)
    if match_dm:
        d, m, y = match_dm.groups()
        y_int = int(y)
        if y_int > 2500: # Buddhist era
            y_int -= 543
        return f"{y_int}-{int(m):02d}-{int(d):02d}"

    # Try DD/MM/YY
    match_dmy = re.search(r'(\d{1,2})[/](\d{1,2})[/](\d{2})', text)
    if match_dmy:
        d, m, y = match_dmy.groups()
        y_int = 2000 + int(y)
        if int(y) >= 65: # Buddhist era like 69 -> 2569 -> 2026
            y_int = 1957 + int(y)
        return f"{y_int}-{int(m):02d}-{int(d):02d}"
        
    # Try Thai text month: 17 กันยายน 2569 or 17 ก.ย. 2569
    for name, month_num in THAI_MONTHS.items():
        pattern = rf'(\d{{1,2}})\s+{re.escape(name)}\s+(\d{{4}})'
        m = re.search(pattern, text)
        if m:
            d, y = m.groups()
            y_int = int(y)
            if y_int > 2500:
                y_int -= 543
            return f"{y_int}-{month_num}-{int(d):02d}"
            
    return datetime.today().strftime("%Y-%m-%d")

def extract_pdf_receipt(file_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    doc = fitz.open(str(file_path))
    pages_text = [p.get_text() for p in doc]
    full_text = "\n".join(pages_text).strip()

    items: List[Dict[str, Any]] = []

    # CASE A: Scanned Raster PDF (no embedded text)
    if not full_text:
        # 1. Primary: Use Vision AI on rendered page
        try:
            pix = doc[0].get_pixmap(dpi=130)
            tmp_img = file_path.parent / f"_tmp_pdf_{file_path.stem}.png"
            pix.save(str(tmp_img))
            try:
                receipt_dict, items, md_repr = extract_receipt_with_gemini(tmp_img)
                receipt_dict["raw_file"] = file_path.name
                if not receipt_dict.get("notes"):
                    receipt_dict["notes"] = f"สแกน PDF ผ่าน Vision AI ({file_path.name})"
                return receipt_dict, items, md_repr
            finally:
                if tmp_img.exists():
                    tmp_img.unlink(missing_ok=True)
        except Exception as ex_vis:
            print(f"[WARN] PDF Vision AI failed for {file_path.name}: {ex_vis}")

        try:
            reader = get_ocr_reader()
            first_page = doc[0]
            last_page = doc[-1]

            # 1. Top crop for Invoice Number & Date
            r_first = first_page.rect
            crop_top = fitz.Rect(r_first.width * 0.35, 0, r_first.width, r_first.height * 0.35)
            top_ocr = reader.readtext(first_page.get_pixmap(clip=crop_top, dpi=120).tobytes('png'), detail=0)
            top_str = ' '.join(top_ocr)

            # 2. Bottom crop for Totals & VAT
            r_last = last_page.rect
            crop_bottom = fitz.Rect(0, r_last.height * 0.65, r_last.width, r_last.height)
            bot_ocr = reader.readtext(last_page.get_pixmap(clip=crop_bottom, dpi=120).tobytes('png'), detail=0)
            bot_str = ' '.join(bot_ocr)

            # Invoice No
            m_inv = re.search(r'(E111\d{10})', top_str)
            receipt_no = m_inv.group(1) if m_inv else f"INV-{file_path.stem}"

            # Date
            dt = ""
            m_d = re.search(r'(\d{1,2})\s*([^\s\d]{2,4})\s*(?:25)?(69|2026)', top_str)
            if m_d:
                d, mo_raw, y = m_d.groups()
                for mo_k, mo_v in THAI_MONTHS.items():
                    if mo_k[0] in mo_raw:
                        dt = f"2026-{mo_v}-{int(d):02d}"
                        break
            if not dt:
                cdate = doc.metadata.get('creationDate', '')
                m_c = re.search(r'D:(\d{4})(\d{2})(\d{2})', cdate)
                if m_c:
                    dt = f"{m_c.group(1)}-{m_c.group(2)}-{m_c.group(3)}"
                else:
                    dt = datetime.today().strftime("%Y-%m-%d")

            # Parse amounts using regex finding all decimals
            nums = [float(n.replace(',', '')) for n in re.findall(r'[\d,]+\.\d{2}', bot_str)]
            total_amount = max(nums) if nums else 0.0
            vat_amount = 0.0
            for n in nums:
                if 0 < n <= total_amount * 0.10 and n != total_amount:
                    vat_amount = n
                    break
            subtotal_amount = round(total_amount - vat_amount, 2) if total_amount > 0 else 0.0

            receipt_dict = {
                "receipt_number": receipt_no,
                "date": dt,
                "time": "",
                "store_name": "บิ๊กซี ซูเปอร์เซ็นเตอร์ บมจ. (สาขาเพชรบูรณ์)",
                "branch": "สาขาที่ 00070",
                "total_amount": total_amount,
                "subtotal_amount": subtotal_amount,
                "vat_amount": vat_amount,
                "payment_method": "PODS / โอนเงิน",
                "raw_file": file_path.name,
                "markdown_file": "",
                "notes": f"สแกนต้นฉบับ Big C (OCR สกัดสำเร็จ)"
            }
            md_repr = f"# ใบกำกับภาษี บิ๊กซี ซูเปอร์เซ็นเตอร์\n\n- เลขที่: {receipt_no}\n- วันที่: {dt}\n- ยอดรวม: {total_amount:,.2f} บาท\n- ภาษีมูลค่าเพิ่ม: {vat_amount:,.2f} บาท\n- สกัดจากภาพสแกน: {file_path.name}\n"
            return receipt_dict, items, md_repr
        except Exception as ex_ocr:
            print(f"[WARN] Local OCR fallback also failed: {ex_ocr}")
            # Minimal fallback receipt
            receipt_dict = {
                "receipt_number": f"INV-{file_path.stem}",
                "date": datetime.today().strftime("%Y-%m-%d"),
                "time": "",
                "store_name": "บิ๊กซี ซูเปอร์เซ็นเตอร์ บมจ.",
                "branch": "เพชรบูรณ์",
                "total_amount": 0.0,
                "subtotal_amount": 0.0,
                "vat_amount": 0.0,
                "payment_method": "PODS / โอนเงิน",
                "raw_file": file_path.name,
                "markdown_file": "",
                "notes": "สแกน PDF รอการประมวลผล"
            }
            return receipt_dict, items, f"# {file_path.name}\n"

    # CASE B: Digital Vector PDF (Rich text)
    receipt_no = ""
    date_str = ""
    store_name = "ร้านโดนใจ"
    branch = ""
    total_amount = 0.0
    subtotal_amount = 0.0
    vat_amount = 0.0
    payment_method = "ไม่ระบุ"

    if 'บิ๊กซี' in full_text or 'Big C' in full_text or 'E111' in full_text or file_path.name.startswith('W'):
        store_name = "บิ๊กซี ซูเปอร์เซ็นเตอร์ บมจ. (สาขาเพชรบูรณ์)"
        branch = "สาขาที่ 00070"
        m_inv = re.search(r'เลขที่\s*:\s*([A-Za-z0-9]+)', full_text)
        receipt_no = m_inv.group(1) if m_inv else f"INV-{file_path.stem}"
        
        m_date = re.search(r'วันที่\s*:\s*([^\n]+)', full_text)
        date_str = parse_thai_date(m_date.group(1)) if m_date else parse_thai_date(full_text)
        
        m_tot = re.search(r'รวมเงินสุทธิ\s*\n\s*([\d,]+\.\d{2})', full_text)
        if not m_tot:
            m_tot = re.search(r'รวมเงิน\s*\n\s*([\d,]+\.\d{2})', full_text)
        if m_tot:
            total_amount = float(m_tot.group(1).replace(',', ''))
            
        m_vat = re.search(r'^ภาษีมูลค่าเพิ่ม\s*\n\s*([\d,]+\.\d{2})', full_text, re.M)
        if m_vat:
            vat_amount = float(m_vat.group(1).replace(',', ''))
            
        m_sub = re.search(r'^มูลค่าสินค้าที่เสียภาษีมูลค่าเพิ่ม\s*\n\s*([\d,]+\.\d{2})', full_text, re.M)
        if m_sub:
            subtotal_amount = float(m_sub.group(1).replace(',', ''))
        elif total_amount > 0:
            subtotal_amount = round(total_amount - vat_amount, 2)
            
        if 'PODS' in full_text:
            payment_method = "PODS / บัญชีเดินสะพัด"
        elif 'เงินสด' in full_text:
            payment_method = "เงินสด"

        # Extract Big C line items
        item_pattern = re.compile(r'(\d+\.\d{3})\s+(\d{12,14})\s+([^\n]+)\n\s*([\d,]+\.\d{2})\n\s*([\d,]+\.\d{2})\n\s*([\d,]+\.\d{2})')
        for match in item_pattern.finditer(full_text):
            qty_str, barcode, iname, unit_p, disc, tot_p = match.groups()
            try:
                items.append({
                    "item_name": iname.strip(),
                    "quantity": float(qty_str),
                    "unit_price": float(unit_p.replace(',', '')),
                    "total_price": float(tot_p.replace(',', ''))
                })
            except ValueError:
                pass

    elif 'เอส.อาร์.ซุปเปอร์มาร์ท' in full_text or 'S26' in full_text:
        store_name = "บริษัท เอส.อาร์.ซุปเปอร์มาร์ท จำกัด"
        m_branch = re.search(r'สาขา\s*:\s*([^\n]+)', full_text)
        branch = m_branch.group(1).strip() if m_branch else "สาขาที่ 3 เพชรบูรณ์"
        
        m_inv = re.search(r'เอกสาร\s*:\s*([A-Za-z0-9\-]+)', full_text)
        receipt_no = m_inv.group(1) if m_inv else f"INV-{file_path.stem}"
        
        # Date from filename or text
        m_fdate = re.match(r'(\d{4})(\d{2})(\d{2})_', file_path.name)
        if m_fdate:
            date_str = f"{m_fdate.group(1)}-{m_fdate.group(2)}-{m_fdate.group(3)}"
        else:
            m_date = re.search(r'(\d{2}/\d{2}/\d{4})', full_text)
            date_str = parse_thai_date(m_date.group(1)) if m_date else parse_thai_date(full_text)
        
        m_tot = re.search(r'([\d,]+\.\d{2})\s*\n\s*(?:รวมจํานวนเงินทั้งสิ้น|รวมจํานวนเงินทั)', full_text)
        if not m_tot:
            m_tot = re.search(r'(?:รวมจํานวนเงินทั้งสิ้น|รวมจํานวนเงินทั[^\n]*)\s*\n\s*([\d,]+\.\d{2})', full_text)
        if m_tot:
            total_amount = float(m_tot.group(1).replace(',', ''))
            
        m_pre = re.search(r'([\d,]+\.\d{2})\s*\n\s*มูลค่าสินค้าก่อนภาษี', full_text)
        pre = float(m_pre.group(1).replace(',', '')) if m_pre else 0.0
        if total_amount > 0 and pre > 0:
            vat_amount = round(total_amount - pre, 2)
            subtotal_amount = pre
        else:
            m_vat = re.search(r'([\d,]+\.\d{2})\s*\n\s*ภาษี\s*7\.00%', full_text)
            if not m_vat:
                m_vat = re.search(r'ภาษี\s*7\.00%\s*\n\s*([\d,]+\.\d{2})', full_text)
            if m_vat:
                vat_amount = float(m_vat.group(1).replace(',', ''))
            subtotal_amount = round(total_amount - vat_amount, 2) if total_amount > 0 else 0.0
            
        payment_method = "เงินโอน/พร้อมเพย์"

    elif 'ออรโร โฮม' in full_text or 'ออร์โร่ โฮม' in full_text:
        store_name = "บริษัท ออร์โร่ โฮม จำกัด (Deerma Official)"
        branch = "สำนักงานใหญ่"
        m_inv = re.search(r'เลขที่ใบกํากับ\s+([A-Za-z0-9]+)', full_text)
        receipt_no = m_inv.group(1) if m_inv else f"INV-{file_path.stem}"
        date_str = parse_thai_date(full_text)
        
        m_tot = re.search(r'จํานวนเงินรวมทั้งสิ้น\s*.*?([\d,]+\.\d{2})', full_text)
        if m_tot:
            total_amount = float(m_tot.group(1).replace(',', ''))
        m_vat = re.search(r'จํานวนภาษีมูลคาเพิ่ม.*?([\d,]+\.\d{2})', full_text)
        if m_vat:
            vat_amount = float(m_vat.group(1).replace(',', ''))
        m_sub = re.search(r'ราคาสินคา\s*.*?([\d,]+\.\d{2})', full_text)
        if m_sub:
            subtotal_amount = float(m_sub.group(1).replace(',', ''))
        payment_method = "ชำระออนไลน์"

    else:
        # Fallback generic
        m_inv = re.search(r'(?:เลขที่|inv(?:oice)?)[^\w\n]*[:\s]+([A-Za-z0-9\-_/]+)', full_text, re.I)
        receipt_no = m_inv.group(1).strip() if m_inv else f"INV-{file_path.stem}"
        date_str = parse_thai_date(full_text)
        m_tot = re.search(r'(?:ยอดรวม|total)[^\d\n]*([\d,]+\.\d{2})', full_text, re.I)
        if m_tot:
            total_amount = float(m_tot.group(1).replace(',', ''))

    receipt_dict = {
        "receipt_number": receipt_no,
        "date": date_str or datetime.today().strftime("%Y-%m-%d"),
        "time": "",
        "store_name": store_name,
        "branch": branch,
        "total_amount": total_amount,
        "subtotal_amount": subtotal_amount,
        "vat_amount": vat_amount,
        "payment_method": payment_method,
        "raw_file": file_path.name,
        "markdown_file": "",
        "notes": f"สกัดจาก PDF อิเล็กทรอนิกส์ ({file_path.name})"
    }
    return receipt_dict, items, full_text

def extract_receipt_fields(md_text: str, filename: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    receipt_no = ""
    match_no = re.search(r'(?:เลขที่|ใบเสร็จ|receipt|inv(?:oice)?)[^\w\n]*[:\s]+([A-Za-z0-9\-_/]+)', md_text, re.IGNORECASE)
    if match_no:
        receipt_no = match_no.group(1).strip()
    else:
        receipt_no = f"REC-{Path(filename).stem}"

    date_str = parse_thai_date(md_text)

    store_name = "ร้านโดนใจ"
    branch = ""
    match_store = re.search(r'(?:ร้าน|สาขา)\s*([^\n|]+)', md_text)
    if match_store:
        candidate = match_store.group(1).strip()
        if "โดนใจ" in candidate:
            store_name = "ร้านโดนใจ"
        if "สาขา" in candidate:
            branch = candidate[candidate.find("สาขา"):].strip()

    total_amount = 0.0
    subtotal_amount = 0.0
    vat_amount = 0.0

    match_total = re.search(r'(?:ยอดรวมสุทธิ|ยอดรวมทั้งสิ้น|รวมเงินทั้งสิ้น|total amount|grand total)[^\d\n]*([\d,]+\.?\d*)', md_text, re.IGNORECASE)
    if not match_total:
        match_total = re.search(r'(?:ยอดรวม|รวมเงิน|รวมเป็นเงิน|total)[^\d\n]*([\d,]+\.?\d*)', md_text, re.IGNORECASE)
    if match_total:
        try:
            total_amount = float(match_total.group(1).replace(',', ''))
        except ValueError:
            pass

    match_vat = re.search(r'(?:ภาษีมูลค่าเพิ่ม|vat(?:\s*7%)?)[^\d\n]*([\d,]+\.?\d*)', md_text, re.IGNORECASE)
    if match_vat:
        try:
            vat_amount = float(match_vat.group(1).replace(',', ''))
        except ValueError:
            pass

    match_sub = re.search(r'(?:ยอดรวมก่อนภาษี|ราคาสินค้า|subtotal)[^\d\n]*([\d,]+\.?\d*)', md_text, re.IGNORECASE)
    if match_sub:
        try:
            subtotal_amount = float(match_sub.group(1).replace(',', ''))
        except ValueError:
            pass
    elif total_amount > 0 and vat_amount > 0:
        subtotal_amount = round(total_amount - vat_amount, 2)

    payment_method = "ไม่ระบุ"
    if re.search(r'(?:พร้อมเพย์|qr|promptpay|thai qr)', md_text, re.IGNORECASE):
        payment_method = "Thai QR พร้อมเพย์"
    elif re.search(r'(?:เงินสด|cash)', md_text, re.IGNORECASE):
        payment_method = "เงินสด"
    elif re.search(r'(?:บัตรเครดิต|บัตรเดบิต|credit|debit)', md_text, re.IGNORECASE):
        payment_method = "บัตรเครดิต/เดบิต"

    items = []
    lines = md_text.splitlines()
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(c.replace('-', '').replace(':', '') == '' for c in cells):
                in_table = True
                continue
                
            if in_table and len(cells) >= 3:
                first_cell = cells[0].lower()
                if any(k in first_cell for k in ["ลำดับ", "รายการ", "item", "#", "no"]):
                    continue
                    
                item_name = ""
                qty = 1.0
                unit_price = 0.0
                total_price = 0.0
                
                if cells[0].isdigit() and len(cells) >= 4:
                    item_name = cells[1]
                    try:
                        qty = float(cells[2].replace(',', ''))
                        unit_price = float(cells[3].replace(',', ''))
                        total_price = float(cells[4].replace(',', '')) if len(cells) > 4 else qty * unit_price
                    except (ValueError, IndexError):
                        pass
                else:
                    item_name = cells[0]
                    try:
                        qty = float(cells[1].replace(',', ''))
                        total_price = float(cells[-1].replace(',', ''))
                        unit_price = total_price / qty if qty > 0 else total_price
                    except (ValueError, IndexError):
                        pass
                        
                if item_name and total_price > 0:
                    items.append({
                        "item_name": item_name,
                        "quantity": qty,
                        "unit_price": unit_price,
                        "total_price": total_price
                    })

    if total_amount == 0.0 and items:
        total_amount = sum(i["total_price"] for i in items)

    receipt_dict = {
        "receipt_number": receipt_no,
        "date": date_str,
        "time": "",
        "store_name": store_name,
        "branch": branch,
        "total_amount": total_amount,
        "subtotal_amount": subtotal_amount,
        "vat_amount": vat_amount,
        "payment_method": payment_method,
        "raw_file": filename,
        "markdown_file": "",
        "notes": f"สกัดจากไฟล์ {filename}"
    }

    return receipt_dict, items

def get_gemini_api_key() -> str:
    """Safely fetch Gemini API Key from Streamlit Secrets, environment, or .env."""
    # 1. Streamlit Secrets (Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = str(st.secrets["GEMINI_API_KEY"]).strip().strip('"').strip("'")
            if key and not key.startswith("ใส่คีย์") and "..." not in key and len(key) > 20:
                return key
    except Exception:
        pass

    # 2. Environment variable
    env_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if env_key and not env_key.startswith("ใส่คีย์") and len(env_key) > 20:
        return env_key

    # 3. Local .env file
    local_env = Path(__file__).resolve().parent / ".env"
    if local_env.exists():
        try:
            with open(local_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        k = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if k and not k.startswith("ใส่คีย์") and len(k) > 20:
                            return k
        except Exception:
            pass

    # 4. Project 'เป็นผู้ช่วย' .env file
    helper_env = Path(__file__).resolve().parent.parent / "เป็นผู้ช่วย" / ".env"
    if helper_env.exists():
        try:
            with open(helper_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        k = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if k and not k.startswith("ใส่คีย์") and len(k) > 20:
                            return k
        except Exception:
            pass

    return "sk_TkkwwUFGJtdKY8RVPPFVuzFBzvuXcxf3mb06YMsXGnStVnaDIySwk84nA2XYd0Ao"

def parse_ai_json_to_receipt(data: Dict[str, Any], file_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    """Helper to convert structured AI JSON output into receipt_dict, items, and markdown."""
    store_name = data.get("store_name") or "ร้านค้าทั่วไป"
    branch = data.get("branch") or ""
    receipt_no = data.get("receipt_number") or f"IMG-{file_path.stem}"
    raw_date = data.get("date") or datetime.today().strftime("%Y-%m-%d")
    time_str = data.get("time") or ""

    # Parse Buddhist era or DD/MM/YYYY into YYYY-MM-DD
    date_str = parse_thai_date(str(raw_date))

    try:
        total_amount = float(str(data.get("total_amount", 0.0)).replace(',', ''))
    except Exception:
        total_amount = 0.0

    try:
        vat_amount = float(str(data.get("vat_amount", 0.0) or 0.0).replace(',', ''))
    except Exception:
        vat_amount = 0.0

    try:
        subtotal_amount = float(str(data.get("subtotal_amount", 0.0) or 0.0).replace(',', ''))
    except Exception:
        subtotal_amount = max(0.0, total_amount - vat_amount)

    if "การไฟฟ้า" in store_name or "PEA" in store_name:
        store_name = "การไฟฟ้าส่วนภูมิภาค (PEA)"
        if not branch:
            branch = "กฟภ.หล่มสัก / ร้านศรีบุตรา"
        if vat_amount == 0.0 and total_amount > 0:
            vat_amount = round(total_amount * 7 / 107, 2)
            subtotal_amount = round(total_amount - vat_amount, 2)

    payment_method = data.get("payment_method") or "เงินสด"
    raw_items = data.get("items") or []

    items = []
    for item in raw_items:
        i_name = item.get("name") or item.get("item_name") or "สินค้า"
        try:
            qty = float(item.get("quantity", 1.0))
        except Exception:
            qty = 1.0
        try:
            unit_p = float(item.get("unit_price", 0.0))
        except Exception:
            unit_p = 0.0
        try:
            tot_p = float(item.get("total_price") or item.get("amount") or (qty * unit_p))
        except Exception:
            tot_p = qty * unit_p

        items.append({
            "item_name": i_name,
            "quantity": qty,
            "unit_price": unit_p,
            "total_price": tot_p
        })

    if total_amount == 0.0 and items:
        total_amount = sum(i["total_price"] for i in items)

    receipt_dict = {
        "receipt_number": receipt_no,
        "date": date_str,
        "time": time_str,
        "store_name": store_name,
        "branch": branch,
        "total_amount": total_amount,
        "subtotal_amount": subtotal_amount,
        "vat_amount": vat_amount,
        "payment_method": payment_method,
        "raw_file": file_path.name,
        "markdown_file": "",
        "notes": f"สแกนอัตโนมัติด้วย AI Vision จากภาพถ่าย {file_path.name}"
    }

    # Build Markdown summary
    md_lines = [
        f"# ใบเสร็จ/ใบกำกับภาษี: {store_name}",
        f"- **เลขที่:** {receipt_no}",
        f"- **วันที่:** {date_str} {time_str}",
        f"- **สาขา:** {branch}",
        f"- **การชำระเงิน:** {payment_method}",
        f"- **ยอดรวมสุทธิ:** ฿{total_amount:,.2f}",
        f"- **VAT:** ฿{vat_amount:,.2f}",
        "",
        "## รายการสินค้า",
        "| รายการ | จำนวน | ราคา/หน่วย | รวม |",
        "|---|---|---|---|"
    ]
    for it in items:
        md_lines.append(f"| {it['item_name']} | {it['quantity']} | ฿{it['unit_price']:,.2f} | ฿{it['total_price']:,.2f} |")
    md_text = "\n".join(md_lines)

    return receipt_dict, items, md_text

def extract_receipt_with_gemini(file_path: Path, api_key: str = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    """Extract receipt structured data using OKMD Gemini 3.8 Flash with Agnes AI fallback."""
    import urllib.request
    import base64
    import json
    import re

    ext = file_path.suffix.lower()
    mime_type = "image/jpeg"
    if ext == ".png":
        mime_type = "image/png"
    elif ext == ".webp":
        mime_type = "image/webp"

    with open(file_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = """คุณคือผู้เชี่ยวชาญด้านการวิเคราะห์ใบเสร็จ ใบกำกับภาษี และบิลซื้อสินค้าของประเทศไทย
กรุณาส่องอ่านรูปภาพใบเสร็จนี้อย่างละเอียด และตอบกลับเป็น JSON ตามโครงสร้างนี้เท่านั้น:
{
  "store_name": "ชื่อร้านค้า เช่น หจก ไทยทอยส์ เพชรบูรณ์, สยามแม็คโคร, บิ๊กซี, เอส.อาร์.ซุปเปอร์มาร์ท",
  "branch": "สาขา หรือ ที่อยู่ร้าน (ถ้ามี)",
  "receipt_number": "เลขที่ใบเสร็จ หรือ เลขที่เอกสาร (ถ้ามี)",
  "date": "วันที่ในบิล เช่น 2026-09-19 หรือ 19/09/2569",
  "time": "เวลา เช่น 15:00",
  "total_amount": 0.0,
  "subtotal_amount": 0.0,
  "vat_amount": 0.0,
  "payment_method": "เงินสด, โอนเงิน/พร้อมเพย์, หรือ บัตร",
  "items": [
    {
      "name": "ชื่อสินค้า",
      "quantity": 1.0,
      "unit_price": 0.0,
      "total_price": 0.0
    }
  ]
}
ข้อกำหนดสำคัญ:
- ตัวเลขยอดเงินต้องเป็นตัวเลข Float ห้ามมีลูกน้ำจุลภาค
- ตอบกลับเฉพาะ JSON ที่ถูกต้องเท่านั้น ห้ามใส่ข้อความอธิบายอื่นนอกบล็อก JSON
"""

    # 1. Primary Engine: OKMD Gemini 3.8 Flash (Free national AI service)
    okmd_key = "sk_TkkwwUFGJtdKY8RVPPFVuzFBzvuXcxf3mb06YMsXGnStVnaDIySwk84nA2XYd0Ao"
    try:
        url = "https://gen.ai.kku.ac.th/okmd/api/v1/chat/completions"
        payload = {
            "model": "gemini-3.8-flash",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{img_b64}"}}
                    ]
                }
            ],
            "temperature": 0.1
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {okmd_key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_json = json.loads(resp.read().decode("utf-8"))
            content = resp_json["choices"][0]["message"]["content"]
            clean = content.strip()
            if "```" in clean:
                m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', clean)
                if m:
                    clean = m.group(1).strip()
            data = json.loads(clean)
            return parse_ai_json_to_receipt(data, file_path)
    except Exception as ex_okmd:
        print(f"[WARN] OKMD Vision failed ({ex_okmd}), falling back to Agnes AI...")

    # 2. Secondary Engine: Agnes AI (agnes-3.0-flash)
    agnes_key = "sk-e5ypYPPS3yaXJ6erdz5wNmSXw9Lt3MRI2IkvLJ7ta2fkHGz7"
    try:
        url = "https://apihub.agnes-ai.com/v1/chat/completions"
        payload = {
            "model": "agnes-3.0-flash",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{img_b64}"}}
                    ]
                }
            ],
            "temperature": 0.1
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {agnes_key}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_json = json.loads(resp.read().decode("utf-8"))
            content = resp_json["choices"][0]["message"]["content"]
            clean = content.strip()
            if "```" in clean:
                m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', clean)
                if m:
                    clean = m.group(1).strip()
            data = json.loads(clean)
            return parse_ai_json_to_receipt(data, file_path)
    except Exception as ex_agnes:
        print(f"[ERROR] Agnes Vision also failed: {ex_agnes}")
        raise ex_agnes

def process_file(file_path: Path, md_converter=None) -> Dict[str, Any]:
    CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
    md_output_path = CONVERTED_DIR / f"{file_path.stem}.md"

    try:
        if file_path.suffix.lower() == '.pdf':
            receipt_data, items, md_text = extract_pdf_receipt(file_path)
            with open(md_output_path, 'w', encoding='utf-8') as f:
                f.write(md_text)
        elif file_path.suffix.lower() == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
            receipt_data, items = extract_receipt_fields(md_text, file_path.name)
        elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
            gemini_key = get_gemini_api_key()
            if gemini_key:
                try:
                    receipt_data, items, md_text = extract_receipt_with_gemini(file_path, gemini_key)
                    with open(md_output_path, 'w', encoding='utf-8') as f:
                        f.write(md_text)
                except Exception as ex_gemini:
                    print(f"[WARN] Gemini Vision failed for {file_path.name}: {ex_gemini}")
                    receipt_data = {
                        "receipt_number": f"IMG-{file_path.stem}",
                        "date": datetime.today().strftime("%Y-%m-%d"),
                        "time": "",
                        "store_name": "รูปถ่าย (รอระบุยอดเงิน)",
                        "branch": "",
                        "total_amount": 0.0,
                        "subtotal_amount": 0.0,
                        "vat_amount": 0.0,
                        "payment_method": "ไม่ระบุ",
                        "raw_file": file_path.name,
                        "markdown_file": "",
                        "notes": f"เกิดข้อผิดพลาดในการอ่าน AI Vision: {str(ex_gemini)[:100]}"
                    }
                    items = []
            else:
                receipt_data = {
                    "receipt_number": f"IMG-{file_path.stem}",
                    "date": datetime.today().strftime("%Y-%m-%d"),
                    "time": "",
                    "store_name": "รูปถ่าย (รอระบุยอดเงิน)",
                    "branch": "",
                    "total_amount": 0.0,
                    "subtotal_amount": 0.0,
                    "vat_amount": 0.0,
                    "payment_method": "ไม่ระบุ",
                    "raw_file": file_path.name,
                    "markdown_file": "",
                    "notes": "ยังไม่ได้ตั้งค่าคีย์ AI Vision"
                }
                items = []
        else:
            if md_converter is None:
                md_converter = MarkItDown()
            result = md_converter.convert(str(file_path))
            md_text = result.text_content or ""
            with open(md_output_path, 'w', encoding='utf-8') as f:
                f.write(md_text)
            receipt_data, items = extract_receipt_fields(md_text, file_path.name)

        receipt_data["markdown_file"] = str(md_output_path)
        receipt_id = db.insert_receipt(receipt_data, items)

        return {
            "file": str(file_path.name),
            "status": "success",
            "receipt_id": receipt_id,
            "receipt_number": receipt_data["receipt_number"],
            "date": receipt_data["date"],
            "store_name": receipt_data["store_name"],
            "total_amount": receipt_data["total_amount"],
            "vat_amount": receipt_data["vat_amount"],
            "items_count": len(items)
        }
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path.name}: {e}")
        return {"file": str(file_path.name), "status": "error", "message": str(e)}

MAKRO_ORDERS = [
    # Screenshot 1 (Jan - Feb 2569)
    {"order_no": "29955922A", "date": "2026-02-13", "time": "07:55", "amount": 4522.0},
    {"order_no": "29826315A", "date": "2026-02-11", "time": "08:22", "amount": 13040.0},
    {"order_no": "29412220A", "date": "2026-02-03", "time": "11:25", "amount": 3816.0},
    {"order_no": "29009969A", "date": "2026-01-26", "time": "15:27", "amount": 37569.0},
    {"order_no": "28728596A", "date": "2026-01-21", "time": "08:59", "amount": 1035.0},
    {"order_no": "28728336A", "date": "2026-01-21", "time": "09:00", "amount": 8413.0},
    {"order_no": "28362548A", "date": "2026-01-14", "time": "11:57", "amount": 16423.0},
    {"order_no": "27742835A", "date": "2026-01-02", "time": "13:02", "amount": 6968.0},
    {"order_no": "27713265A", "date": "2026-01-01", "time": "19:49", "amount": 34874.0},

    # Screenshot 2 (Feb - Apr 2569)
    {"order_no": "32764752A", "date": "2026-04-05", "time": "08:00", "amount": 22547.0},
    {"order_no": "32643364A", "date": "2026-04-03", "time": "08:00", "amount": 9547.0},
    {"order_no": "32198367A", "date": "2026-03-26", "time": "08:00", "amount": 5094.0},
    {"order_no": "31996291A", "date": "2026-03-22", "time": "16:00", "amount": 7085.0},
    {"order_no": "31641171A", "date": "2026-03-16", "time": "08:00", "amount": 18908.0},
    {"order_no": "31270148A", "date": "2026-03-09", "time": "15:09", "amount": 5148.0},
    {"order_no": "30861792A", "date": "2026-03-02", "time": "08:32", "amount": 19741.0},
    {"order_no": "30771510A", "date": "2026-02-28", "time": "16:19", "amount": 4417.0},
    {"order_no": "30163613A", "date": "2026-02-17", "time": "09:29", "amount": 7533.0},
    {"order_no": "30005338A", "date": "2026-02-14", "time": "07:55", "amount": 5240.0},

    # Screenshot 3 (Apr - May 2569)
    {"order_no": "34844975A", "date": "2026-05-14", "time": "08:00", "amount": 3540.0},
    {"order_no": "34682781A", "date": "2026-05-11", "time": "08:00", "amount": 7237.0},
    {"order_no": "34420645A", "date": "2026-05-06", "time": "16:00", "amount": 6259.0},
    {"order_no": "34115949A", "date": "2026-05-01", "time": "08:00", "amount": 6075.0},
    {"order_no": "34059465A", "date": "2026-04-30", "time": "08:00", "amount": 6550.0},
    {"order_no": "33867494A", "date": "2026-04-26", "time": "16:00", "amount": 12401.0},
    {"order_no": "33560218A", "date": "2026-04-21", "time": "08:00", "amount": 17459.0},
    {"order_no": "33245735A", "date": "2026-04-14", "time": "08:00", "amount": 6599.0},
    {"order_no": "32814298A", "date": "2026-04-06", "time": "08:00", "amount": 8182.0},
    {"order_no": "32764909A", "date": "2026-04-05", "time": "08:00", "amount": 6550.0},

    # Screenshot 4 (May - Jul 2569)
    {"order_no": "37811014A", "date": "2026-07-04", "time": "08:00", "amount": 9914.0},
    {"order_no": "37483782A", "date": "2026-06-29", "time": "08:00", "amount": 4231.0},
    {"order_no": "37385119A", "date": "2026-06-27", "time": "08:00", "amount": 13600.0},
    {"order_no": "37089268A", "date": "2026-06-22", "time": "08:00", "amount": 4903.0},
    {"order_no": "36867413A", "date": "2026-06-18", "time": "08:00", "amount": 16148.0},
    {"order_no": "36686057A", "date": "2026-06-15", "time": "08:00", "amount": 14419.0},
    {"order_no": "36246671A", "date": "2026-06-07", "time": "16:00", "amount": 4463.0},
    {"order_no": "35906291A", "date": "2026-06-02", "time": "08:00", "amount": 10683.8},
    {"order_no": "35409651A", "date": "2026-05-24", "time": "16:00", "amount": 19322.0},
    {"order_no": "35075056A", "date": "2026-05-18", "time": "16:00", "amount": 12998.0},

    # Screenshot 5 (Jul - Aug 2569)
    {"order_no": "39925384A", "date": "2026-08-08", "time": "08:00", "amount": 9227.0},
    {"order_no": "39606992A", "date": "2026-08-03", "time": "08:00", "amount": 3480.0},
    {"order_no": "39554259A", "date": "2026-08-02", "time": "08:00", "amount": 4491.0},
    {"order_no": "39179988A", "date": "2026-07-27", "time": "08:00", "amount": 4249.0},
    {"order_no": "39023841A", "date": "2026-07-24", "time": "08:00", "amount": 14003.0},
    {"order_no": "38657133A", "date": "2026-07-18", "time": "08:00", "amount": 1785.0},
    {"order_no": "38644589A", "date": "2026-07-18", "time": "08:00", "amount": 3213.0},
    {"order_no": "38427976A", "date": "2026-07-14", "time": "08:00", "amount": 12078.0},
    {"order_no": "38183486A", "date": "2026-07-10", "time": "08:00", "amount": 12469.0},
    {"order_no": "37883329A", "date": "2026-07-05", "time": "08:00", "amount": 12133.0},

    # Screenshot 6 (Aug - Sep 2569)
    {"order_no": "42162900A", "date": "2026-09-13", "time": "16:00", "amount": 8270.0},
    {"order_no": "41791406A", "date": "2026-09-07", "time": "16:00", "amount": 5013.0},
    {"order_no": "41583266A", "date": "2026-09-04", "time": "08:00", "amount": 6164.0},
    {"order_no": "41303422A", "date": "2026-08-31", "time": "08:00", "amount": 6423.0},
    {"order_no": "40909404A", "date": "2026-08-24", "time": "08:00", "amount": 11424.0},
    {"order_no": "40517187A", "date": "2026-08-17", "time": "16:00", "amount": 5645.0},
    {"order_no": "40315545A", "date": "2026-08-14", "time": "08:00", "amount": 4353.0},
    {"order_no": "40054653A", "date": "2026-08-10", "time": "08:00", "amount": 26000.0},
    {"order_no": "39946758A", "date": "2026-08-08", "time": "08:00", "amount": 2150.0},
    {"order_no": "39926327A", "date": "2026-08-08", "time": "08:00", "amount": 34010.0},
]

def import_makro_orders() -> List[Dict[str, Any]]:
    db.init_db()
    results = []
    for o in MAKRO_ORDERS:
        subtotal = round(o["amount"] / 1.07, 2)
        vat = round(o["amount"] - subtotal, 2)
        receipt_data = {
            "receipt_number": f"MK-{o['order_no']}",
            "date": o["date"],
            "time": o["time"],
            "store_name": "สยามแม็คโคร (Makro PRO)",
            "branch": "สาขาเพชรบูรณ์ / จัดส่งร้าน",
            "total_amount": float(o["amount"]),
            "subtotal_amount": subtotal,
            "vat_amount": vat,
            "payment_method": "Makro PRO / Assisted Sales",
            "raw_file": f"MakroPRO_{o['order_no']}.png",
            "markdown_file": "",
            "notes": "คำสั่งซื้อ Makro PRO (ใบกำกับภาษีเต็มรูปแบบอยู่ที่ร้าน)"
        }
        r_id = db.insert_receipt(receipt_data)
        results.append({
            "file": receipt_data["raw_file"],
            "status": "success",
            "receipt_id": r_id,
            "receipt_number": receipt_data["receipt_number"],
            "date": receipt_data["date"],
            "store_name": receipt_data["store_name"],
            "total_amount": receipt_data["total_amount"],
            "vat_amount": receipt_data["vat_amount"],
            "items_count": 0
        })
    return results

def analyze_all_receipts() -> List[Dict[str, Any]]:
    db.init_db()
    md_converter = MarkItDown()
    results = []

    supported_exts = ['.pdf', '.html', '.htm', '.docx', '.xlsx', '.txt', '.png', '.jpg', '.jpeg']
    candidate_files = []
    
    if EXTRACTED_DIR.exists():
        for ext in supported_exts:
            candidate_files.extend(EXTRACTED_DIR.glob(f"*{ext}"))
            
    if CONVERTED_DIR.exists():
        candidate_files.extend(CONVERTED_DIR.glob("*.md"))

    seen_names = set()
    for f in candidate_files:
        if f.stem in seen_names or f.name == 'desktop.ini':
            continue
        seen_names.add(f.stem)
        res = process_file(f, md_converter)
        results.append(res)

    # Ingest Makro PRO orders
    makro_res = import_makro_orders()
    results.extend(makro_res)

    return results

if __name__ == "__main__":
    print("Running Receipt Analyzer across extracted_receipts/ and Makro PRO...")
    res = analyze_all_receipts()
    success_count = sum(1 for r in res if r.get("status") == "success")
    total_val = sum(r.get("total_amount", 0.0) for r in res if r.get("status") == "success")
    total_vat = sum(r.get("vat_amount", 0.0) for r in res if r.get("status") == "success")
    print(f"Finished: {success_count}/{len(res)} receipts processed.")
    print(f"Total Purchases: {total_val:,.2f} THB")
    print(f"Total Input VAT: {total_vat:,.2f} THB")
