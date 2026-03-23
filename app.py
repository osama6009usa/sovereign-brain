"""
⬡ مركز القيادة السيادي — مجلس أبو عبدالله
النسخة النهائية المتكاملة
"""

import streamlit as st
import anthropic
import pandas as pd
import requests
import smtplib
import base64
import json
import os
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# PDF
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Supabase
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# ─────────────────────────────────────────
st.set_page_config(page_title="⬡ مجلس أبو عبدالله", page_icon="⬡", layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────
# CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&family=IBM+Plex+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{direction:rtl;text-align:right;font-family:'Tajawal',sans-serif!important;background-color:#0A0F1E!important;color:#E8EDF5!important;}
#MainMenu,footer,header{visibility:hidden;}.stDeployButton{display:none;}
.main .block-container{padding:1.2rem 1.8rem;max-width:1350px;background:#0A0F1E;}
[data-testid="stSidebar"]{background:#06080F!important;border-left:1px solid rgba(201,168,76,0.18)!important;}
[data-testid="stSidebar"]>div:first-child{padding:0.8rem;}
.msg-ai{background:rgba(22,32,64,0.8);border:1px solid rgba(155,89,182,0.25);border-radius:14px 14px 14px 0;padding:1rem 1.2rem;margin:0.5rem 0;font-size:0.88rem;line-height:1.8;direction:rtl;color:#E8EDF5;}
.msg-user{background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.25);border-radius:14px 14px 0 14px;padding:1rem 1.2rem;margin:0.5rem 0;font-size:0.88rem;direction:rtl;color:#E8C97A;}
.stTextArea textarea,.stTextInput input{direction:rtl!important;text-align:right!important;font-family:'Tajawal',sans-serif!important;background:rgba(22,32,64,0.7)!important;border:1px solid rgba(201,168,76,0.25)!important;color:#E8EDF5!important;border-radius:8px!important;}
.stButton button{background:rgba(201,168,76,0.1)!important;border:1px solid rgba(201,168,76,0.28)!important;color:#E8C97A!important;font-family:'Tajawal',sans-serif!important;font-weight:700!important;border-radius:7px!important;}
.stButton button:hover{background:rgba(201,168,76,0.2)!important;}
.pc{background:rgba(22,32,64,0.6);border:1px solid rgba(201,168,76,0.18);border-radius:10px;padding:0.75rem;text-align:center;}
.pc.d{border-color:rgba(231,76,60,0.45);background:rgba(231,76,60,0.06);}
.pc.w{border-color:rgba(230,126,34,0.4);background:rgba(230,126,34,0.05);}
.pc.ok{border-color:rgba(46,204,113,0.4);background:rgba(46,204,113,0.05);}
.pl{font-size:0.58rem;color:#A8B8CC;margin-bottom:0.2rem;}
.pv{font-family:'IBM Plex Mono',monospace;font-size:1.05rem;font-weight:700;}
.pg{font-size:0.6rem;margin-top:0.15rem;}
.sok{background:rgba(46,204,113,0.1);border:1px solid rgba(46,204,113,0.3);color:#69db7c;padding:0.2rem 0.65rem;border-radius:100px;font-size:0.65rem;font-weight:700;display:inline-block;}
.swarn{background:rgba(231,76,60,0.1);border:1px solid rgba(231,76,60,0.3);color:#ff8a80;padding:0.2rem 0.65rem;border-radius:100px;font-size:0.65rem;font-weight:700;display:inline-block;}
.sinfo{background:rgba(52,152,219,0.1);border:1px solid rgba(52,152,219,0.3);color:#74c0fc;padding:0.2rem 0.65rem;border-radius:100px;font-size:0.65rem;font-weight:700;display:inline-block;}
.shdr{background:linear-gradient(135deg,rgba(22,32,64,0.95),rgba(15,23,41,0.9));border:1px solid rgba(201,168,76,0.25);border-top:2px solid #C9A84C;border-radius:14px;padding:1.1rem 1.6rem;margin-bottom:1.1rem;}
.alert-r{background:rgba(231,76,60,0.07);border:1px solid rgba(231,76,60,0.28);border-right:3px solid #E74C3C;border-radius:8px;padding:0.75rem 1rem;font-size:0.77rem;color:#ff8a80;direction:rtl;margin:0.5rem 0;}
.alert-g{background:rgba(46,204,113,0.06);border:1px solid rgba(46,204,113,0.25);border-right:3px solid #2ECC71;border-radius:8px;padding:0.75rem 1rem;font-size:0.77rem;color:#69db7c;direction:rtl;margin:0.5rem 0;}
.cal-item{background:rgba(22,32,64,0.5);border:1px solid rgba(201,168,76,0.15);border-radius:8px;padding:0.65rem 1rem;margin-bottom:0.4rem;direction:rtl;}
.hist-row{background:rgba(22,32,64,0.5);border:1px solid rgba(201,168,76,0.12);border-radius:8px;padding:0.6rem 0.9rem;margin-bottom:0.35rem;font-size:0.75rem;direction:rtl;}
hr{border-color:rgba(201,168,76,0.13)!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
SHEET_ID  = "1RsCPeUcMZEU05cJ7Ge6zaQyayFYtXIAe93zHOcXSKpQ"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

STOCKS_META = {
    "2001":{"name":"كيمانول",        "cost":19.30, "shares":2072},
    "4164":{"name":"النهدي",          "cost":126.24,"shares":338},
    "4051":{"name":"باعظيم",          "cost":7.43,  "shares":5480},
    "4007":{"name":"الحمادي",         "cost":39.94, "shares":1841},
    "2330":{"name":"المتقدمة",        "cost":40.85, "shares":867},
    "2222":{"name":"أرامكو",          "cost":28.68, "shares":1583},
    "4250":{"name":"جبل عمر",        "cost":23.89, "shares":3604},
    "3010":{"name":"أسمنت العربية",  "cost":35.73, "shares":580},
    "4336":{"name":"ملكية ريت",      "cost":5.00,  "shares":1510},
    "4325":{"name":"مسار",           "cost":22.78, "shares":939},
    "LCID":{"name":"Lucid (LCID)",   "cost":28.27, "shares":152},
}

SESSIONS = [
    {"date":"2026-03-22","title":"⬡ الجلسة الجراحية — أسهم + كريبتو","who":"PTJ·بوري·سوروس·تشانوس·مونجر","color":"#E74C3C","urgent":True},
    {"date":"2026-03-29","title":"⬡ تقرير الفائض الضائع + ميزانية الحقيقة","who":"بوري + PwC","color":"#E67E22","urgent":False},
    {"date":"2026-03-31","title":"🏠 تقييمات عقارية + تسوية الجله","who":"بويز + لي كا شينج","color":"#E67E22","urgent":False},
    {"date":"2026-04-01","title":"📊 التقرير الشهري الموحد","who":"تيم كوك","color":"#2ECC71","urgent":False},
    {"date":"2026-04-05","title":"⬡ ROT الأراضي + معادلات الخروج","who":"آيكان + لي + بويز","color":"#3498DB","urgent":False},
]

PAGES = [
    ("📊","لوحة القيادة"), ("🧠","غرفة المشورة"), ("📅","الجلسات"),
    ("📎","رفع الملفات"), ("🔍","بحث الويب"), ("📈","الأسعار التاريخية"),
    ("👥","المجلس"), ("📁","التقارير"), ("🎯","القناصون"),
    ("⚖️","الحوكمة"), ("📜","الذاكرة"),
]

# ─────────────────────────────────────────
# SECRETS HELPER
# ─────────────────────────────────────────
def secret(key, fallback=None):
    try: return st.secrets[key]
    except: return fallback

# ─────────────────────────────────────────
# SUPABASE CLIENT
# ─────────────────────────────────────────
@st.cache_resource
def get_supabase():
    if not SUPABASE_AVAILABLE: return None
    url  = secret("SUPABASE_URL")
    key  = secret("SUPABASE_KEY")
    if not url or not key: return None
    try: return create_client(url, key)
    except: return None

def db_save_message(role, content):
    sb = get_supabase()
    if not sb: return
    try:
        sb.table("messages").insert({
            "role": role, "content": content[:4000],
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except: pass

def db_load_messages(limit=50):
    sb = get_supabase()
    if not sb: return []
    try:
        res = sb.table("messages").select("*").order("created_at", desc=False).limit(limit).execute()
        return [{"role": r["role"], "content": r["content"]} for r in (res.data or [])]
    except: return []

def db_clear_messages():
    sb = get_supabase()
    if not sb: return
    try: sb.table("messages").delete().neq("id", 0).execute()
    except: pass

def db_save_price_snapshot(prices: dict):
    sb = get_supabase()
    if not sb: return
    try:
        sb.table("price_history").insert({
            "snapshot": json.dumps(prices),
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except: pass

def db_load_price_history(limit=10):
    sb = get_supabase()
    if not sb: return []
    try:
        res = sb.table("price_history").select("*").order("created_at", desc=True).limit(limit).execute()
        out = []
        for r in (res.data or []):
            out.append({"time": r["created_at"], "prices": json.loads(r["snapshot"])})
        return out
    except: return []

# ─────────────────────────────────────────
# NOTIFICATIONS
# ─────────────────────────────────────────
def send_email(subject, body_html):
    email = secret("EMAIL_ADDRESS")
    passw = secret("EMAIL_PASSWORD")
    if not email or not passw: return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = email
        msg["To"]      = email
        msg.attach(MIMEText(body_html, "html", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as s:
            s.login(email, passw)
            s.sendmail(email, email, msg.as_string())
        return True
    except Exception as e:
        return False

def send_telegram(text):
    token   = secret("TELEGRAM_BOT_TOKEN")
    chat_id = secret("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=10)
        return r.status_code == 200
    except: return False

def check_and_notify(prices):
    """يتحقق من الأسهم التي تجاوزت 20% ويرسل تنبيهات"""
    surgical = []
    for sym, info in STOCKS_META.items():
        p = prices.get(sym)
        if not p: continue
        loss = ((p - info["cost"]) / info["cost"]) * 100
        if loss <= -20:
            surgical.append((info["name"], sym, p, loss))
    if not surgical: return

    now_str = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    # إعداد رسالة البريد
    rows = "".join([
        f"<tr><td style='padding:6px 10px;'>{n}({s})</td>"
        f"<td style='padding:6px 10px;color:#E74C3C;font-weight:bold;'>{p:.2f} ر</td>"
        f"<td style='padding:6px 10px;color:#E74C3C;'>{l:.1f}%</td></tr>"
        for n,s,p,l in surgical
    ])
    email_html = f"""
    <div dir="rtl" style="font-family:Arial;background:#0A0F1E;color:#E8EDF5;padding:20px;border-radius:12px;">
    <h2 style="color:#C9A84C;">⬡ مجلس أبو عبدالله — تنبيه جراحي</h2>
    <p style="color:#ff8a80;font-size:16px;">🔴 الأسهم التالية تجاوزت حد وقف الخسارة 20% في {now_str}</p>
    <table border="1" style="border-collapse:collapse;width:100%;color:#E8EDF5;">
    <tr style="background:#162040;"><th style="padding:8px;">السهم</th><th>السعر</th><th>الخسارة</th></tr>
    {rows}
    </table>
    <p style="color:#A8B8CC;margin-top:15px;">⚖️ قانون وقف الخسارة القطعي: تنفيذ آلي فوري — لا أمل — لا انتظار</p>
    </div>"""

    # رسالة Telegram
    tg_lines = [f"⬡ <b>مجلس أبو عبدالله — تنبيه جراحي</b>\n🔴 {now_str}\n"]
    for n,s,p,l in surgical:
        tg_lines.append(f"🔴 <b>{n}</b> ({s}): {p:.2f} ر | خسارة {l:.1f}%")
    tg_lines.append("\n⚖️ وقف الخسارة 20% — قرار عاجل مطلوب")

    send_email(f"🔴 تنبيه جراحي — {len(surgical)} أسهم تجاوزت 20%", email_html)
    send_telegram("\n".join(tg_lines))

# ─────────────────────────────────────────
# PDF REPORT
# ─────────────────────────────────────────
def generate_pdf(prices):
    if not PDF_AVAILABLE: return None
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Header
        pdf.set_fill_color(10, 15, 30)
        pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(201, 168, 76)
        pdf.cell(0, 15, "Sovereign Council - Portfolio Report", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(168, 184, 204)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}", ln=True, align="C")
        pdf.ln(5)

        # KPIs
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(201, 168, 76)
        pdf.cell(0, 10, "Portfolio Overview", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(232, 237, 245)
        kpis = [
            ("Monthly Income", "103,959 SAR"),
            ("Monthly Surplus", "58,924 SAR (56.7%)"),
            ("Total Deposits", "3,735,756 SAR"),
            ("Total Debt", "2,815,970 SAR"),
            ("Family Safety Valve", "270,208 SAR"),
        ]
        for label, val in kpis:
            pdf.cell(80, 7, label + ":", border=0)
            pdf.cell(0, 7, val, ln=True)
        pdf.ln(5)

        # Stocks Table
        if prices:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 10, "Stock Portfolio - Live Prices", ln=True)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(22, 32, 64)
            pdf.set_text_color(232, 197, 122)
            headers = ["Symbol", "Name", "Cost", "Current", "Loss%", "Status"]
            widths  = [20, 45, 25, 25, 20, 30]
            for h, w in zip(headers, widths):
                pdf.cell(w, 8, h, border=1, fill=True, align="C")
            pdf.ln()

            for sym, info in STOCKS_META.items():
                p = prices.get(sym)
                if not p: continue
                loss = ((p - info["cost"]) / info["cost"]) * 100
                status = "SURGICAL" if loss <= -20 else "WATCH" if loss < 0 else "OK"
                if loss <= -20: pdf.set_text_color(231, 76, 60)
                elif loss < 0:  pdf.set_text_color(230, 126, 34)
                else:           pdf.set_text_color(46, 204, 113)
                pdf.set_font("Helvetica", "", 8)
                row = [sym, info["name"], f"{info['cost']:.2f}", f"{p:.2f}", f"{loss:.1f}%", status]
                for val, w in zip(row, widths):
                    pdf.cell(w, 7, str(val), border=1, align="C")
                pdf.ln()
                pdf.set_text_color(232, 237, 245)
            pdf.ln(5)

        # Sessions
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(201, 168, 76)
        pdf.cell(0, 10, "Upcoming Council Sessions", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(232, 237, 245)
        for s in SESSIONS:
            pdf.cell(30, 7, s["date"], border=0)
            pdf.cell(0, 7, s["title"][:60], ln=True)

        # Footer
        pdf.set_y(-20)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 110, 130)
        pdf.cell(0, 5, "Confidential - Abu Abdullah Sovereign Council - Sovereign Charter V10.0", align="C")

        buf = BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        buf.write(pdf_bytes)
        buf.seek(0)
        return buf
    except Exception as e:
        return None

# ─────────────────────────────────────────
# PRICES
# ─────────────────────────────────────────
def fetch_prices():
    try:
        r = requests.get(SHEET_URL, timeout=15); r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        df.columns = [c.strip().lower() for c in df.columns]
        out = {}
        for _, row in df.iterrows():
            sym = str(row.get("symbol","")).strip()
            raw = row.get("price", None)
            if raw and str(raw).strip() not in ("","#N/A","nan","#ERROR!"):
                try:
                    p = float(str(raw).replace(",","").strip())
                    if p > 0: out[sym] = round(p, 2)
                except: pass
        return out, None
    except Exception as e: return {}, str(e)

def prices_ctx_str():
    if not st.session_state.prices: return ""
    lines = []
    for sym, info in STOCKS_META.items():
        p = st.session_state.prices.get(sym)
        if p:
            loss = ((p - info["cost"]) / info["cost"]) * 100
            c = "$" if sym == "LCID" else "ر"
            s = "🔴 جراحي" if loss <= -20 else "🟡 متابعة" if loss < 0 else "🟢 رابح"
            lines.append(f"{info['name']}({sym}): {p}{c} | تكلفة {info['cost']}{c} | {loss:.1f}% | {s}")
    return "\n".join(lines)

# ─────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────
def build_system(file_ctx="", search_ctx=""):
    base = """أنت "دماغ المجلس السيادي" — المرجع القطعي لـ "أبو عبدالله" (القاضي السيادي) وفق الميثاق السيادي V10.0.
هويتك: دماغ مجلس من 21 شخصية استثمارية عالمية. لغتك دقيقة ملتزمة بالحوكمة.
الترميز: 🟢 يقين قطعي / 🟡 توقع مدروس / 🔴 بيانات ناقصة

القوانين المقدسة:
١. وقف الخسارة 20% — آلي فوري لا استثناء
٢. فلتر الائتمان 33%
٣. صمام العائلة 270,208 ريال — محظور المساس به
٤. تحريم الروافع — صفر مديونية
٥. أرضية السيولة 20% دائماً
٦. سقف التركيز 15% لأصل واحد
٧. فترة التبريد 48 ساعة
٨. الفلتر الشرعي
٩. الانتظار الذكي 30 يوم بعد الجراحة
١٠. الفصل السيادي — الثروة الشخصية فقط

الجرد (08-03-2026):
الدخل: 103,959 ر/م | الفائض: 58,924 ر (56.7%)
الودائع: 3,735,756 ر | الديون: 2,815,970 ر
تكاليف: كيمانول 19.30 | النهدي 126.24 | باعظيم 7.43 | الحمادي 39.94
المتقدمة 40.85 | أرامكو 28.68 | جبل عمر 23.89 | أسمنت 35.73 | مسار 22.78 | LCID $28.27
العقارات: منزل(2.4M) + أراضٍ(حصة50%) + الجله(بلا صك)
الشركات: BMP 100% · لؤي 37% · SEAT 49% · دريم فالي 12% · انفستكورب(NAV مجهول)

الأعضاء: PwC·بويز·أكمان·طالب·بافيت·داليو·نافال·لي كا شينج·مونجر·رؤية2030
بوري·PTJ·آيكان·بيزوس·سوروس·ثيل·جينسن·تيم كوك·ماركس·تشانوس·بريمر

المعادلة الذهبية: قرار الشراء = قيمة بافيت + توقيت PTJ + فيتو بوري + اختبار طالب
أجب دائماً بالعربية. دقيق. استشهد بالأعضاء والأرقام."""

    pc = prices_ctx_str()
    if pc:      base += f"\n\n{'='*40}\nالأسعار الحية ({st.session_state.last_update}):\n{pc}"
    if file_ctx:   base += f"\n\n{'='*40}\nمحتوى الملف:\n{file_ctx}"
    if search_ctx: base += f"\n\n{'='*40}\nnتائج البحث:\n{search_ctx}"
    return base

# ─────────────────────────────────────────
# AI CALL
# ─────────────────────────────────────────
def call_brain(q, file_ctx="", search_ctx=""):
    key = secret("ANTHROPIC_API_KEY") or st.session_state.get("manual_key","")
    if not key: return "🔴 أدخل API Key."
    try:
        client = anthropic.Anthropic(api_key=key)
        system = build_system(file_ctx if not file_ctx.startswith("__PDF") else "", search_ctx)
        if file_ctx.startswith("__PDF__"):
            pdf_b64 = file_ctx.replace("__PDF__","")
            msgs = [{"role":"user","content":[
                {"type":"document","source":{"type":"base64","media_type":"application/pdf","data":pdf_b64}},
                {"type":"text","text":q}
            ]}]
        else:
            msgs = [{"role":"user","content":q}]
        resp = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1500, system=system, messages=msgs)
        return resp.content[0].text
    except anthropic.AuthenticationError: return "🔴 مفتاح خاطئ."
    except anthropic.RateLimitError:      return "🟡 انتظر دقيقة."
    except Exception as e:                return f"🔴 {e}"

def read_file(f):
    n = f.name.lower()
    try:
        if   n.endswith(".pdf"):  return "__PDF__" + base64.b64encode(f.read()).decode()
        elif n.endswith(".csv"):  df = pd.read_csv(f); return f"CSV: {f.name}\n{df.to_string(max_rows=100)}"
        elif n.endswith((".xlsx",".xls")): df = pd.read_excel(f); return f"Excel: {f.name}\n{df.to_string(max_rows=100)}"
        elif n.endswith(".txt"): return f.read().decode("utf-8","ignore")
        else: return f"ملف: {f.name}"
    except Exception as e: return f"خطأ: {e}"

def web_search(q):
    try:
        r = requests.get("https://api.duckduckgo.com/", params={"q":q,"format":"json","no_html":1}, timeout=10)
        d = r.json()
        parts = []
        if d.get("AbstractText"): parts.append(d["AbstractText"])
        for t in d.get("RelatedTopics",[])[:5]:
            if isinstance(t,dict) and t.get("Text"): parts.append(f"• {t['Text'][:200]}")
        return "\n".join(parts) if parts else f"لا توجد نتائج لـ: {q}"
    except Exception as e: return f"خطأ: {e}"

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
_defaults = {
    "page":"📊 لوحة القيادة", "messages":[], "topic":"الميثاق V10.0",
    "manual_key":"", "prices":{}, "last_update":None,
    "uploaded_files":[], "search_results":{}, "alert_filter":None,
    "mem_filter":None, "db_loaded":False,
}
for k,v in _defaults.items():
    if k not in st.session_state: st.session_state[k]=v

# تحميل الرسائل من Supabase عند أول فتح
if not st.session_state.db_loaded and get_supabase():
    loaded = db_load_messages(50)
    if loaded: st.session_state.messages = loaded
    st.session_state.db_loaded = True

def has_key(): return bool(secret("ANTHROPIC_API_KEY") or st.session_state.get("manual_key"))
def has_supabase(): return get_supabase() is not None
def has_email(): return bool(secret("EMAIL_ADDRESS") and secret("EMAIL_PASSWORD"))
def has_telegram(): return bool(secret("TELEGRAM_BOT_TOKEN") and secret("TELEGRAM_CHAT_ID"))

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='padding:0.5rem 0 0.8rem;border-bottom:1px solid rgba(201,168,76,0.2);margin-bottom:0.7rem;text-align:center;'>
    <div style='font-size:1.1rem;font-weight:900;color:#E8C97A;'>⬡ مجلس أبو عبدالله</div>
    <div style='font-size:0.58rem;color:#A8B8CC;'>الميثاق السيادي V10.0 · النسخة المتكاملة</div>
    </div>""",unsafe_allow_html=True)

    # حالة الخدمات
    statuses = [
        ("🔑 API",     has_key()),
        ("🗄️ الذاكرة", has_supabase()),
        ("📧 البريد",  has_email()),
        ("✈️ Telegram", has_telegram()),
        ("📊 الأسعار", bool(st.session_state.prices)),
    ]
    cols_s = st.columns(3)
    for i,(lbl,ok) in enumerate(statuses):
        with cols_s[i%3]:
            clr = "#69db7c" if ok else "#ff8a80"
            st.markdown(f"<div style='font-size:0.6rem;color:{clr};text-align:center;'>{lbl}<br>{'✅' if ok else '❌'}</div>",unsafe_allow_html=True)

    if not has_key():
        st.markdown("<div style='height:4px;'></div>",unsafe_allow_html=True)
        mk = st.text_input("🔑 API Key","",type="password",placeholder="sk-ant-...",label_visibility="collapsed")
        if mk: st.session_state.manual_key=mk; st.rerun()

    st.markdown("<hr>",unsafe_allow_html=True)

    # زر جلب الأسعار
    if st.button("🔄 جلب الأسعار من Google Sheet", use_container_width=True):
        with st.spinner("جاري الجلب..."):
            p,err = fetch_prices()
        if err: st.error(err)
        elif not p: st.error("لم تُجلب أسعار")
        else:
            st.session_state.prices = p
            st.session_state.last_update = datetime.now().strftime("%d/%m %I:%M %p")
            db_save_price_snapshot(p)
            check_and_notify(p)
            st.success(f"✅ {len(p)} سعر — تم الحفظ والتحقق")
            st.rerun()

    # زر PDF
    if st.session_state.prices and PDF_AVAILABLE:
        pdf_buf = generate_pdf(st.session_state.prices)
        if pdf_buf:
            st.download_button(
                "📥 تصدير تقرير PDF",
                data=pdf_buf,
                file_name=f"sovereign_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.markdown("<hr>",unsafe_allow_html=True)

    # الأقسام
    for icon,label in PAGES:
        full = f"{icon} {label}"
        is_a = st.session_state.page == full
        if st.button(f"{'← ' if is_a else ''}{full}", key=f"nav_{full}", use_container_width=True):
            st.session_state.page=full; st.rerun()

    st.markdown("<hr>",unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("🗑️ محادثة",use_container_width=True):
            st.session_state.messages=[]
            db_clear_messages(); st.rerun()
    with c2:
        if st.button("🗑️ ملفات",use_container_width=True):
            st.session_state.uploaded_files=[]; st.rerun()

    st.markdown("""<div style='font-size:0.54rem;color:#A8B8CC;text-align:center;line-height:1.7;margin-top:0.3rem;'>
    📊 Google Sheet · 🗄️ Supabase · 📧 Gmail · ✈️ Telegram · 📥 PDF
    </div>""",unsafe_allow_html=True)

pg = st.session_state.page

# ─────────────────────────────────────────
# PAGE: لوحة القيادة
# ─────────────────────────────────────────
if pg == "📊 لوحة القيادة":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📊 لوحة القيادة — مجلس أبو عبدالله</div>
    <div style='font-size:0.62rem;color:#A8B8CC;margin-top:0.2rem;'>الجرد 08-03-2026 · أسعار Google Sheet · تنبيهات تلقائية</div>
    </div>""",unsafe_allow_html=True)

    # خدمات
    svcs = []
    if has_supabase(): svcs.append("🗄️ ذاكرة دائمة")
    if has_email():    svcs.append("📧 تنبيه بريد")
    if has_telegram(): svcs.append("✈️ Telegram")
    if PDF_AVAILABLE:  svcs.append("📥 تصدير PDF")
    if svcs: st.markdown(f"<div class='sok'>{'  ·  '.join(svcs)}</div><div style='height:8px;'></div>",unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(l,v,clr) in zip([c1,c2,c3,c4,c5],[
        ("💚 الفائض","58,924 ر","#2ECC71"),("🏦 الودائع","3,735,756 ر","#C9A84C"),
        ("💸 الديون","2,815,970 ر","#E74C3C"),("🛡️ الصمام","270,208 ر","#C9A84C"),
        ("📅 الجراحة","22 مارس","#E67E22"),
    ]):
        with col: st.markdown(f"<div class='pc'><div class='pl'>{l}</div><div class='pv' style='color:{clr};font-size:0.9rem;'>{v}</div></div>",unsafe_allow_html=True)

    # الجلسات القادمة
    st.markdown("<div style='height:6px;'></div>",unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.78rem;font-weight:800;color:#E8C97A;margin-bottom:0.5rem;'>📅 الجلسات القادمة</div>",unsafe_allow_html=True)
    sess_cols = st.columns(len(SESSIONS))
    for col, s in zip(sess_cols, SESSIONS):
        with col:
            date_obj = datetime.strptime(s["date"],"%Y-%m-%d")
            days_left = (date_obj - datetime.now()).days
            urgency = "🔴" if days_left <= 1 else "🟠" if days_left <= 5 else "🔵"
            st.markdown(f"""<div style='background:rgba(22,32,64,0.6);border:1px solid {s["color"]}44;border-top:2px solid {s["color"]};
            border-radius:8px;padding:0.6rem;text-align:center;'>
            <div style='font-size:0.6rem;color:{s["color"]};font-weight:700;'>{s["date"]}</div>
            <div style='font-size:0.65rem;font-weight:700;margin:0.2rem 0;'>{s["title"][:30]}</div>
            <div style='font-size:0.55rem;color:#A8B8CC;'>{urgency} {'اليوم' if days_left==0 else f'{days_left} يوم'}</div>
            </div>""",unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)

    if not st.session_state.prices:
        st.markdown("""<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);border-radius:12px;padding:2.5rem;text-align:center;'>
        <div style='font-size:2rem;'>📊</div>
        <div style='font-size:0.88rem;font-weight:700;color:#E8C97A;margin:0.5rem 0;'>اضغط "🔄 جلب الأسعار" في الشريط الجانبي</div>
        <div style='font-size:0.72rem;color:#A8B8CC;'>يجلب الأسعار · يحفظها في Supabase · يرسل تنبيهات إذا تجاوزت 20%</div></div>""",unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:800;color:#E8C97A;margin-bottom:0.7rem;'>📈 المحفظة · {st.session_state.last_update}</div>",unsafe_allow_html=True)
        surgical=[]
        tv=tc=0
        cols=st.columns(5)
        for i,(sym,info) in enumerate(STOCKS_META.items()):
            p=st.session_state.prices.get(sym)
            if not p: continue
            loss=((p-info["cost"])/info["cost"])*100
            val=p*info["shares"]; tv+=val; tc+=info["cost"]*info["shares"]
            if loss<=-20: css="d";icon="🔴";clr="#E74C3C"; surgical.append(f"{info['name']}({loss:.1f}%)")
            elif loss<0:  css="w";icon="🟡";clr="#E67E22"
            else:         css="ok";icon="🟢";clr="#2ECC71"
            c="$" if sym=="LCID" else "ر"
            with cols[i%5]:
                st.markdown(f"""<div class='pc {css}'>
                <div class='pl'>{info['name']} ({sym})</div>
                <div class='pv' style='color:{clr};'>{p:.2f}{c}</div>
                <div class='pg' style='color:{clr};'>{icon} {loss:.1f}%</div>
                <div style='font-size:0.57rem;color:#A8B8CC;'>{val:,.0f} ر</div></div>""",unsafe_allow_html=True)

        lp=((tv-tc)/tc*100) if tc else 0
        st.markdown(f"""<div style='background:rgba(22,32,64,0.6);border:1px solid rgba(201,168,76,0.18);
        border-radius:10px;padding:0.9rem 1.4rem;margin-top:0.7rem;
        display:flex;align-items:center;justify-content:space-around;flex-wrap:wrap;gap:1rem;direction:rtl;'>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>القيمة السوقية</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#C9A84C;'>{tv:,.0f} ر</span></div>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>إجمالي الخسارة</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#E74C3C;'>{lp:.1f}% ({tv-tc:,.0f} ر)</span></div>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>جراحية</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#E74C3C;'>{len(surgical)} أسهم</span></div>
        </div>""",unsafe_allow_html=True)

        if surgical:
            st.markdown(f"<div class='alert-r'>🔴 <strong>جراحية:</strong> {' · '.join(surgical)}</div>",unsafe_allow_html=True)

        if st.button("🧠 تحليل جراحي فوري",use_container_width=True):
            q="حلّل المحفظة بالأسعار الحية وقدّم توصية جراحية لكل سهم تجاوز 20%."
            st.session_state.messages.append({"role":"user","content":q})
            db_save_message("user",q)
            with st.spinner("يفكر..."): ans=call_brain(q)
            st.session_state.messages.append({"role":"assistant","content":ans})
            db_save_message("assistant",ans)
            st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ─────────────────────────────────────────
# PAGE: غرفة المشورة
# ─────────────────────────────────────────
elif pg == "🧠 غرفة المشورة":
    n_files = len(st.session_state.uploaded_files)
    n_srch  = len(st.session_state.search_results)
    ctx_info = []
    if n_files: ctx_info.append(f"<span class='sinfo'>📎 {n_files} ملف</span>")
    if n_srch:  ctx_info.append(f"<span class='sok'>🔍 {n_srch} بحث</span>")
    if st.session_state.prices: ctx_info.append(f"<span class='sok'>📊 أسعار حية</span>")
    if has_supabase(): ctx_info.append(f"<span class='sinfo'>🗄️ ذاكرة دائمة</span>")
    if ctx_info:
        st.markdown(f"<div style='margin-bottom:0.6rem;'>{'  '.join(ctx_info)}</div>",unsafe_allow_html=True)

    st.markdown(f"""<div class='shdr' style='display:flex;align-items:center;gap:1rem;'>
    <div style='font-size:1.5rem;'>🧠</div>
    <div style='flex:1;'>
        <div style='font-size:0.95rem;font-weight:800;color:#E8C97A;'>غرفة المشورة — دماغ المجلس السيادي</div>
        <div style='font-size:0.62rem;color:#A8B8CC;'>مرجع قطعي · سياق أعمق · ذاكرة دائمة</div>
    </div>
    <div style='background:rgba(155,89,182,0.12);border:1px solid rgba(155,89,182,0.28);color:#c39bd3;font-size:0.63rem;font-weight:700;padding:0.18rem 0.65rem;border-radius:100px;'>{st.session_state.topic}</div>
    </div>""",unsafe_allow_html=True)

    topics=["الميثاق V10.0","أعضاء المجلس","الجرد","الأسهم والجراحة","العقارات","الديون","القوانين","القرارات","الشراكات","التنسيق"]
    tc2=st.columns(5)
    for i,t in enumerate(topics):
        with tc2[i%5]:
            if st.button(t,key=f"tp_{t}",use_container_width=True):
                st.session_state.topic=t; st.rerun()

    qqs=["حلّل المحفظة جراحياً","الانتظار الذكي؟","حق النقض؟","مهام بوري كاملة؟","صمام العائلة؟","المعادلة الذهبية؟","بند الفناء؟","ملخص الجرد"]
    st.markdown("<div style='font-size:0.62rem;color:#A8B8CC;margin:0.4rem 0 0.25rem;'>⚡ أسئلة سريعة:</div>",unsafe_allow_html=True)
    qc2=st.columns(4)
    for i,q in enumerate(qqs):
        with qc2[i%4]:
            if st.button(q,key=f"qq_{i}",use_container_width=True):
                if not has_key(): st.error("أدخل API Key")
                else:
                    fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF")])
                    sc="\n\n".join([f"بحث '{k}':\n{v}" for k,v in st.session_state.search_results.items()])
                    st.session_state.messages.append({"role":"user","content":q}); db_save_message("user",q)
                    with st.spinner("يفكر..."): ans=call_brain(q,fc,sc)
                    st.session_state.messages.append({"role":"assistant","content":ans}); db_save_message("assistant",ans)
                    st.rerun()

    st.markdown("<hr style='margin:0.5rem 0;'>",unsafe_allow_html=True)

    if not st.session_state.messages:
        mem_note = " · الذاكرة محفوظة في Supabase" if has_supabase() else ""
        st.markdown(f"""<div class='msg-ai'>مرحباً يا أبا عبدالله — دماغ المجلس السيادي جاهز{mem_note}.<br><br>
        أحمل الميثاق V10.0، الـ21 عضو، الجرد الكامل، القوانين، القرارات المعتمدة، والأسعار الحية.<br>
        الذاكرة محفوظة بين الجلسات — محادثاتنا لا تضيع. 🟢</div>""",unsafe_allow_html=True)
    else:
        for m in st.session_state.messages[-30:]:
            css="msg-user" if m["role"]=="user" else "msg-ai"
            st.markdown(f"<div class='{css}'>{m['content'].replace(chr(10),'<br>')}</div>",unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.4rem 0;'>",unsafe_allow_html=True)
    with st.form("cf",clear_on_submit=True):
        ci,cb=st.columns([5,1])
        with ci: uq=st.text_area("","",placeholder="اسأل دماغ المجلس...",label_visibility="collapsed",height=65)
        with cb:
            st.markdown("<div style='height:14px;'></div>",unsafe_allow_html=True)
            s=st.form_submit_button("↗",use_container_width=True)
        if s and uq.strip():
            if not has_key(): st.error("أدخل API Key")
            else:
                fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF")])
                pdf_ctx=next((f["content"] for f in st.session_state.uploaded_files if f["content"].startswith("__PDF")),"")
                sc="\n\n".join([f"بحث '{k}':\n{v}" for k,v in st.session_state.search_results.items()])
                final_fc = pdf_ctx if pdf_ctx else fc
                st.session_state.messages.append({"role":"user","content":uq.strip()}); db_save_message("user",uq.strip())
                with st.spinner("يفكر..."): ans=call_brain(uq.strip(),final_fc,sc)
                st.session_state.messages.append({"role":"assistant","content":ans}); db_save_message("assistant",ans)
                st.rerun()

# ─────────────────────────────────────────
# PAGE: الجلسات
# ─────────────────────────────────────────
elif pg == "📅 الجلسات":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📅 الجلسات — أجندة المجلس السيادي</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>مزامنة من Google Calendar · محدّثة تلقائياً</div>
    </div>""",unsafe_allow_html=True)

    today = datetime.now().date()
    for s in SESSIONS:
        d = datetime.strptime(s["date"],"%Y-%m-%d").date()
        diff = (d - today).days
        if   diff < 0:  status="✅ انتهت";   badge_clr="#2ECC71"
        elif diff == 0: status="🔴 اليوم!";   badge_clr="#E74C3C"
        elif diff <= 3: status=f"🟠 بعد {diff} أيام"; badge_clr="#E67E22"
        else:           status=f"🔵 بعد {diff} يوم"; badge_clr="#3498DB"

        st.markdown(f"""<div class='cal-item' style='border-right:3px solid {s["color"]};'>
        <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;'>
        <div>
            <div style='font-size:0.82rem;font-weight:800;'>{s["title"]}</div>
            <div style='font-size:0.65rem;color:#A8B8CC;margin-top:0.2rem;'>📅 {s["date"]} · 👥 {s["who"]}</div>
        </div>
        <div style='background:{badge_clr}22;color:{badge_clr};border:1px solid {badge_clr}55;
        padding:0.18rem 0.65rem;border-radius:100px;font-size:0.7rem;font-weight:700;white-space:nowrap;'>{status}</div>
        </div></div>""",unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown("""<div style='background:rgba(52,152,219,0.06);border:1px solid rgba(52,152,219,0.2);border-radius:8px;
    padding:0.8rem 1rem;font-size:0.72rem;color:#74c0fc;direction:rtl;'>
    💡 لمزامنة التقويم تلقائياً: في Google Calendar ← إعدادات التقويم ← نسخ الرابط السري (ICS) ← أضفه في Streamlit Secrets بمفتاح CALENDAR_ICS_URL
    </div>""",unsafe_allow_html=True)

# ─────────────────────────────────────────
# PAGE: رفع الملفات
# ─────────────────────────────────────────
elif pg == "📎 رفع الملفات":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📎 رفع وتحليل الملفات</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>PDF · Excel · CSV · TXT — يُحلَّل بسياق الميثاق والجرد</div>
    </div>""",unsafe_allow_html=True)

    uploaded = st.file_uploader("ارفع ملفاً",type=["pdf","xlsx","xls","csv","txt"],label_visibility="collapsed")
    if uploaded:
        with st.spinner(f"قراءة {uploaded.name}..."):
            content = read_file(uploaded)
        existing = [f["name"] for f in st.session_state.uploaded_files]
        if uploaded.name not in existing:
            st.session_state.uploaded_files.append({"name":uploaded.name,"content":content,"time":datetime.now().strftime("%I:%M %p")})
            st.success(f"✅ {uploaded.name}"); st.rerun()
        else: st.info("الملف محمّل مسبقاً")

    if st.session_state.uploaded_files:
        st.markdown("<div style='font-size:0.78rem;font-weight:800;color:#E8C97A;margin:0.8rem 0 0.5rem;'>الملفات المحمّلة</div>",unsafe_allow_html=True)
        for i,f in enumerate(st.session_state.uploaded_files):
            c1,c2,c3=st.columns([4,2,1])
            with c1: st.markdown(f"<div style='font-size:0.8rem;padding:0.5rem 0;'>{'📄' if f['content'].startswith('__PDF') else '📊'} {f['name']}</div>",unsafe_allow_html=True)
            with c2: st.markdown(f"<div style='font-size:0.67rem;color:#A8B8CC;padding:0.5rem 0;'>{f['time']}</div>",unsafe_allow_html=True)
            with c3:
                if st.button("🗑️",key=f"df_{i}"): st.session_state.uploaded_files.pop(i); st.rerun()

        qs=["لخّص أبرز الأرقام في هذا الملف","ابحث عن أي مخاطر مالية","قارن مع جرد المجلس","حلّل وفق الميثاق V10.0"]
        qc3=st.columns(2)
        for i,q in enumerate(qs):
            with qc3[i%2]:
                if st.button(q,key=f"fa_{i}",use_container_width=True):
                    if not has_key(): st.error("أدخل API Key")
                    else:
                        fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF")])
                        pdf_ctx=next((f["content"] for f in st.session_state.uploaded_files if f["content"].startswith("__PDF")),"")
                        final=pdf_ctx if pdf_ctx else fc
                        st.session_state.messages.append({"role":"user","content":q}); db_save_message("user",q)
                        with st.spinner("يحلل..."): ans=call_brain(q,final,"")
                        st.session_state.messages.append({"role":"assistant","content":ans}); db_save_message("assistant",ans)
                        st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ─────────────────────────────────────────
# PAGE: بحث الويب
# ─────────────────────────────────────────
elif pg == "🔍 بحث الويب":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>🔍 بحث الويب الحي</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>أخبار الأسهم والاقتصاد — تُضاف لسياق دماغ المجلس</div>
    </div>""",unsafe_allow_html=True)

    quick_s=["أخبار سهم كيمانول اليوم","أخبار جبل عمر للتطوير","تداول TASI اليوم","أخبار أسمنت العربية","أسعار النفط اليوم","اقتصاد السعودية 2026","Lucid Group LCID news","أخبار العقارات السعودية"]
    sc2=st.columns(4)
    for i,q in enumerate(quick_s):
        with sc2[i%4]:
            if st.button(q,key=f"sq_{i}",use_container_width=True):
                with st.spinner(f"يبحث..."): r=web_search(q)
                st.session_state.search_results[q]=r
                st.success(f"✅ {q[:25]}"); st.rerun()

    st.markdown("<hr>",unsafe_allow_html=True)
    with st.form("sf",clear_on_submit=True):
        cs,cb2=st.columns([5,1])
        with cs: cq=st.text_input("","",placeholder="ابحث عن أي خبر...",label_visibility="collapsed")
        with cb2: sb2=st.form_submit_button("🔍",use_container_width=True)
        if sb2 and cq.strip():
            with st.spinner("يبحث..."): r=web_search(cq.strip())
            st.session_state.search_results[cq.strip()]=r; st.rerun()

    for q,result in st.session_state.search_results.items():
        with st.expander(f"🔍 {q}"):
            st.markdown(f"<div style='font-size:0.73rem;color:#A8B8CC;line-height:1.7;direction:rtl;'>{result}</div>",unsafe_allow_html=True)
            c_a,c_d2=st.columns([3,1])
            with c_a:
                if st.button(f"🧠 اسأل دماغ المجلس",key=f"as_{q[:15]}",use_container_width=True):
                    aq=f"بناءً على أخبار '{q}' — ما تأثيرها على محفظتي؟"
                    st.session_state.messages.append({"role":"user","content":aq}); db_save_message("user",aq)
                    with st.spinner("يفكر..."): ans=call_brain(aq,"",f"بحث '{q}':\n{result}")
                    st.session_state.messages.append({"role":"assistant","content":ans}); db_save_message("assistant",ans)
                    st.session_state.page="🧠 غرفة المشورة"; st.rerun()
            with c_d2:
                if st.button("🗑️",key=f"ds_{q[:15]}"): del st.session_state.search_results[q]; st.rerun()

# ─────────────────────────────────────────
# PAGE: الأسعار التاريخية
# ─────────────────────────────────────────
elif pg == "📈 الأسعار التاريخية":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📈 الأسعار التاريخية — المقارنة عبر الزمن</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>كل عملية جلب تُحفظ تلقائياً — تتبّع حركة الأسعار</div>
    </div>""",unsafe_allow_html=True)

    if not has_supabase():
        st.markdown("""<div class='alert-r'>🗄️ الأسعار التاريخية تحتاج Supabase — أضف SUPABASE_URL و SUPABASE_KEY في Secrets</div>""",unsafe_allow_html=True)
    else:
        history = db_load_price_history(10)
        if not history:
            st.markdown("""<div style='text-align:center;padding:2rem;color:#A8B8CC;'>
            لا يوجد تاريخ بعد — اجلب الأسعار وستُحفظ تلقائياً</div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:0.78rem;color:#A8B8CC;margin-bottom:0.7rem;'>آخر {len(history)} عمليات جلب محفوظة</div>",unsafe_allow_html=True)

            # جدول مقارنة
            sym_sel = st.selectbox("اختر سهماً للمقارنة", list(STOCKS_META.keys()),
                                   format_func=lambda x: f"{x} - {STOCKS_META[x]['name']}")
            if sym_sel:
                cost = STOCKS_META[sym_sel]["cost"]
                rows_data = []
                for h in history:
                    p = h["prices"].get(sym_sel)
                    if p:
                        loss = ((p - cost) / cost) * 100
                        t = h["time"][:16].replace("T"," ")
                        rows_data.append({"الوقت":t,"السعر":p,"الخسارة%":round(loss,1)})
                if rows_data:
                    df_hist = pd.DataFrame(rows_data)
                    # رسم بياني
                    st.line_chart(df_hist.set_index("الوقت")["السعر"])
                    # جدول
                    for row in rows_data:
                        clr = "#E74C3C" if row["الخسارة%"] <= -20 else "#E67E22" if row["الخسارة%"] < 0 else "#2ECC71"
                        st.markdown(f"""<div class='hist-row'>
                        <span style='color:#A8B8CC;'>{row["الوقت"]}</span>  ·
                        <span style='color:#C9A84C;font-family:IBM Plex Mono;'>{row["السعر"]:.2f} ر</span>  ·
                        <span style='color:{clr};'>{row["الخسارة%"]:.1f}%</span></div>""",unsafe_allow_html=True)

# ─────────────────────────────────────────
# الأقسام الأخرى (مختصرة مع إعادة توجيه للمشورة)
# ─────────────────────────────────────────
elif pg in ["👥 المجلس","📁 التقارير","🎯 القناصون","⚖️ الحوكمة","📜 الذاكرة"]:
    labels = {
        "👥 المجلس":   ("👥 المجلس الاقتصادي الأعلى — 21 عضواً","أضف محتوى المجلس من ملف app_sovereign_full.py"),
        "📁 التقارير": ("📁 أرشيف التقارير السيادية","أضف التقارير من ملف app_sovereign_full.py"),
        "🎯 القناصون": ("🎯 قاعة القناصين","أضف التنبيهات من ملف app_sovereign_full.py"),
        "⚖️ الحوكمة":  ("⚖️ الحوكمة والقوانين المقدسة","أضف القوانين من ملف app_sovereign_full.py"),
        "📜 الذاكرة":  ("📜 الذاكرة السيادية","أضف سجل القرارات من ملف app_sovereign_full.py"),
    }
    title, hint = labels.get(pg, (pg,""))
    st.markdown(f"""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>{title}</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>{hint}</div>
    </div>""",unsafe_allow_html=True)

    # للذاكرة: عرض رسائل Supabase
    if pg == "📜 الذاكرة" and has_supabase():
        msgs_db = db_load_messages(20)
        if msgs_db:
            st.markdown(f"<div style='font-size:0.78rem;color:#A8B8CC;margin-bottom:0.5rem;'>آخر {len(msgs_db)} رسالة من Supabase</div>",unsafe_allow_html=True)
            for m in msgs_db[-10:]:
                css="msg-user" if m["role"]=="user" else "msg-ai"
                preview=m["content"][:200]+"..." if len(m["content"])>200 else m["content"]
                st.markdown(f"<div class='{css}' style='font-size:0.75rem;'>{preview}</div>",unsafe_allow_html=True)

    if st.button("🧠 انتقل لغرفة المشورة",use_container_width=True):
        st.session_state.page="🧠 غرفة المشورة"; st.rerun()
