import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from pathlib import Path
import json

import importlib
import db
import analyzer
import tax_calc
import statement_data

importlib.reload(db)
importlib.reload(analyzer)
importlib.reload(tax_calc)
importlib.reload(statement_data)

st.set_page_config(
    page_title="ร้านศรีบุตรา | ระบบบัญชี ภาษี และกระแสเงินสด",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db.init_db()

# Custom Luxury FinTech Dark Styling - High Contrast & Crystal Clear
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* Global Typography - protect icons from distortion */
    html, body, .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Prompt', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    [data-testid="stIconMaterial"], 
    .material-symbols-rounded, 
    .material-symbols-outlined, 
    .material-icons,
    [data-testid="stExpanderToggleIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    }
    
    /* Global Page Background and Spacing */
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 96%;
    }
    
    /* Hero Header Banner */
    .hero-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 22px 26px;
        color: #f8fafc;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        color: #ffffff !important;
    }
    .hero-subtitle {
        font-size: 0.92rem;
        color: #94a3b8 !important;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .badge-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #f8fafc;
    }
    .status-badge.green {
        background: rgba(16, 185, 129, 0.2);
        border-color: rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
    }
    .status-badge.blue {
        background: rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
        color: #93c5fd;
    }
    
    /* Modern Metric Cards - Slate Dark High-Contrast */
    .metric-card-lux {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-card-lux:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        border-color: #475569 !important;
    }
    .metric-card-lux::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .metric-card-lux.blue::before { background: linear-gradient(90deg, #0284c7, #38bdf8); }
    .metric-card-lux.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .metric-card-lux.purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .metric-card-lux.amber::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    
    .metric-label-lux {
        font-size: 0.84rem;
        font-weight: 600;
        color: #94a3b8 !important;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
        line-height: 1.3;
    }
    .metric-value-lux {
        font-size: clamp(1.2rem, 1.6vw, 1.55rem);
        font-weight: 700;
        color: #f8fafc !important;
        line-height: 1.25;
        margin: 4px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-sub-lux {
        font-size: 0.78rem;
        color: #cbd5e1 !important;
        margin-top: 2px;
        line-height: 1.3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Modern Tabs in Dark Theme */
    div[data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #334155 !important;
        padding-bottom: 2px;
        margin-bottom: 18px;
    }
    button[data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 9px 16px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        color: #94a3b8 !important;
        transition: all 0.15s ease-in-out;
    }
    button[data-baseweb="tab"]:hover {
        color: #38bdf8 !important;
        background-color: #1e293b !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e293b !important;
        border-bottom: 3px solid #0284c7 !important;
        color: #38bdf8 !important;
    }
    
    /* Sidebar Styling - Crystal Clear High Contrast */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] label {
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: #e2e8f0 !important;
    }
    
    /* Crisp Input Fields in Sidebar */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] div[data-baseweb="input"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    
    /* File Uploader Container in Sidebar */
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #1e293b !important;
        border: 1px dashed #64748b !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] div {
        color: #cbd5e1 !important;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- OPTIONAL PASSWORD PROTECTION (FOR CLOUD) -----------------
def check_password():
    admin_password = st.secrets.get("ADMIN_PASSWORD", "")
    if not admin_password:
        return True

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div style="max-width: 440px; margin: 40px auto 20px auto; padding: 26px 30px; background: white; border-radius: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; text-align: center;">
        <h2 style="color: #0f172a; margin: 0 0 6px 0; font-size: 1.5rem;">🏪 ร้านศรีบุตรา</h2>
        <p style="color: #64748b; font-size: 0.88rem; margin: 0 0 16px 0;">ระบบวิเคราะห์บัญชี ภาษี และกระแสเงินสด</p>
        <div style="padding: 10px 14px; background: #f0f9ff; border-radius: 10px; color: #0369a1; font-size: 0.84rem; font-weight: 500;">
            🔒 ระบบออนไลน์นี้ได้รับการปกป้อง กรุณาระบุรหัสผ่านเพื่อเข้าใช้งาน
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        pwd = st.text_input("รหัสผ่าน (PIN / Password):", type="password", key="auth_password_input")
        if st.button("🚀 เข้าสู่ระบบ", use_container_width=True, key="btn_auth_login"):
            if pwd == admin_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
    return False

if not check_password():
    st.stop()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 12px; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0;">
        <h2 style="margin: 0; color: #0f172a; font-size: 1.4rem;">🏪 ร้านศรีบุตรา</h2>
        <p style="margin: 2px 0 0 0; font-size: 0.82rem; color: #64748b;">Smart Retail & Tax Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔄 ซิงค์ข้อมูล")
    if st.button("🚀 สแกนและวิเคราะห์ใบเสร็จใหม่", key="btn_scan_receipts", use_container_width=True):
        with st.spinner("กำลังแปลงไฟล์และอัปเดตฐานข้อมูล..."):
            try:
                res = analyzer.analyze_all_receipts()
                st.toast(f"✅ สแกนและประมวลผลสำเร็จ {len(res)} รายการ!", icon="🧾")
                st.success(f"ประมวลผลสำเร็จ {len(res)} รายการ!")
                st.rerun()
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการสแกน: {e}")

    # Check AI Vision Key status
    has_ai_brain = bool(analyzer.get_gemini_api_key())
    if has_ai_brain:
        st.markdown('<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 6px 10px; font-size: 0.78rem; color: #6ee7b7; margin-bottom: 8px;">🧠 <b>AI Vision พร้อมใช้งาน:</b> อ่านภาพถ่ายภาษาไทยอัตโนมัติ</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 6px 10px; font-size: 0.78rem; color: #fde68a; margin-bottom: 8px;">⚠️ <b>ยังไม่พบคีย์ AI:</b> รูปถ่ายจะถูกบันทึกชั่วคราวเพื่อให้กรอกยอดเอง</div>', unsafe_allow_html=True)

    # Direct Drag-and-Drop Receipt Uploader
    uploaded_files = st.file_uploader(
        "📥 ลาก/วางไฟล์ หรือถ่ายรูปใบเสร็จที่นี่:",
        type=["pdf", "html", "htm", "png", "jpg", "jpeg", "docx", "xlsx", "txt"],
        accept_multiple_files=True,
        key="receipt_sidebar_uploader"
    )
    if uploaded_files:
        save_dir = Path(__file__).resolve().parent / "extracted_receipts"
        save_dir.mkdir(parents=True, exist_ok=True)
        uploaded_sig = tuple(sorted((uf.name, uf.size) for uf in uploaded_files))
        if st.session_state.get("_last_uploaded_sig") != uploaded_sig:
            st.session_state["_last_uploaded_sig"] = uploaded_sig
            processed_count = 0
            with st.spinner("🧠 กำลังให้สมอง AI Vision วิเคราะห์สแกนใบเสร็จ..."):
                for uf in uploaded_files:
                    if uf.size == 0:
                        continue
                    target_path = save_dir / uf.name
                    with open(target_path, "wb") as f:
                        f.write(uf.getbuffer())
                    analyzer.process_file(target_path)
                    processed_count += 1
            if processed_count > 0:
                st.toast(f"✅ สแกนและวิเคราะห์ใบเสร็จ {processed_count} ไฟล์สำเร็จเรียบร้อย!", icon="🎉")
                st.rerun()

    if st.button("🔄 บังคับสแกนไฟล์ทั้งหมดใหม่ (Re-scan All)", use_container_width=True):
        with st.spinner("กำลังสแกนและประมวลผลไฟล์ทั้งหมดใหม่อีกครั้ง..."):
            analyzer.analyze_all_receipts()
        st.toast("✅ สแกนและอัปเดตข้อมูลทุกไฟล์เสร็จสิ้น!", icon="🎉")
        st.rerun()

    st.divider()
    st.subheader("🔍 ตัวกรองข้อมูล")

    # Date Range Filter
    today = datetime.today()
    default_start = datetime(today.year, 1, 1)
    
    date_range = st.date_input(
        "ช่วงวันที่",
        value=(default_start, today),
        max_value=today
    )
    
    start_date = None
    end_date = None
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date = date_range[0].strftime("%Y-%m-%d")
        end_date = date_range[1].strftime("%Y-%m-%d")
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = date_range[0].strftime("%Y-%m-%d")

    # Search keyword
    search_keyword = st.text_input("ค้นหา (เลขที่ใบเสร็จ/สาขา/บันทึก)", "")

    st.divider()
    st.caption("พัฒนาด้วย Streamlit • SQLite • Python")

# ----------------- DATA QUERY -----------------
kpis = db.get_kpis(start_date=start_date, end_date=end_date)
receipts_list = db.get_receipts(start_date=start_date, end_date=end_date, search=search_keyword)
spending_trend = db.get_spending_trend(start_date=start_date, end_date=end_date)
top_items = db.get_top_items(limit=10, start_date=start_date, end_date=end_date)
store_breakdown = db.get_store_breakdown()
bank_overall = db.get_bank_summary()
pea_overall = db.get_utility_expenses()

# ----------------- HERO HEADER & KPIS -----------------
st.markdown("""
<div class="hero-header">
    <div>
        <h1 class="hero-title">🏪 ร้านศรีบุตรา | ศูนย์วิเคราะห์บัญชี ภาษี และกระแสเงินสด</h1>
        <p class="hero-subtitle">ระบบบริหารจัดการต้นทุนซื้อสินค้า • สเตตเมนต์ธนาคารกรุงไทย • วางแผนภาษี ภ.ง.ด. 94/90 • เพดาน VAT 1.8M</p>
    </div>
    <div class="badge-container">
        <span class="status-badge green">🟢 ระบบออนไลน์</span>
        <span class="status-badge blue">🧾 168 ใบเสร็จจริง</span>
        <span class="status-badge blue">🏦 744 ธุรกรรม 8 เดือน</span>
        <span class="status-badge">⚡ ค่าไฟ กฟภ. 6 รอบบิล</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card-lux blue">
        <div class="metric-label-lux">💰 ยอดซื้อสินค้าเข้าร้านสะสม</div>
        <div class="metric-value-lux">฿{kpis['total']:,.2f}</div>
        <div class="metric-sub-lux">🧾 เอกสารจริงในระบบ {kpis['count']} ฉบับ</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card-lux green">
        <div class="metric-label-lux">🏦 ยอดเงินรับเข้าสเตตเมนต์จริง</div>
        <div class="metric-value-lux">฿{bank_overall['total_deposit']:,.2f}</div>
        <div class="metric-sub-lux">📊 สถิติ 8 เดือนเต็ม (744 ธุรกรรม)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card-lux purple">
        <div class="metric-label-lux">🏛️ ภาษีซื้อสะสม (Input VAT)</div>
        <div class="metric-value-lux">฿{kpis['total_vat']:,.2f}</div>
        <div class="metric-sub-lux">💳 เครดิตภาษี 7% พร้อมใช้หักภาษีขาย</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card-lux amber">
        <div class="metric-label-lux">⚡ ค่าไฟฟ้าดำเนินงาน (กฟภ.)</div>
        <div class="metric-value-lux">฿{pea_overall['total_amount']:,.2f}</div>
        <div class="metric-sub-lux">💡 ร้านศรีบุตรา 6 รอบบิล (4,822 หน่วย)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab_analytics, tab_receipts, tab_tax, tab_statement, tab_sync = st.tabs([
    "📈 สถิติและแนวโน้ม (Analytics)", 
    "📋 รายการใบเสร็จ (Receipts Explorer)", 
    "💰 จำลองยื่นภาษีร้านศรีบุตรา (ภ.ง.ด. 94 / 90)",
    "🏦 สเตตเมนต์ & เพดาน VAT (Bank Statement & VAT)",
    "⚙️ ตั้งค่าและซิงค์อีเมล (Settings & Sync)"
])



# ----- TAB 1: ANALYTICS -----
with tab_analytics:
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("📅 แนวโน้มยอดซื้อรายวัน / รายเดือน")
        if spending_trend:
            df_trend = pd.DataFrame(spending_trend)
            df_trend["date"] = pd.to_datetime(df_trend["date"])
            
            trend_view = st.radio("มุมมองการแสดงผล:", ["รายวัน", "รายเดือน"], horizontal=True, key="trend_view_toggle")
            
            if trend_view == "รายเดือน":
                df_trend["month_year"] = df_trend["date"].dt.strftime("%Y-%m")
                df_monthly = df_trend.groupby("month_year", as_index=False)["total_spent"].sum()
                # Map to Thai month
                month_names = {"01":"ม.ค.","02":"ก.พ.","03":"มี.ค.","04":"เม.ย.","05":"พ.ค.","06":"มิ.ย.","07":"ก.ค.","08":"ส.ค.","09":"ก.ย.","10":"ต.ค.","11":"พ.ย.","12":"ธ.ค."}
                df_monthly["month_label"] = df_monthly["month_year"].apply(lambda m: f"{month_names.get(m.split('-')[1], m.split('-')[1])} {int(m.split('-')[0])+543}")
                
                fig_trend = px.bar(
                    df_monthly,
                    x="month_label",
                    y="total_spent",
                    text="total_spent",
                    labels={"month_label": "เดือน", "total_spent": "ยอดเงิน (บาท)"},
                    title="ยอดการซื้อสะสมรายเดือน (บาท)",
                    color_discrete_sequence=["#0284c7"],
                    template="plotly_white"
                )
                fig_trend.update_traces(texttemplate='฿%{text:,.0f}', textposition='outside')
                fig_trend.update_layout(
                    font_family="Prompt, sans-serif",
                    xaxis_title="เดือน",
                    yaxis_title="จำนวนเงิน (บาท)",
                    hovermode="x unified",
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                fig_trend = px.bar(
                    df_trend, 
                    x="date", 
                    y="total_spent", 
                    labels={"date": "วันที่", "total_spent": "ยอดเงิน (บาท)"},
                    title="ยอดการซื้อในแต่ละวัน (รายใบเสร็จ)",
                    color_discrete_sequence=["#0284c7"],
                    template="plotly_white"
                )
                fig_trend.update_traces(hovertemplate='<b>วันที่ %{x|%d/%m/%Y}</b><br>ยอดซื้อ: ฿%{y:,.2f}<extra></extra>')
                fig_trend.update_layout(
                    font_family="Prompt, sans-serif",
                    xaxis_title="วันที่", 
                    yaxis_title="จำนวนเงิน (บาท)", 
                    hovermode="x unified",
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("ยังไม่มีข้อมูลค่าใช้จ่ายในช่วงเวลาที่เลือก")

    with col_chart2:
        st.subheader("🏪 สัดส่วนยอดซื้อตามร้านค้า")
        if store_breakdown:
            df_store = pd.DataFrame(store_breakdown)
            fig_store = px.pie(
                df_store,
                names="store_name",
                values="total_amount",
                hole=0.45,
                title="สัดส่วนตามร้านค้า/ผู้ขาย",
                color_discrete_sequence=["#0284c7", "#10b981", "#f59e0b", "#6366f1", "#ec4899"],
                template="plotly_white"
            )
            fig_store.update_traces(textposition='inside', textinfo='percent+label')
            fig_store.update_layout(
                font_family="Prompt, sans-serif",
                margin=dict(t=40, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_store, use_container_width=True)
        else:
            st.info("ยังไม่มีข้อมูลร้านค้า")

    st.divider()

    st.subheader("🏆 10 อันดับสินค้าที่ซื้อบ่อยและยอดรวมสูงสุด")
    if top_items:
        df_top = pd.DataFrame(top_items)
        # Filter out utility description if present
        df_top = df_top[~df_top["item_name"].str.contains("ค่ากระแสไฟฟ้า|PEA", na=False)]
        fig_items = px.bar(
            df_top,
            x="total_spend",
            y="item_name",
            orientation="h",
            text="total_spend",
            labels={"total_spend": "ยอดเงินรวม (บาท)", "item_name": "รายการสินค้า"},
            color="total_qty",
            color_continuous_scale="Blues",
            title="สินค้าที่มียอดซื้อสูงสุด (เรียงตามมูลค่า)",
            template="plotly_white"
        )
        fig_items.update_traces(texttemplate='฿%{text:,.0f}', textposition='outside')
        fig_items.update_layout(
            font_family="Prompt, sans-serif",
            yaxis={'categoryorder':'total ascending'},
            margin=dict(t=40, b=20, l=20, r=100)
        )
        st.plotly_chart(fig_items, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลรายการสินค้า")

# ----- TAB 2: RECEIPTS EXPLORER -----
with tab_receipts:
    st.subheader(f"📑 คลังใบเสร็จและใบกำกับภาษี ({len(receipts_list)} ฉบับ)")
    
    # Auto-detect zero amount / incomplete receipts
    zero_receipts = [r for r in receipts_list if float(r.get("total_amount", 0.0)) == 0.0]
    if zero_receipts:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px;">
            <h4 style="color: #fca5a5; margin: 0 0 6px 0;">🚨 ตรวจพบใบเสร็จที่ยังไม่มียอดเงิน / อ่านข้อความไม่สำเร็จ ({len(zero_receipts)} รายการ)</h4>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0 0 10px 0;">เกิดจากไฟล์รูปถ่ายที่ระบบไม่สามารถดึงตัวหนังสือดิจิทัลได้ สามารถกดลบออก หรือกดให้ AI สแกนอ่านใหม่ได้ทันที:</p>
        </div>
        """, unsafe_allow_html=True)
        z_act1, z_act2 = st.columns([1, 1])
        with z_act1:
            if st.button("🗑️ ลบใบเสร็จยอด ฿0.00 ทั้งหมดออกทันที", key="del_all_zero_recs", type="primary", use_container_width=True):
                for zr in zero_receipts:
                    db.delete_receipt(zr['id'])
                st.toast("✅ ล้างใบเสร็จยอด ฿0.00 ทั้งหมดเรียบร้อยแล้ว!", icon="🗑️")
                st.rerun()
        with z_act2:
            if st.button("🧠 สั่ง AI Vision สแกนอ่านใหม่อีกครั้ง", key="rescan_all_zero_recs", use_container_width=True):
                with st.spinner("กำลังให้ AI Vision สแกนอ่านไฟล์ภาพ..."):
                    analyzer.analyze_all_receipts()
                st.toast("✅ AI Vision สแกนอ่านไฟล์เรียบร้อย!", icon="🎉")
                st.rerun()
        st.write("")
        for zr in zero_receipts:
            zc1, zc2, zc3 = st.columns([3, 1.2, 1.2])
            with zc1:
                st.markdown(f"🔴 **ID: {zr['id']}** | เลขที่: `{zr.get('receipt_number', '-')}` | วันที่: `{zr.get('date', '-')}` | ร้าน: `{zr.get('store_name', '-')}` (฿0.00)")
            with zc2:
                if st.button(f"🗑️ ลบ ID {zr['id']} ทันที", key=f"quick_del_zero_{zr['id']}", type="primary", use_container_width=True):
                    db.delete_receipt(zr['id'])
                    st.toast(f"✅ ลบใบเสร็จ ID {zr['id']} สำเร็จ!", icon="🗑️")
                    st.rerun()
            with zc3:
                with st.popover("✏️ กรอกยอดจริง"):
                    with st.form(f"quick_fix_zero_{zr['id']}"):
                        q_store = st.text_input("ชื่อร้านค้า:", value=zr.get("store_name", "ร้านโดนใจ"))
                        q_total = st.number_input("ยอดเงินจริง (บาท):", value=100.0, step=10.0, format="%.2f")
                        q_vat = st.number_input("VAT (บาท):", value=round(100.0 * 7 / 107, 2), step=5.0, format="%.2f")
                        if st.form_submit_button("💾 บันทึกยอดเงิน", use_container_width=True):
                            db.update_receipt(zr['id'], {
                                "store_name": q_store,
                                "branch": zr.get("branch", ""),
                                "receipt_number": zr.get("receipt_number", ""),
                                "date": zr.get("date", ""),
                                "total_amount": q_total,
                                "subtotal_amount": max(0.0, q_total - q_vat),
                                "vat_amount": q_vat,
                                "payment_method": "เงินสด/โอน",
                                "notes": "แก้ไขยอดด้วยตนเอง"
                            })
                            st.toast("✅ อัปเดตยอดเงินสำเร็จ!", icon="💾")
                            st.rerun()
        st.write("")

    # Store Filter Interactive Selector
    store_options = ["ทั้งหมด", "สยามแม็คโคร", "บิ๊กซี ซูเปอร์เซ็นเตอร์", "เอส.อาร์.ซุปเปอร์มาร์ท", "การไฟฟ้าส่วนภูมิภาค (PEA)", "ออร์โร่ โฮม"]
    chosen_store = st.radio("🏢 กรองตามร้านค้า / ผู้ขาย:", store_options, horizontal=True, key="tab2_store_filter")
    
    filtered_receipts = receipts_list
    if chosen_store != "ทั้งหมด":
        filtered_receipts = [r for r in receipts_list if chosen_store in r.get("store_name", "")]
        st.caption(f"พบ **{len(filtered_receipts)}** ฉบับ จากผู้ขาย '{chosen_store}'")

    # Fast dictionary lookup map
    r_dict = {r["id"]: r for r in filtered_receipts}

    if filtered_receipts:
        # Quick action bar above the table
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            with st.expander("🗑️ ลบใบเสร็จออกจากระบบ (เลือก ID ที่ต้องการลบ)"):
                del_pick_id = st.selectbox(
                    "เลือก ID ใบเสร็จที่ต้องการลบ:",
                    options=[r["id"] for r in filtered_receipts],
                    key="quick_delete_picker",
                    format_func=lambda x: f"ID {x} | เลขที่: {r_dict.get(x, {}).get('receipt_number', '-')} | ฿{r_dict.get(x, {}).get('total_amount', 0):,.2f} ({r_dict.get(x, {}).get('store_name', '')})"
                )
                if del_pick_id:
                    del_info = r_dict.get(del_pick_id, {})
                    st.warning(f"⚠️ ยืนยันลบ: ID {del_pick_id} | {del_info.get('store_name', '')} | ฿{del_info.get('total_amount', 0):,.2f}")
                    if st.button("🗑️ ยืนยันลบรายการนี้", type="primary", use_container_width=True, key=f"btn_confirm_del_top_{del_pick_id}"):
                        db.delete_receipt(del_pick_id)
                        st.toast(f"✅ ลบใบเสร็จ ID {del_pick_id} เรียบร้อยแล้ว!", icon="🗑️")
                        st.rerun()
        with col_m2:
            with st.expander("✏️ แก้ไขข้อมูลใบเสร็จ (เลือก ID เพื่อปรับยอด/ชื่อร้าน)"):
                edit_pick_id = st.selectbox(
                    "เลือก ID ใบเสร็จที่ต้องการแก้ไข:",
                    options=[r["id"] for r in filtered_receipts],
                    key="quick_edit_picker",
                    format_func=lambda x: f"ID {x} | เลขที่: {r_dict.get(x, {}).get('receipt_number', '-')} | ฿{r_dict.get(x, {}).get('total_amount', 0):,.2f} ({r_dict.get(x, {}).get('store_name', '')})"
                )
                if edit_pick_id:
                    e_info = db.get_receipt_detail(edit_pick_id)
                    with st.form(f"form_quick_edit_top_{edit_pick_id}"):
                        qe_store = st.text_input("ชื่อร้านค้า:", value=e_info.get("store_name", ""))
                        qe_rec_no = st.text_input("เลขที่บิล:", value=e_info.get("receipt_number", ""))
                        qe_date = st.text_input("วันที่ (YYYY-MM-DD):", value=e_info.get("date", ""))
                        qe_total = st.number_input("ยอดเงินรวม (บาท):", value=float(e_info.get("total_amount", 0.0)), step=10.0, format="%.2f")
                        qe_vat = st.number_input("VAT (บาท):", value=float(e_info.get("vat_amount", 0.0)), step=5.0, format="%.2f")
                        if st.form_submit_button("💾 บันทึกข้อมูลที่แก้ไข", use_container_width=True):
                            db.update_receipt(edit_pick_id, {
                                "store_name": qe_store,
                                "branch": e_info.get("branch", ""),
                                "receipt_number": qe_rec_no,
                                "date": qe_date,
                                "total_amount": qe_total,
                                "subtotal_amount": max(0.0, qe_total - qe_vat),
                                "vat_amount": qe_vat,
                                "payment_method": e_info.get("payment_method", ""),
                                "notes": e_info.get("notes", "")
                            })
                            st.toast("✅ บันทึกการแก้ไขสำเร็จ!", icon="💾")
                            st.rerun()

        st.write("")
        df_display = pd.DataFrame(filtered_receipts)[["id", "date", "receipt_number", "store_name", "branch", "total_amount", "vat_amount", "payment_method"]]
        df_display.columns = ["ID", "วันที่", "เลขที่ใบเสร็จ", "ร้านค้า", "สาขา", "ยอดรวม (บาท)", "VAT (บาท)", "การชำระเงิน"]
        
        st.dataframe(
            df_display.style.format({"ยอดรวม (บาท)": "฿{:,.2f}", "VAT (บาท)": "฿{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        st.subheader("🔍 ตรวจสอบรายละเอียดใบเสร็จ")
        
        # Fast dictionary lookup map
        r_dict = {r["id"]: r for r in filtered_receipts}
        
        selected_id = st.selectbox(
            "เลือกใบเสร็จที่ต้องการดูรายละเอียด:",
            options=[r["id"] for r in filtered_receipts],
            format_func=lambda x: f"ID: {x} | เลขที่: {r_dict[x].get('receipt_number', '-')} | วันที่: {r_dict[x].get('date', '-')} | ฿{r_dict[x].get('total_amount', 0):,.2f} ({r_dict[x].get('store_name', '')})"
        )
        
        if selected_id:
            detail = db.get_receipt_detail(selected_id)
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                st.write(f"**เลขที่ใบเสร็จ:** `{detail.get('receipt_number', '-')}`")
                st.write(f"**วันที่:** `{detail.get('date', '-')}`")
            with c2:
                st.write(f"**ร้านค้า:** {detail.get('store_name', '-')} {detail.get('branch', '')}")
                st.write(f"**วิธีชำระเงิน:** {detail.get('payment_method', '-')}")
            with c3:
                st.write(f"**ยอดรวมสุทธิ:** `฿{detail.get('total_amount', 0):,.2f}`")
                st.write(f"**ภาษีมูลค่าเพิ่ม:** `฿{detail.get('vat_amount', 0):,.2f}`")
                
            st.markdown("#### รายการสินค้าในใบเสร็จนี้:")
            if detail.get("items"):
                df_items = pd.DataFrame(detail["items"])[["item_name", "quantity", "unit_price", "total_price"]]
                df_items.columns = ["รายการสินค้า", "จำนวน", "ราคา/หน่วย (บาท)", "รวม (บาท)"]
                st.dataframe(
                    df_items.style.format({"ราคา/หน่วย (บาท)": "฿{:,.2f}", "รวม (บาท)": "฿{:,.2f}"}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("ไม่มีรายการสินค้าย่อยในบิลนี้")
                
            # Full Markdown view
            md_path = detail.get("markdown_file")
            if md_path and os.path.exists(md_path):
                with st.expander("📄 ดูโครงสร้าง Markdown ฉบับเต็ม (สกัดโดย MarkItDown)"):
                    with open(md_path, 'r', encoding='utf-8') as f:
                        st.code(f.read(), language="markdown")

            st.write("")
            col_act1, col_act2 = st.columns([1, 1])
            with col_act1:
                with st.expander("✏️ แก้ไขข้อมูลใบเสร็จนี้ (ปรับยอดเงิน/ชื่อร้าน/เลขที่)"):
                    with st.form(f"edit_receipt_form_{selected_id}"):
                        e_store = st.text_input("ชื่อร้านค้า / ผู้ขาย:", value=detail.get("store_name", "ร้านโดนใจ"))
                        e_branch = st.text_input("สาขา:", value=detail.get("branch", "") or "")
                        e_rec_no = st.text_input("เลขที่ใบเสร็จ / บิล:", value=detail.get("receipt_number", "") or "")
                        e_date = st.text_input("วันที่ (YYYY-MM-DD):", value=detail.get("date", "") or "")
                        e_total = st.number_input("ยอดรวมสุทธิ (บาท):", value=float(detail.get("total_amount", 0.0)), step=10.0, format="%.2f")
                        e_vat = st.number_input("ภาษีมูลค่าเพิ่ม VAT (บาท):", value=float(detail.get("vat_amount", 0.0)), step=5.0, format="%.2f")
                        e_payment = st.text_input("ช่องทางการชำระเงิน:", value=detail.get("payment_method", "") or "เงินสด/โอน")
                        e_notes = st.text_input("หมายเหตุเพิ่มเติม:", value=detail.get("notes", "") or "")

                        if st.form_submit_button("💾 บันทึกการแก้ไข", use_container_width=True):
                            db.update_receipt(selected_id, {
                                "store_name": e_store,
                                "branch": e_branch,
                                "receipt_number": e_rec_no,
                                "date": e_date,
                                "total_amount": e_total,
                                "subtotal_amount": max(0.0, e_total - e_vat),
                                "vat_amount": e_vat,
                                "payment_method": e_payment,
                                "notes": e_notes
                            })
                            st.toast("✅ แก้ไขข้อมูลใบเสร็จสำเร็จ!", icon="💾")
                            st.success("บันทึกการแก้ไขเรียบร้อยแล้ว!")
                            st.rerun()

            with col_act2:
                with st.expander("🗑️ ลบใบเสร็จนี้ออกจากระบบ"):
                    st.warning(f"⚠️ ยืนยันการลบใบเสร็จ ID: {selected_id} ({detail.get('receipt_number', '-')})?")
                    confirm_del = st.checkbox("ฉันแน่ใจว่าต้องการลบรายการนี้ออกจากฐานข้อมูล", key=f"confirm_del_{selected_id}")
                    if st.button("🗑️ ยืนยันลบใบเสร็จ", type="primary", use_container_width=True, disabled=not confirm_del, key=f"btn_del_{selected_id}"):
                        db.delete_receipt(selected_id)
                        st.toast(f"🗑️ ลบใบเสร็จ ID: {selected_id} สำเร็จแล้ว!", icon="✅")
                        st.success(f"ลบใบเสร็จ ID {selected_id} เรียบร้อย!")
                        st.rerun()
    else:
        st.warning("ไม่พบรายการใบเสร็จตามเงื่อนไขที่เลือก กรุณากดปุ่ม 'สแกนและวิเคราะห์ใบเสร็จใหม่' ด้านซ้าย")

# ----- TAB 3: TAX SIMULATION (ร้านศรีบุตรา) -----
with tab_tax:
    st.header("💰 ระบบจำลองการยื่นภาษีเงินได้บุคคลธรรมดา ร้านศรีบุตรา")
    st.caption("คำนวณและเปรียบเทียบภาษีตามกฎหมายสรรพากร (มาตรา 40(8) ร้านค้าปลีก/โชห่วย) เพื่อวางแผนลดหย่อนและประหยัดภาษี")
    
    col_t1, col_t2 = st.columns([1, 1])
    with col_t1:
        tax_form_choice = st.radio(
            "📌 เลือกประเภทแบบแสดงรายการภาษีที่ต้องการจำลอง:",
            options=["ภ.ง.ด. 94 (ภาษีครึ่งปี: รายรับ ม.ค. - มิ.ย.)", "ภ.ง.ด. 90 (ภาษีสิ้นปี: รายรับ ม.ค. - ธ.ค.)"],
            horizontal=True
        )
    with col_t2:
        current_year = datetime.today().year
        tax_year = st.selectbox("📅 ประจำปีภาษี:", options=[current_year, current_year - 1], format_func=lambda y: f"ปี ค.ศ. {y} (พ.ศ. {y + 543})")
        
    is_half = "ภ.ง.ด. 94" in tax_form_choice
    
    # Calculate period dates
    if is_half:
        p_start = f"{tax_year}-01-01"
        p_end = f"{tax_year}-06-30"
        default_personal_allowance = 30_000.0  # ครึ่งปี
        st.info("💡 **ภ.ง.ด. 94:** ใช้สำหรับยื่นภาษีช่วง ก.ค. - ก.ย. โดยนำรายได้และค่าใช้จ่าย 6 เดือนแรก (1 ม.ค. - 30 มิ.ย.) มาคำนวณ ค่าลดหย่อนผู้มีเงินได้คำนวณกึ่งหนึ่ง (30,000 บาท)")
    else:
        p_start = f"{tax_year}-01-01"
        p_end = f"{tax_year}-12-31"
        default_personal_allowance = 60_000.0  # เต็มปี
        st.info("💡 **ภ.ง.ด. 90:** ใช้สำหรับยื่นภาษีช่วง ม.ค. - มี.ค. ของปีถัดไป โดยนำรายได้ทั้งปี (1 ม.ค. - 31 ธ.ค.) มาคำนวณ และนำยอดภาษีครึ่งปีที่จ่ายไปแล้วมาเครดิตหักออกได้")
        
    # Query purchases and utilities from DB in this period
    goods_kpis = db.get_goods_purchases(start_date=p_start, end_date=p_end)
    utility_kpis = db.get_utility_expenses(start_date=p_start, end_date=p_end)
    
    db_purchases = float(goods_kpis.get("total_amount", 0.0))
    if db_purchases == 0.0:
        db_purchases = float(kpis.get("total", 0.0))
        
    db_utility = float(utility_kpis.get("total_amount", 0.0))
        
    st.divider()
    
    # Input columns
    col_input_left, col_input_right = st.columns(2)
    
    with col_input_left:
        st.subheader("💵 รายรับและต้นทุนค่าใช้จ่าย")
        
        purchases_input = st.number_input(
            "1. ต้นทุนซื้อสินค้าเข้าร้าน (จากใบเสร็จ Makro, Big C, S.R. Supermart สะสม):",
            value=db_purchases if db_purchases > 0 else 864_152.30,
            step=5_000.0,
            format="%.2f",
            help="ดึงจากยอดรวมใบเสร็จซื้อสินค้าเข้าร้านสะสมในระบบ สามารถปรับแก้ไขได้ตามจริง"
        )
        
        # Bank Statement Sales
        if is_half:
            bank_period_sum = db.get_bank_summary(start_date=p_start, end_date=p_end)
            actual_stmt_sales = float(bank_period_sum.get("total_deposit", 1369253.49))
            sales_label = f"ยอดเงินเข้าสเตตเมนต์จริง 6 เดือนแรก (ม.ค. - มิ.ย. 69): ฿{actual_stmt_sales:,.2f} บาท"
        else:
            bank_all_sum = db.get_bank_summary()
            eight_month_dep = float(bank_all_sum.get("total_deposit", 2038286.49))
            actual_stmt_sales = round((eight_month_dep / 8) * 12, 2)
            sales_label = f"ประมาณการยอดขายเต็มปีจากสเตตเมนต์ 8 เดือน (เฉลี่ย 12 เดือน): ฿{actual_stmt_sales:,.2f} บาท (ยอดจริง 8 เดือน = ฿{eight_month_dep:,.2f})"

        sales_mode = st.radio(
            "📊 แหล่งที่มาของยอดขายหน้าร้าน:",
            options=["ดึงยอดขายจริงจากสเตตเมนต์ธนาคาร (แนะนำ)", "คำนวณประมาณการจากยอดซื้อ (+% กำไร)", "กรอกตัวเลขเอง"],
            horizontal=False
        )
        
        if sales_mode == "ดึงยอดขายจริงจากสเตตเมนต์ธนาคาร (แนะนำ)":
            st.success(f"🏦 {sales_label}")
            gross_sales_val = float(actual_stmt_sales)
        elif sales_mode == "คำนวณประมาณการจากยอดซื้อ (+% กำไร)":
            markup_pct = st.slider("อัตรากำไรเฉลี่ย (% Markup):", 5, 35, 15, 1)
            est_sales = round(purchases_input * (1 + markup_pct / 100.0), 2)
            st.caption(f"ประมาณการยอดขายจากต้นทุน (+{markup_pct}%): **฿{est_sales:,.2f} บาท**")
            gross_sales_val = float(est_sales)
        else:
            gross_sales_val = float(actual_stmt_sales)
            
        gross_sales_input = st.number_input(
            "2. ยอดขายรวมหน้าร้านที่นำไปคิดภาษี (บาท):",
            value=gross_sales_val,
            step=10_000.0,
            format="%.2f"
        )

        
        other_exp_input = st.number_input(
            "3. ค่าใช้จ่ายดำเนินงานอื่นของร้าน (เช่น ค่าไฟ กฟภ., ค่าเช่าร้าน, ค่าขนส่ง):",
            value=db_utility if db_utility > 0 else 0.0,
            step=1_000.0,
            format="%.2f",
            help="รวมค่าไฟฟ้าจาก กฟภ. (บันทึกจากประวัติ PEA Smart Plus ร้านศรีบุตรา) สามารถแก้ไขเพิ่มค่าใช้จ่ายอื่นได้"
        )
        if db_utility > 0:
            st.success(f"⚡ รวมค่าไฟฟ้าจริง กฟภ. ร้านศรีบุตรา ({utility_kpis.get('bill_count', 0)} เดือน): **฿{db_utility:,.2f} บาท** (VAT ฿{utility_kpis.get('total_vat', 0):,.2f})")
            
        with st.expander("⚡ ดูประวัติค่าไฟฟ้า กฟภ. ร้านศรีบุตรา (PEA Smart Plus)"):
            pea_bills = db.get_receipts(store="การไฟฟ้าส่วนภูมิภาค (PEA)")
            if pea_bills:
                df_pea = pd.DataFrame(pea_bills)[["date", "receipt_number", "total_amount", "vat_amount", "notes"]]
                df_pea.columns = ["วันที่", "เลขอ้างอิง PEA", "ยอดรวม (บาท)", "VAT 7% (บาท)", "รายละเอียด"]
                st.dataframe(df_pea.style.format({"ยอดรวม (บาท)": "฿{:,.2f}", "VAT 7% (บาท)": "฿{:,.2f}"}), use_container_width=True, hide_index=True)
                st.caption("💡 สถานที่ใช้ไฟฟ้า: **ร้านศรีบุตรา** (88 ม.12 ต.บ้านกลาง อ.หล่มสัก จ.เพชรบูรณ์ 67110) | หมายเลขผู้ใช้ไฟฟ้า: `020025734423` | รหัสเครื่องวัด: `6500013480` | อัตรา: `1125 กิจการขนาดเล็ก`")

    with col_input_right:
        st.subheader("🛡️ สิทธิค่าลดหย่อนภาษี")
        
        st.write(f"• **ค่าลดหย่อนส่วนตัวผู้มีเงินได้:** ฿{default_personal_allowance:,.2f} บาท (ตามเกณฑ์กฎหมาย)")
        
        has_spouse = st.checkbox("มีคู่สมรส (ไม่มีเงินได้และจดทะเบียนสมรสถูกต้อง)")
        spouse_allowance = (30_000.0 if is_half else 60_000.0) if has_spouse else 0.0
        
        children_count = st.number_input("จำนวนบุตรที่ชอบด้วยกฎหมาย (คน):", min_value=0, max_value=10, value=0, step=1)
        child_rate = 15_000.0 if is_half else 30_000.0
        children_allowance = children_count * child_rate
        
        other_deductions = st.number_input(
            "ลดหย่อนอื่นๆ (เช่น ประกันสังคม, ประกันชีวิต, กองทุน, ดอกเบี้ยกู้บ้าน):",
            value=0.0,
            step=1_000.0,
            format="%.2f"
        )
        
        prepaid_tax = 0.0
        if not is_half:
            prepaid_tax = st.number_input(
                "ภาษีครึ่งปี (ภ.ง.ด. 94) ที่ได้ชำระไปแล้วในระหว่างปี (บาท):",
                value=0.0,
                step=500.0,
                format="%.2f",
                help="นำยอดที่เคยจ่ายตอนยื่น ภ.ง.ด. 94 มาหักออกจากภาษีสิ้นปีได้"
            )
            
        total_allowances = default_personal_allowance + spouse_allowance + children_allowance + other_deductions
        st.success(f"**รวมค่าลดหย่อนทั้งหมด:** ฿{total_allowances:,.2f} บาท")

    # Perform Tax Calculation
    calc_res = tax_calc.compare_tax_methods(
        gross_sales=gross_sales_input,
        actual_purchases=purchases_input,
        other_expenses=other_exp_input,
        allowances=total_allowances,
        is_half_year=is_half,
        prepaid_tax=prepaid_tax
    )
    
    st.divider()
    
    # Tax Savings Hero Banner
    savings = calc_res["tax_savings"]
    if savings > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 22px 26px; border-radius: 16px; margin-bottom: 22px; box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.25);">
            <h2 style="color: white; margin: 0; font-size: 1.6rem;">🎉 ร้านศรีบุตรา ประหยัดภาษีได้สูงสุด: ฿{savings:,.2f} บาท!</h2>
            <p style="margin-top: 8px; font-size: 1rem; opacity: 0.95; line-height: 1.5;">
                ผลการคำนวณแนะนำให้ยื่นแบบ <b>'หักค่าใช้จ่ายตามจริง'</b> เนื่องจากร้านรวบรวมใบเสร็จและใบกำกับภาษี (แม็คโคร, บิ๊กซี, เอส.อาร์. และค่าไฟฟ้า กฟภ.) ไว้อย่างถูกต้องครบถ้วน เสียภาษีจากกำไรจริง ไม่ถูกเหมาคิดกำไร 40%
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: #f0fdf4; color: #166534; padding: 18px 22px; border-radius: 14px; border: 1px solid #bbf7d0; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #166534; font-size: 1.25rem;">💡 ผลการคำนวณ: ภาษีทั้งสองวิธีใกล้เคียงกัน หรืออยู่ในเกณฑ์ยกเว้นภาษี</h3>
            <p style="margin: 6px 0 0 0; font-size: 0.95rem;">ยอดเงินได้สุทธิของคุณยังอยู่ในเกณฑ์ 150,000 บาทแรกที่ได้รับการยกเว้นภาษี หรือวิธีหักเหมา 60% ให้ผลลัพธ์ที่สะดวกกว่า</p>
        </div>
        """, unsafe_allow_html=True)

    # 4 Comparative Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card-lux blue">
            <div class="metric-label-lux">💵 ยอดขายพึงประเมิน</div>
            <div class="metric-value-lux">฿{gross_sales_input:,.2f}</div>
            <div class="metric-sub-lux">ฐานรายรับที่นำไปคิดภาษี</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card-lux green">
            <div class="metric-label-lux">📦 ต้นทุนจริงที่มีใบเสร็จ</div>
            <div class="metric-value-lux">฿{purchases_input:,.2f}</div>
            <div class="metric-sub-lux">แม็คโคร, บิ๊กซี, เอส.อาร์.</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card-lux amber">
            <div class="metric-label-lux">⚖️ ภาษีวิธีเหมา 60%</div>
            <div class="metric-value-lux">฿{calc_res['flat']['tax_net']:,.2f}</div>
            <div class="metric-sub-lux">คิดกำไรเหมา 40%</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card-lux purple">
            <div class="metric-label-lux">🛡️ ภาษีวิธีหักตามจริง</div>
            <div class="metric-value-lux">฿{calc_res['actual']['tax_net']:,.2f}</div>
            <div class="metric-sub-lux">ประหยัดกว่า ฿{savings:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Side-by-Side Comparison Table
    st.subheader(f"📊 ตารางเปรียบเทียบการคำนวณภาษี {calc_res['form_name']}")
    
    comp_data = [
        {"รายการเปรียบเทียบ": "ยอดขายรวม (เงินได้พึงประเมิน)", "วิธีหักเหมา 60%": f"฿{gross_sales_input:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"฿{gross_sales_input:,.2f}"},
        {"รายการเปรียบเทียบ": "หักค่าใช้จ่าย", "วิธีหักเหมา 60%": f"-฿{calc_res['flat']['expenses']:,.2f} (เหมา 60%)", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"-฿{calc_res['actual']['total_expenses']:,.2f} (ตามจริง)"},
        {"รายการเปรียบเทียบ": "หักค่าลดหย่อนรวม", "วิธีหักเหมา 60%": f"-฿{total_allowances:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"-฿{total_allowances:,.2f}"},
        {"รายการเปรียบเทียบ": "เงินได้สุทธิ (เพื่อนำไปคิดภาษี)", "วิธีหักเหมา 60%": f"฿{calc_res['flat']['net_income']:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"฿{calc_res['actual']['net_income']:,.2f}"},
        {"รายการเปรียบเทียบ": "ภาษีคำนวณตามอัตราก้าวหน้า (วิธีที่ 1)", "วิธีหักเหมา 60%": f"฿{calc_res['flat']['tax_method1']:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"฿{calc_res['actual']['tax_method1']:,.2f}"},
        {"รายการเปรียบเทียบ": "ภาษีคำนวณขั้นต่ำ 0.5% (วิธีที่ 2)", "วิธีหักเหมา 60%": f"฿{calc_res['flat']['tax_method2']:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"฿{calc_res['actual']['tax_method2']:,.2f}"},
        {"รายการเปรียบเทียบ": "หักภาษีครึ่งปีที่ชำระไว้แล้ว", "วิธีหักเหมา 60%": f"-฿{prepaid_tax:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"-฿{prepaid_tax:,.2f}"},
        {"รายการเปรียบเทียบ": "ยอดภาษีสุทธิที่ต้องชำระ", "วิธีหักเหมา 60%": f"฿{calc_res['flat']['tax_net']:,.2f}", "วิธีหักตามจริง (มีใบเสร็จรองรับ)": f"฿{calc_res['actual']['tax_net']:,.2f}"},
    ]
    df_comp = pd.DataFrame(comp_data)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)
    
    # Progressive Brackets Detail
    with st.expander("🔍 ดูการแจกแจงขั้นบันไดภาษีอัตราก้าวหน้า (Tax Brackets)"):
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown("**วิธีหักเหมา 60%:**")
            if calc_res["flat"]["bracket_detail"]:
                st.dataframe(pd.DataFrame(calc_res["flat"]["bracket_detail"]), use_container_width=True, hide_index=True)
            else:
                st.write("เงินได้สุทธิไม่เกิน 150,000 บาท ได้รับการยกเว้นภาษีทั้งจำนวน")
        with b_col2:
            st.markdown("**วิธีหักตามจริง (มีใบเสร็จรองรับ):**")
            if calc_res["actual"]["bracket_detail"]:
                st.dataframe(pd.DataFrame(calc_res["actual"]["bracket_detail"]), use_container_width=True, hide_index=True)
            else:
                st.write("เงินได้สุทธิไม่เกิน 150,000 บาท ได้รับการยกเว้นภาษีทั้งจำนวน")
                
    # e-Filing Checklist for ร้านศรีบุตรา
    st.divider()
    st.subheader("📋 ตัวเลขสำคัญสำหรับนำไปกรอกในระบบ e-Filing กรมสรรพากร")
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        st.write(f"• **ประเภทเงินได้:** มาตรา 40(8) การพาณิชย์")
        st.write(f"• **เงินได้พึงประเมิน:** `฿{gross_sales_input:,.2f}`")
    with f_c2:
        chosen_exp = calc_res['actual']['total_expenses'] if savings > 0 else calc_res['flat']['expenses']
        exp_label = "หักตามจริง (มีหลักฐานใบเสร็จ)" if savings > 0 else "หักเหมา 60%"
        st.write(f"• **วิธีหักค่าใช้จ่าย:** {exp_label}")
        st.write(f"• **จำนวนเงินค่าใช้จ่าย:** `฿{chosen_exp:,.2f}`")
    with f_c3:
        final_tax = calc_res['actual']['tax_net'] if savings > 0 else calc_res['flat']['tax_net']
        st.write(f"• **ค่าลดหย่อนรวม:** `฿{total_allowances:,.2f}`")
        st.write(f"• **ยอดภาษีที่ต้องเตรียมชำระ:** `฿{final_tax:,.2f}`")

# ----- TAB 4: BANK STATEMENT & VAT INTELLIGENCE (ร้านศรีบุตรา) -----
with tab_statement:
    st.header("🏦 วิเคราะห์สเตตเมนต์ธนาคาร & เรดาร์เพดาน VAT 1.8 ล้านบาท")
    st.caption("ระบบเชื่อมต่อข้อมูลรายการเดินบัญชีธนาคารกรุงไทย บัญชี 'ร้านศรีบุตรา โดย นายณัฐวุฒิ ศรีบุตรา' (615-3-XXXXX-2)")
    
    # Month Map for all 8 individual months
    MONTH_MAP = {
        "มกราคม": {"dep": 219048.00, "wdr": 259997.50, "dep_cnt": 29, "wdr_cnt": 31, "days": 31, "start": "2026-01-01", "end": "2026-01-31", "label": "มกราคม 2569 (31 วัน)"},
        "กุมภาพันธ์": {"dep": 208762.00, "wdr": 185288.72, "dep_cnt": 17, "wdr_cnt": 34, "days": 28, "start": "2026-02-01", "end": "2026-02-28", "label": "กุมภาพันธ์ 2569 (28 วัน)"},
        "มีนาคม": {"dep": 221984.00, "wdr": 215704.58, "dep_cnt": 24, "wdr_cnt": 28, "days": 31, "start": "2026-03-01", "end": "2026-03-31", "label": "มีนาคม 2569 (31 วัน)"},
        "เมษายน": {"dep": 256821.00, "wdr": 278795.29, "dep_cnt": 42, "wdr_cnt": 40, "days": 30, "start": "2026-04-01", "end": "2026-04-30", "label": "เมษายน 2569 (30 วัน)"},
        "พฤษภาคม": {"dep": 253553.00, "wdr": 243196.65, "dep_cnt": 42, "wdr_cnt": 39, "days": 31, "start": "2026-05-01", "end": "2026-05-31", "label": "พฤษภาคม 2569 (31 วัน)"},
        "มิถุนายน": {"dep": 209085.49, "wdr": 263758.73, "dep_cnt": 79, "wdr_cnt": 47, "days": 30, "start": "2026-06-01", "end": "2026-06-30", "label": "มิถุนายน 2569 (30 วัน)"},
        "กรกฎาคม": {"dep": 296781.00, "wdr": 263512.56, "dep_cnt": 98, "wdr_cnt": 45, "days": 31, "start": "2026-07-01", "end": "2026-07-31", "label": "กรกฎาคม 2569 (31 วัน)"},
        "สิงหาคม": {"dep": 372252.00, "wdr": 407038.16, "dep_cnt": 95, "wdr_cnt": 54, "days": 31, "start": "2026-08-01", "end": "2026-08-31", "label": "สิงหาคม 2569 (31 วัน)"},
    }

    # Month Filter Selector
    sel_col1, sel_col2 = st.columns([2, 1])
    with sel_col1:
        period_option = st.selectbox(
            "📅 เลือกช่วงเวลาสเตตเมนต์ที่ต้องการวิเคราะห์:",
            options=[
                "ภาพรวม 8 เดือนเต็ม (ม.ค. - ส.ค. 2569 | 36 หน้า 744 รายการ)",
                "ครึ่งปีแรก 6 เดือน (ม.ค. - มิ.ย. 2569 | สำหรับยื่น ภ.ง.ด. 94)",
                "สิงหาคม 2569 (01/08/69 - 31/08/69 | แตะเพดาน 1.8M)",
                "กรกฎาคม 2569 (01/07/69 - 31/07/69)",
                "มิถุนายน 2569 (01/06/69 - 30/06/69)",
                "พฤษภาคม 2569 (01/05/69 - 31/05/69)",
                "เมษายน 2569 (01/04/69 - 30/04/69)",
                "มีนาคม 2569 (01/03/69 - 31/03/69)",
                "กุมภาพันธ์ 2569 (01/02/69 - 28/02/69)",
                "มกราคม 2569 (01/01/69 - 31/01/69)"
            ],
            index=1,
            key="statement_period_select"
        )
    with sel_col2:
        st.write("")
        st.write("")
        if "8 เดือนเต็ม" in period_option or "สิงหาคม" in period_option:
            st.error("🚨 **สถานะ VAT:** ยอดขายสะสมทะลุ **1.8 ล้านบาทแล้ว** (+฿238,286.49)")
        elif "ครึ่งปีแรก" in period_option:
            st.success("💼 **ภ.ง.ด. 94:** ยอดขาย 6 เดือน ฿1,369,253.49 (ประหยัดได้ ฿23,308)")
        else:
            st.info(f"📊 แสดงผลข้อมูลเฉพาะเดือน **{period_option.split(' ')[0]}**")

    if "8 เดือนเต็ม" in period_option:
        s_start, s_end, s_days = "2026-01-01", "2026-08-31", 243
        period_label = "มกราคม - สิงหาคม 2569 (8 เดือนเต็ม | 36 หน้า)"
        tot_dep = statement_data.STATEMENT_8_MONTHS_SUMMARY["total_deposits"]
        tot_wdr = statement_data.STATEMENT_8_MONTHS_SUMMARY["total_withdrawals"]
        dep_count = statement_data.STATEMENT_8_MONTHS_SUMMARY["deposit_count"]
        wdr_count = statement_data.STATEMENT_8_MONTHS_SUMMARY["withdrawal_count"]
        tx_count = statement_data.STATEMENT_8_MONTHS_SUMMARY["total_transactions"]
    elif "ครึ่งปีแรก" in period_option:
        s_start, s_end, s_days = "2026-01-01", "2026-06-30", 181
        period_label = "มกราคม - มิถุนายน 2569 (ครึ่งปีแรก 6 เดือนเต็ม)"
        tot_dep = statement_data.STATEMENT_6_MONTHS_SUMMARY["total_deposits"]
        tot_wdr = statement_data.STATEMENT_6_MONTHS_SUMMARY["total_withdrawals"]
        dep_count = 233
        wdr_count = 219
        tx_count = 452
    else:
        # Match single month
        m_key = period_option.split(" ")[0]
        m_info = MONTH_MAP.get(m_key, MONTH_MAP["มกราคม"])
        s_start = m_info["start"]
        s_end = m_info["end"]
        s_days = m_info["days"]
        period_label = m_info["label"]
        tot_dep = m_info["dep"]
        tot_wdr = m_info["wdr"]
        dep_count = m_info["dep_cnt"]
        wdr_count = m_info["wdr_cnt"]
        tx_count = dep_count + wdr_count
    
    # Run VAT Projection Analysis
    vat_analysis = tax_calc.analyze_vat_threshold(tot_dep, days_in_sample=s_days)
    
    # Account Summary Banner
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 18px 22px; border-radius: 14px; border: 1px solid #bae6fd; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #0369a1; font-weight: 700;">🏢 ข้อมูลบัญชี: ร้านศรีบุตรา โดย นายณัฐวุฒิ ศรีบุตรา</h4>
        <p style="margin: 6px 0 0 0; color: #0c4a6e; font-size: 0.92rem;">
            ธนาคารกรุงไทย • สาขาหล่มสัก (615) • เลขที่บัญชี: <code>615-3-XXXXX-2</code> • ช่วงข้อมูลที่เลือก: <b>{period_label}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate Net Cashflow (Inflow - Outflow)
    tot_net = tot_dep - tot_wdr
    
    # 5 Key Statement Metrics
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    with sc1:
        st.markdown(f"""
        <div class="metric-card-lux green">
            <div class="metric-label-lux">📥 ยอดเงินรับเข้าจริง</div>
            <div class="metric-value-lux" style="color: #047857;">฿{tot_dep:,.2f}</div>
            <div class="metric-sub-lux">ทั้งหมด {dep_count} รายการฝาก</div>
        </div>
        """, unsafe_allow_html=True)
    with sc2:
        st.markdown(f"""
        <div class="metric-card-lux amber">
            <div class="metric-label-lux">📤 ยอดเงินจ่ายออกจริง</div>
            <div class="metric-value-lux" style="color: #b91c1c;">฿{tot_wdr:,.2f}</div>
            <div class="metric-sub-lux">ทั้งหมด {wdr_count} รายการถอน</div>
        </div>
        """, unsafe_allow_html=True)
    with sc3:
        if tot_net >= 0:
            st.markdown(f"""
            <div class="metric-card-lux blue">
                <div class="metric-label-lux">💵 รายรับ ลบ รายจ่าย</div>
                <div class="metric-value-lux" style="color: #0284c7;">+฿{tot_net:,.2f}</div>
                <div class="metric-sub-lux" style="color: #10b981; font-weight: 600;">🟢 กระแสเงินสดสุทธิเป็นบวก</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card-lux blue">
                <div class="metric-label-lux">💵 รายรับ ลบ รายจ่าย</div>
                <div class="metric-value-lux" style="color: #e11d48;">-฿{abs(tot_net):,.2f}</div>
                <div class="metric-sub-lux" style="color: #e11d48; font-weight: 600;">🔻 จ่ายมากกว่ารับในรอบนี้</div>
            </div>
            """, unsafe_allow_html=True)
    with sc4:
        st.markdown(f"""
        <div class="metric-card-lux purple">
            <div class="metric-label-lux">📈 พยากรณ์ยอดขายทั้งปี</div>
            <div class="metric-value-lux">฿{vat_analysis['annual_projected']:,.2f}</div>
            <div class="metric-sub-lux">Annual Run-rate จากเงินเข้า</div>
        </div>
        """, unsafe_allow_html=True)
    with sc5:
        if vat_analysis["status"] == "OFFICIALLY_BREACHED":
            st.markdown(f"""
            <div class="metric-card-lux" style="border-top: 4px solid #ef4444;">
                <div class="metric-label-lux">🚨 ทะลุเพดาน VAT แล้ว</div>
                <div class="metric-value-lux" style="color: #b91c1c;">+฿{tot_dep - 1800000.0:,.2f}</div>
                <div class="metric-sub-lux" style="color: #ef4444; font-weight: 600;">เกิน 1.8M ต้องยื่น ภ.พ.01</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card-lux blue">
                <div class="metric-label-lux">⏱️ ประมาณการแตะ 1.8M</div>
                <div class="metric-value-lux">{vat_analysis['months_to_reach']} เดือน</div>
                <div class="metric-sub-lux">{vat_analysis['pct_of_limit']:.1f}% ของเพดาน 1.8M</div>
            </div>
            """, unsafe_allow_html=True)
        
    st.divider()
    
    # VAT Alert Banner
    if vat_analysis["status"] == "OFFICIALLY_BREACHED":
        st.error(f"""
        ### {vat_analysis['status_text']}
        
        {vat_analysis['advice']}
        
        **📌 ไทม์ไลน์สำคัญทางกฎหมาย:**
        1. **วันที่ยอดขายสะสมแตะ 1.8 ล้านบาท:** ช่วงต้นเดือนสิงหาคม 2569 (~03/08/69)
        2. **กรอบเวลา 30 วันตามกฎหมาย (มาตรา 85/1):** ครบกำหนดประมาณ 2 กันยายน 2569
        3. **คำแนะนำเร่งด่วน:** ควรรีบยื่นคำขอจดทะเบียนภาษีมูลค่าเพิ่ม (แบบ ภ.พ.01) ออนไลน์ผ่านเว็บกรมสรรพากรโดยเร็ว เพื่อลดหย่อนเบี้ยปรับล่าช้า และเริ่มนำภาษีซื้อจากบิ๊กซีโดนใจมาหักภาษีขาย
        """)
    elif vat_analysis["status"] == "CRITICAL_OVER":
        st.error(f"### {vat_analysis['status_text']}\n\n{vat_analysis['advice']}")
    elif vat_analysis["status"] == "WARNING_HIGH":
        st.warning(f"### {vat_analysis['status_text']}\n\n{vat_analysis['advice']}")
    else:
        st.success(f"### {vat_analysis['status_text']}\n\n{vat_analysis['advice']}")
        
    st.divider()
    
    # Monthly Cashflow: Inflow - Outflow Breakdown
    st.subheader("💰 สรุปเปรียบเทียบ 'รายรับ ลบ รายจ่าย' รายเดือน (8 เดือนเต็ม)")
    st.caption("คำนวณจากรายการเดินบัญชีจริงธนาคารกรุงไทย (เงินฝากเข้า หักลบ เงินถอนออก) เพื่อดูผลกำไรเงินสดหมุนเวียนสุทธิในแต่ละเดือน")
    
    monthly_flow_data = [
        {"เดือน": "มกราคม 2569", "รายรับเข้า (ฝาก)": 219048.00, "รายจ่ายออก (ถอน)": 259997.50, "ส่วนต่าง (รับ - จ่าย)": -40949.50, "สถานะเงินสด": "🔻 จ่ายมากกว่ารับ ฿40,949.50", "ยอดคงเหลือสิ้นเดือน": 106352.91},
        {"เดือน": "กุมภาพันธ์ 2569", "รายรับเข้า (ฝาก)": 208762.00, "รายจ่ายออก (ถอน)": 185288.72, "ส่วนต่าง (รับ - จ่าย)": 23473.28, "สถานะเงินสด": "🟢 เงินสดเหลือบวก ฿23,473.28", "ยอดคงเหลือสิ้นเดือน": 129826.19},
        {"เดือน": "มีนาคม 2569", "รายรับเข้า (ฝาก)": 221984.00, "รายจ่ายออก (ถอน)": 215704.58, "ส่วนต่าง (รับ - จ่าย)": 6279.42, "สถานะเงินสด": "🟢 เงินสดเหลือบวก ฿6,279.42", "ยอดคงเหลือสิ้นเดือน": 136105.61},
        {"เดือน": "เมษายน 2569", "รายรับเข้า (ฝาก)": 256821.00, "รายจ่ายออก (ถอน)": 278795.29, "ส่วนต่าง (รับ - จ่าย)": -21974.29, "สถานะเงินสด": "🔻 จ่ายมากกว่ารับ ฿21,974.29", "ยอดคงเหลือสิ้นเดือน": 114131.32},
        {"เดือน": "พฤษภาคม 2569", "รายรับเข้า (ฝาก)": 253553.00, "รายจ่ายออก (ถอน)": 243196.65, "ส่วนต่าง (รับ - จ่าย)": 10356.35, "สถานะเงินสด": "🟢 เงินสดเหลือบวก ฿10,356.35", "ยอดคงเหลือสิ้นเดือน": 124487.67},
        {"เดือน": "มิถุนายน 2569", "รายรับเข้า (ฝาก)": 209085.49, "รายจ่ายออก (ถอน)": 263758.73, "ส่วนต่าง (รับ - จ่าย)": -54673.24, "สถานะเงินสด": "🔻 จ่ายมากกว่ารับ ฿54,673.24", "ยอดคงเหลือสิ้นเดือน": 69661.94},
        {"เดือน": "กรกฎาคม 2569", "รายรับเข้า (ฝาก)": 296781.00, "รายจ่ายออก (ถอน)": 263512.56, "ส่วนต่าง (รับ - จ่าย)": 33268.44, "สถานะเงินสด": "🟢 เงินสดเหลือบวก ฿33,268.44", "ยอดคงเหลือสิ้นเดือน": 103082.87},
        {"เดือน": "สิงหาคม 2569", "รายรับเข้า (ฝาก)": 372252.00, "รายจ่ายออก (ถอน)": 407038.16, "ส่วนต่าง (รับ - จ่าย)": -34786.16, "สถานะเงินสด": "🔻 จ่ายมากกว่ารับ ฿34,786.16", "ยอดคงเหลือสิ้นเดือน": 68296.71},
    ]
    df_flow = pd.DataFrame(monthly_flow_data)
    
    # Highlight positive/negative values
    def highlight_net(val):
        color = '#155724' if val > 0 else '#721c24'
        bg = '#d4edda' if val > 0 else '#f8d7da'
        return f'color: {color}; background-color: {bg}; font-weight: bold;'

    st.dataframe(
        df_flow.style.format({
            "รายรับเข้า (ฝาก)": "฿{:,.2f}",
            "รายจ่ายออก (ถอน)": "฿{:,.2f}",
            "ส่วนต่าง (รับ - จ่าย)": "฿{:,.2f}",
            "ยอดคงเหลือสิ้นเดือน": "฿{:,.2f}"
        }).map(highlight_net, subset=["ส่วนต่าง (รับ - จ่าย)"]),
        use_container_width=True,
        hide_index=True
    )
    
    # 3 Summary metric pills below table
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    with col_sum1:
        st.info("💡 **รวมครึ่งปีแรก (ม.ค. - มิ.ย. 69):**\n- รายรับรวม: `฿1,369,253.49`\n- รายจ่ายรวม: `฿1,446,741.47`\n- **ส่วนต่างสุทธิ:** `-฿77,487.98 บาท`")
    with col_sum2:
        st.warning("📊 **รวม 8 เดือนเต็ม (ม.ค. - ส.ค. 69):**\n- รายรับรวม: `฿2,038,286.49`\n- รายจ่ายรวม: `฿2,117,292.19`\n- **ส่วนต่างสุทธิ:** `-฿79,005.70 บาท`")
    with col_sum3:
        st.success("🏦 **การกระทบยอดบัญชี (Reconciliation):**\n- เงินยกมาต้นปี: `฿147,302.41`\n- ส่วนต่างสุทธิ 8 เดือน: `-฿79,005.70`\n- **ยอดคงเหลือสิ้นเดือน ส.ค.:** `฿68,296.71 บาท`")

    # Grouped Bar & Net Cashflow Line Chart (Modernized without overlapping text)
    fig_flow = go.Figure()
    month_names_short = [m["เดือน"].replace(" 2569", "") for m in monthly_flow_data]
    
    fig_flow.add_trace(go.Bar(
        x=month_names_short,
        y=[m["รายรับเข้า (ฝาก)"] for m in monthly_flow_data],
        name="รายรับเข้า (ฝาก)",
        marker_color="#10b981",
        hovertemplate="<b>%{x}</b><br>📥 รายรับเข้า: ฿%{y:,.2f}<extra></extra>"
    ))
    fig_flow.add_trace(go.Bar(
        x=month_names_short,
        y=[m["รายจ่ายออก (ถอน)"] for m in monthly_flow_data],
        name="รายจ่ายออก (ถอน)",
        marker_color="#f43f5e",
        hovertemplate="<b>%{x}</b><br>📤 รายจ่ายออก: ฿%{y:,.2f}<extra></extra>"
    ))
    fig_flow.add_trace(go.Scatter(
        x=month_names_short,
        y=[m["ส่วนต่าง (รับ - จ่าย)"] for m in monthly_flow_data],
        name="ส่วนต่างสุทธิ (รับ - จ่าย)",
        mode="lines+markers+text",
        marker=dict(size=10, color="#0284c7"),
        line=dict(width=3, color="#0284c7"),
        text=[f"{'+' if m['ส่วนต่าง (รับ - จ่าย)'] > 0 else ''}฿{m['ส่วนต่าง (รับ - จ่าย)']:,.0f}" for m in monthly_flow_data],
        textposition="top center",
        textfont=dict(size=11, family="Prompt, sans-serif"),
        hovertemplate="<b>%{x}</b><br>💵 ส่วนต่างสุทธิ: ฿%{y:,.2f}<extra></extra>"
    ))
    fig_flow.update_layout(
        template="plotly_white",
        font_family="Prompt, sans-serif",
        title="📈 กราฟเปรียบเทียบรายรับเข้า vs รายจ่ายออก และส่วนต่างสุทธิรายเดือน",
        barmode="group",
        xaxis_title="เดือน",
        yaxis_title="จำนวนเงิน (บาท)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=50, b=30, l=30, r=30)
    )
    st.plotly_chart(fig_flow, use_container_width=True)

    
    st.divider()
    
    # Visual Analytics (Charts)
    col_v1, col_v2 = st.columns([1, 1])
    
    with col_v1:
        st.subheader("🥧 สัดส่วนรายรับแยกตามช่องทาง (Inflow Breakdown)")
        channel_data = db.get_revenue_by_channel(start_date=s_start, end_date=s_end)
        if channel_data:
            df_ch = pd.DataFrame(channel_data)
            ch_names = {
                "Welfare": "บัตรสวัสดิการแห่งรัฐ (กรมบัญชีกลาง)",
                "Paotang": "แอปเป๋าตัง / ถุงเงิน (Paotang Credit)",
                "Cash_ADM": "เงินสดฝากตู้ ADM",
                "Transfer_In": "เงินโอนทั่วไป / พร้อมเพย์",
                "Interest": "ดอกเบี้ยเงินฝาก"
            }
            df_ch["channel_label"] = df_ch["channel"].map(lambda x: ch_names.get(x, x))
            fig_ch = px.pie(
                df_ch,
                names="channel_label",
                values="total_amount",
                hole=0.45,
                title=f"โครงสร้างรายรับร้านศรีบุตรา ({period_label})",
                color_discrete_sequence=px.colors.qualitative.Safe,
                template="plotly_white"
            )
            fig_ch.update_traces(textposition='inside', textinfo='percent+label')
            fig_ch.update_layout(
                font_family="Prompt, sans-serif",
                margin=dict(t=40, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_ch, use_container_width=True)
        else:
            st.info("💡 ข้อมูลช่องทางรายรับรวมของช่วงเวลานี้จัดเก็บในรายงานสรุปภาพรวม สามารถดูยอดเงินเข้า-ออกและสัดส่วนได้จากการ์ดด้านบน")
            
    with col_v2:
        st.subheader("📊 การเคลื่อนไหวเงินเข้า-ออกรายวัน (Daily Cashflow)")
        daily_inflows = db.get_daily_bank_inflows(start_date=s_start, end_date=s_end)
        if daily_inflows:
            df_daily = pd.DataFrame(daily_inflows)
            fig_daily = go.Figure()
            fig_daily.add_trace(go.Bar(
                x=df_daily["date"],
                y=df_daily["daily_inflow"],
                name="เงินรับเข้า (รายรับ)",
                marker_color="#10b981",
                hovertemplate="<b>วันที่ %{x}</b><br>📥 เงินเข้า: ฿%{y:,.2f}<extra></extra>"
            ))
            fig_daily.add_trace(go.Bar(
                x=df_daily["date"],
                y=df_daily["daily_outflow"],
                name="เงินจ่ายออก (ค่าใช้จ่าย)",
                marker_color="#f43f5e",
                hovertemplate="<b>วันที่ %{x}</b><br>📤 เงินออก: ฿%{y:,.2f}<extra></extra>"
            ))
            fig_daily.update_layout(
                template="plotly_white",
                font_family="Prompt, sans-serif",
                barmode='group',
                title=f"เปรียบเทียบเงินเข้า - เงินออกรายวัน ({period_label})",
                xaxis_title="วันที่",
                yaxis_title="บาท",
                hovermode="x unified",
                margin=dict(t=40, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        else:
            st.info("💡 ข้อมูลสถิติการเคลื่อนไหวเงินเข้า-ออกบันทึกครบถ้วนในกราฟแท่งเปรียบเทียบ 8 เดือนด้านบน")
            
    st.divider()
    
    # Transactions Explorer
    st.subheader(f"📑 ตรวจสอบรายการเดินบัญชี ({tx_count} รายการ)")
    filter_channel = st.selectbox("กรองตามช่องทางธุรกรรม:", ["ทั้งหมด", "Welfare", "Paotang", "Cash_ADM", "Transfer_In", "Biller", "Transfer", "CGSWP"])
    
    tx_rows = db.get_bank_transactions(start_date=s_start, end_date=s_end, channel=filter_channel, limit=1000)
    if tx_rows:
        df_tx = pd.DataFrame(tx_rows)[["date", "time", "tx_type", "description", "channel", "deposit", "withdrawal", "balance"]]
        df_tx.columns = ["วันที่", "เวลา", "ประเภทรายการ", "คำอธิบาย/หมายเลขอ้างอิง", "หมวดหมู่", "เงินฝากเข้า (บาท)", "เงินถอนออก (บาท)", "ยอดคงเหลือ (บาท)"]
        st.dataframe(
            df_tx.style.format({
                "เงินฝากเข้า (บาท)": lambda x: f"฿{x:,.2f}" if x > 0 else "-",
                "เงินถอนออก (บาท)": lambda x: f"฿{x:,.2f}" if x > 0 else "-",
                "ยอดคงเหลือ (บาท)": "฿{:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(f"💡 ไม่พบรายการธุรกรรมในช่องทาง '{filter_channel}' สำหรับช่วงเวลา {period_label} ที่เลือก")

# ----- TAB 5: SETTINGS & SYNC -----


with tab_sync:
    st.subheader("⚙️ สถานะการเชื่อมต่ออีเมล & การตั้งค่า")
    
    config_path = Path(__file__).resolve().parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        st.success("พบไฟล์การตั้งค่า `config.json`")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write(f"**IMAP Server:** `{cfg.get('imap_server', '-')}`")
            st.write(f"**Keywords ค้นหา:** `{', '.join(cfg.get('search_keywords', []))}`")
        with col_s2:
            st.write(f"**ไดเรกทอรีจัดเก็บ:** `{cfg.get('save_directory', '-')}`")
            st.write(f"**ไฟล์ประวัติ:** `{cfg.get('processed_emails_file', '-')}`")
    else:
        st.info("ไม่พบไฟล์ config.json")
        
    st.divider()
    st.subheader("📥 ดึงอีเมลใหม่จากเซิร์ฟเวอร์ Gmail/IMAP")
    st.write("คุณสามารถสั่งรันการดึงอีเมลใหม่เข้ามายังโฟลเดอร์ `extracted_receipts` ได้โดยตรง:")
    if st.button("📨 ดึงอีเมลใบเสร็จจากกล่องจดหมาย (Run fetch_receipts.py)", use_container_width=True):
        with st.spinner("กำลังเชื่อมต่อเซิร์ฟเวอร์อีเมลและดาวน์โหลดใบเสร็จ..."):
            import subprocess
            try:
                result = subprocess.run(["python", "fetch_receipts.py"], capture_output=True, text=True, cwd=str(Path(__file__).resolve().parent))
                st.text_area("Log การดึงอีเมล:", result.stdout or result.stderr, height=150)
                # Auto analyze
                analyzer.analyze_all_receipts()
                st.success("ดึงอีเมลและวิเคราะห์ลงฐานข้อมูลเรียบร้อย!")
                st.rerun()
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการดึงอีเมล: {e}")
