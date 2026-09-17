"""
โมดูลคำนวณและจำลองภาษีเงินได้บุคคลธรรมดา (มาตรา 40(8) ร้านค้าปลีก/โชห่วย)
สำหรับร้านศรีบุตรา ตามเกณฑ์กรมสรรพากร
"""

from typing import Dict, Any, List, Tuple

# อัตราภาษีเงินได้บุคคลธรรมดาแบบก้าวหน้า (Personal Income Tax Progressive Rates)
TAX_BRACKETS = [
    (150_000, 0.00),    # 0 - 150,000 ได้รับการยกเว้น
    (300_000, 0.05),    # 150,001 - 300,000 (150,000 @ 5% = 7,500)
    (500_000, 0.10),    # 300,001 - 500,000 (200,000 @ 10% = 20,000)
    (750_000, 0.15),    # 500,001 - 750,000 (250,000 @ 15% = 37,500)
    (1_000_000, 0.20),  # 750,001 - 1,000,000 (250,000 @ 20% = 50,000)
    (2_000_000, 0.25),  # 1,000,001 - 2,000,000 (1,000,000 @ 25% = 250,000)
    (5_000_000, 0.30),  # 2,000,001 - 5,000,000 (3,000,000 @ 30% = 900,000)
    (float('inf'), 0.35) # เกิน 5,000,000 ขึ้นไป @ 35%
]

def calculate_progressive_tax(net_income: float) -> Tuple[float, List[Dict[str, Any]]]:
    """
    คำนวณภาษีตามขั้นบันไดเงินได้สุทธิ
    คืนค่า (ภาษีรวม, รายละเอียดแต่ละขั้น)
    """
    if net_income <= 0:
        return 0.0, []

    total_tax = 0.0
    tax_breakdown = []
    prev_limit = 0.0

    for limit, rate in TAX_BRACKETS:
        if net_income > prev_limit:
            taxable_in_bracket = min(net_income, limit) - prev_limit
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket

            tax_breakdown.append({
                "bracket_range": f"{prev_limit + 1:,.0f} - {limit:,.0f}" if limit != float('inf') else f"มากกว่า {prev_limit:,.0f}",
                "rate_pct": f"{int(rate * 100)}%",
                "taxable_amount": taxable_in_bracket,
                "tax_amount": tax_in_bracket
            })
            prev_limit = limit
        else:
            break

    return total_tax, tax_breakdown

def calculate_gross_tax(gross_income: float, is_half_year: bool = False) -> float:
    """
    วิธีคำนวณแบบเหมา 0.5% ของเงินได้พึงประเมิน (กรณียอดขายเกิน 1,000,000 บาทต่อปี หรือ 500,000 บาทครึ่งปี)
    ตามกฎหมาย หากภาษีที่คำนวณได้ไม่เกิน 5,000 บาท ได้รับการยกเว้น
    """
    threshold = 500_000 if is_half_year else 1_000_000
    if gross_income > threshold:
        tax = gross_income * 0.005
        return tax if tax > 5_000 else 0.0
    return 0.0

def compare_tax_methods(
    gross_sales: float,
    actual_purchases: float,
    other_expenses: float = 0.0,
    allowances: float = 60_000.0,
    is_half_year: bool = False,
    prepaid_tax: float = 0.0
) -> Dict[str, Any]:
    """
    เปรียบเทียบการเสียภาษีระหว่าง 'หักเหมา 60%' กับ 'หักตามจริง'
    สำหรับ ภ.ง.ด.94 (is_half_year=True) หรือ ภ.ง.ด.90 (is_half_year=False)
    """
    # 1. วิธีหักค่าใช้จ่ายแบบเหมา 60%
    flat_expense_rate = 0.60
    flat_expenses = gross_sales * flat_expense_rate
    flat_net_income = max(0.0, gross_sales - flat_expenses - allowances)
    flat_method1_tax, flat_bracket_detail = calculate_progressive_tax(flat_net_income)
    flat_method2_tax = calculate_gross_tax(gross_sales, is_half_year)
    flat_gross_tax = max(flat_method1_tax, flat_method2_tax)
    flat_net_tax = max(0.0, flat_gross_tax - prepaid_tax)

    # 2. วิธีหักค่าใช้จ่ายตามจริง (Actual Expenses จากใบเสร็จโดนใจ + ค่าใช้จ่ายอื่น)
    total_actual_expenses = actual_purchases + other_expenses
    actual_net_income = max(0.0, gross_sales - total_actual_expenses - allowances)
    actual_method1_tax, actual_bracket_detail = calculate_progressive_tax(actual_net_income)
    actual_method2_tax = calculate_gross_tax(gross_sales, is_half_year)
    actual_gross_tax = max(actual_method1_tax, actual_method2_tax)
    actual_net_tax = max(0.0, actual_gross_tax - prepaid_tax)

    # คำนวณภาษีที่ประหยัดได้
    tax_savings = flat_net_tax - actual_net_tax

    return {
        "is_half_year": is_half_year,
        "form_name": "ภ.ง.ด. 94 (ครึ่งปี)" if is_half_year else "ภ.ง.ด. 90 (สิ้นปี)",
        "gross_sales": gross_sales,
        "allowances": allowances,
        "prepaid_tax": prepaid_tax,
        
        # ผลลัพธ์วิธีเหมา 60%
        "flat": {
            "expenses": flat_expenses,
            "net_income": flat_net_income,
            "tax_method1": flat_method1_tax,
            "tax_method2": flat_method2_tax,
            "tax_gross": flat_gross_tax,
            "tax_net": flat_net_tax,
            "bracket_detail": flat_bracket_detail
        },
        
        # ผลลัพธ์วิธีหักตามจริง
        "actual": {
            "purchases": actual_purchases,
            "other_expenses": other_expenses,
            "total_expenses": total_actual_expenses,
            "net_income": actual_net_income,
            "tax_method1": actual_method1_tax,
            "tax_method2": actual_method2_tax,
            "tax_gross": actual_gross_tax,
            "tax_net": actual_net_tax,
            "bracket_detail": actual_bracket_detail
        },
        
        "tax_savings": tax_savings,
        "recommended_method": "หักค่าใช้จ่ายตามจริง (ประหยัดกว่า)" if tax_savings > 0 else "หักเหมา 60% (สะดวกกว่า)"
    }

def analyze_vat_threshold(sample_revenue: float, days_in_sample: int = 30) -> Dict[str, Any]:
    """
    วิเคราะห์และพยากรณ์เพดานภาษีมูลค่าเพิ่ม (VAT 1.8 ล้านบาท/ปี)
    โดยอ้างอิงจากตัวเลขรายรับจริงในสเตตเมนต์
    """
    VAT_LIMIT = 1_800_000.0
    daily_rate = sample_revenue / max(1, days_in_sample)
    monthly_projected = daily_rate * 30
    annual_projected = daily_rate * 365
    
    pct_of_limit = (annual_projected / VAT_LIMIT) * 100
    
    days_to_reach = round(VAT_LIMIT / daily_rate) if daily_rate > 0 else 9999
    months_to_reach = round(days_to_reach / 30.0, 1)
    
    if sample_revenue >= VAT_LIMIT:
        status = "OFFICIALLY_BREACHED"
        level_color = "red"
        status_text = "🚨 ยอดขายจริงสะสมเกิน 1.8 ล้านบาทแล้วอย่างเป็นทางการ (ต้องยื่น ภ.พ.01 ด่วนที่สุด)"
        advice = f"รายรับจริงสะสมแตะ ฿{sample_revenue:,.2f} บาท ซึ่งเกินเพดาน 1.8 ล้านบาทไปแล้ว +฿{sample_revenue - VAT_LIMIT:,.2f} บาท ตามประมวลรัษฎากร มาตรา 85/1 ต้องยื่นแบบ ภ.พ.01 ภายใน 30 วันนับแต่วันที่ยอดเกิน เพื่อป้องกันเบี้ยปรับย้อนหลัง"
    elif annual_projected >= VAT_LIMIT:
        status = "CRITICAL_OVER"
        level_color = "red"
        status_text = "🚨 มีแนวโน้มเกิน 1.8 ล้านบาทต่อปี (ต้องเตรียมตัวจด VAT ภ.พ.01)"
        advice = f"หากยอดขายเฉลี่ยระดับนี้ต่อเนื่อง ร้านจะมีรายได้ทะลุ 1.8 ล้านบาทภายในประมาณเดือนที่ {months_to_reach} ของปี ควรเตรียมเอกสารขอจดทะเบียนภาษีมูลค่าเพิ่มล่วงหน้าเพื่อป้องกันเบี้ยปรับ"
    elif annual_projected >= 1_440_000.0:  # 80%
        status = "WARNING_HIGH"
        level_color = "orange"
        status_text = "⚠️ ระดับเฝ้าระวังเข้มงวด (แตะ 80% ของเพดาน 1.8 ล้าน)"
        advice = "ยอดขายเริ่มใกล้เคียงเพดาน 1.8 ล้านบาท ควรตรวจเช็ครายรับทุกสิ้นเดือนอย่างใกล้ชิด"
    else:
        status = "SAFE"
        level_color = "green"
        status_text = "🟢 ปลอดภัย (ยังไม่เกินเกณฑ์ 1.8 ล้านบาทต่อปี)"
        advice = "รายได้ยังไม่ถึงเกณฑ์ที่กฎหมายบังคับให้จดทะเบียนภาษีมูลค่าเพิ่ม ไม่ต้องยื่นแบบ ภ.พ.30"
        
    return {
        "vat_limit": VAT_LIMIT,
        "sample_revenue": sample_revenue,
        "daily_rate": daily_rate,
        "monthly_projected": monthly_projected,
        "annual_projected": annual_projected,
        "pct_of_limit": round(pct_of_limit, 1),
        "days_to_reach": days_to_reach,
        "months_to_reach": months_to_reach,
        "status": status,
        "level_color": level_color,
        "status_text": status_text,
        "advice": advice
    }

