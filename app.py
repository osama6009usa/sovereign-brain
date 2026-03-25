"""
⬡ مركز القيادة السيادي — مجلس أبو عبدالله
النسخة المُصحَّحة الكاملة — إصلاح 7 أخطاء جوهرية
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
    from fpdf.enums import XPos, YPos
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
st.set_page_config(
    page_title="⬡ مجلس أبو عبدالله",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
.alert-b{background:rgba(52,152,219,0.06);border:1px solid rgba(52,152,219,0.25);border-right:3px solid #3498DB;border-radius:8px;padding:0.75rem 1rem;font-size:0.77rem;color:#74c0fc;direction:rtl;margin:0.5rem 0;}
.alert-y{background:rgba(243,156,18,0.06);border:1px solid rgba(243,156,18,0.25);border-right:3px solid #F39C12;border-radius:8px;padding:0.75rem 1rem;font-size:0.77rem;color:#ffd43b;direction:rtl;margin:0.5rem 0;}
.cal-item{background:rgba(22,32,64,0.5);border:1px solid rgba(201,168,76,0.15);border-radius:8px;padding:0.65rem 1rem;margin-bottom:0.4rem;direction:rtl;}
.hist-row{background:rgba(22,32,64,0.5);border:1px solid rgba(201,168,76,0.12);border-radius:8px;padding:0.6rem 0.9rem;margin-bottom:0.35rem;font-size:0.75rem;direction:rtl;}
.member-card{background:rgba(22,32,64,0.6);border:1px solid rgba(201,168,76,0.15);border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.5rem;direction:rtl;}
.law-item{background:rgba(22,32,64,0.5);border-right:3px solid #C9A84C;border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin-bottom:0.4rem;direction:rtl;font-size:0.83rem;}
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

# أعضاء المجلس الـ 21
MEMBERS = [
    # جدار المناعة
    {"num":"01","name":"وكيل PwC السيادي","role":"ضابط النزاهة المالية والامتثال الشرعي","group":"🛡️ جدار المناعة","color":"#9B59B6","tasks":["الفحص الجنائي لمصادر المال","حساب الزكاة والضرائب","نسبة التطهير الشرعية"]},
    {"num":"02","name":"ديفيد بويز","role":"كبير المستشارين القانونيين وصائد الثغرات","group":"🛡️ جدار المناعة","color":"#9B59B6","tasks":["تسوية أراضي الجله — 31 مارس","تفكيك عقود الشراكات","حصانة قانونية 1000%"]},
    {"num":"03","name":"بيل أكمان","role":"محقق النزاهة والتحري عن الشركاء","group":"🛡️ جدار المناعة","color":"#9B59B6","tasks":["فحص تاريخ الشركاء","Due Diligence قبل أي صفقة","فيتو فوري عند أي شائبة"]},
    {"num":"04","name":"ناسم طالب","role":"ضابط مكافحة الهشاشة واختبار البجعة السوداء","group":"🛡️ جدار المناعة","color":"#9B59B6","tasks":["اختبار الخسارة القصوى","حماية الأمان الوجودي","نقض الاستثمارات الهشة"]},
    # هيئة الحكماء
    {"num":"05","name":"وارن بافيت","role":"كبير مهندسي القيمة الجوهرية","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["تقييم القيمة الجوهرية","البحث عن الخندق المنيع","استثمار طويل الأمد"]},
    {"num":"06","name":"راي داليو","role":"مهندس الأنظمة الاقتصادية","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["توازن الأصول بالدورات","إدارة التضخم","All Weather Portfolio"]},
    {"num":"07","name":"نافال رافيكانت","role":"مستشار الروافع والنمو الأسّي","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["تقييم الروافع التقنية","النمو بلا تكاليف بشرية","تبسيط المحفظة الجمالي"]},
    {"num":"08","name":"لي كا شينج","role":"قناص العقار والسيولة العالمي","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["ROT الأراضي الثلاث — 5 أبريل","توقيت دخول/خروج العقارات","تحليل Return on Title"]},
    {"num":"09","name":"تشارلي مونجر","role":"المدعي العام وكاشف الأخطاء المنطقية","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["بروتوكول الانتظار الذكي 30 يوم","النماذج الذهنية المضادة للغباء","مراجعة سجل التوقعات دورياً"]},
    {"num":"10","name":"خبير رؤية 2030","role":"ضابط المواءمة الوطنية","group":"🏛️ هيئة الحكماء","color":"#C9A84C","tasks":["ربط الاستثمار بمشاريع المملكة","رصد التحولات التشريعية","فرص رؤية 2030"]},
    # كتيبة التنفيذ
    {"num":"11","name":"مايكل بوري","role":"المحلل الجنائي — شارح الميزانيات","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["تقرير الفائض الضائع — 29 مارس","ميزانية الحقيقة Truth Balance Sheet","تشريح انفستكورب ولؤي"]},
    {"num":"12","name":"بول تودور جونز","role":"خبير الزخم والتوقيت الفني","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["تقرير ما قبل الجراحة التقني","التقويم التداولي السعودي 2026","بروتوكول الدخول الموزّع 25/50/25"]},
    {"num":"13","name":"كارل آيكان","role":"المستثمر الناشط — صائد الأصول المظلومة","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["معادلات الخروج من الشراكات — 5 أبريل","Dilution Radar","Silent Activist Protocol"]},
    {"num":"14","name":"جيف بيزوس","role":"مهندس الكفاءة التشغيلية","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["تشخيص البنية التشغيلية","Blank Sheet Decision Protocol","خارطة الأتمتة"]},
    {"num":"15","name":"جورج سوروس","role":"خبير الانعكاسية وتتبع الحيتان","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["تتبع سيكولوجية الجماهير","المضاربات الكبرى","حركة الحيتان في السوق السعودي"]},
    {"num":"16","name":"بيتر ثيل","role":"خبير الاحتكار والمزايا التنافسية","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["Zero to One Analysis","المزايا السياسية الفريدة","تقييم فرص ما قبل الاكتتاب"]},
    {"num":"17","name":"جينسن هوانغ","role":"المدقق التقني — AI والرقائق","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["فحص جوهر التكنولوجيا","استدامة القطاع التقني","تقييم SEAT ودريم فالي"]},
    {"num":"18","name":"تيم كوك","role":"مايسترو اللوجستيات والتنفيذ","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["التقرير الشهري الموحد — 1 أبريل","جرد الأكسجين والسيولة","سلاسل الإمداد التنفيذي"]},
    {"num":"19","name":"هوارد ماركس","role":"رادار دورات المخاطرة","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["موقعنا من بندول المخاطرة","تحليل تفاؤل/تشاؤم السوق","توقيت إعادة نشر رأس المال"]},
    {"num":"20","name":"جيمس تشانوس","role":"صياد الاحتيال ومصمم التحوط","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["كشف المبالغات في الأرباح","تصميم خطط Hedging","فخ العدو — تحليل تشانوس"]},
    {"num":"21","name":"إيان بريمر","role":"المحلل الجيوسياسي الدولي","group":"⚔️ كتيبة التنفيذ","color":"#E74C3C","tasks":["أثر الحروب على المحفظة","تحليل السياسات الدولية","مخاطر الاستثمار الجيوسياسي"]},
]

# القوانين المقدسة
LAWS = [
    {"num":"١","title":"وقف الخسارة القطعي 20%","desc":"يُمنع استمرار أي صفقة هبطت 20% — تنفيذ آلي فوري. لا أمل. لا انتظار.","color":"#E74C3C"},
    {"num":"٢","title":"فلتر النقاء الائتماني 33%","desc":"يُحظر الدخول في كيان تتجاوز ديونه 33% من قيمته السوقية. استثناء 40% بموافقة الأربعة فقط.","color":"#E67E22"},
    {"num":"٣","title":"صمام العائلة — 270,208 ريال","desc":"مجمّد في أوعية صفرية المخاطرة. محظور استخدامه ضماناً أو في رأس المال المُدار. المساس به = بند الفناء.","color":"#C9A84C"},
    {"num":"٤","title":"تحريم الروافع — صفر مديونية","desc":"يُمنع الاقتراض للاستثمار أو استخدام الهامش. القوة في ملكية الكاش 100%.","color":"#9B59B6"},
    {"num":"٥","title":"أرضية السيولة 20%","desc":"الحفاظ على 20% من المحفظة كسيولة جاهزة دائماً — السلاح عند انهيار الأسواق.","color":"#3498DB"},
    {"num":"٦","title":"سقف التركيز 15%","desc":"يُمنع تخصيص أكثر من 15% من إجمالي الثروة لأصل واحد. توزيع البيض قانون البقاء.","color":"#2ECC71"},
    {"num":"٧","title":"فترة التبريد 48 ساعة","desc":"الصفقات الاستراتيجية تنتظر 48 ساعة لخمود العاطفة والاندفاع. استثناء القنص بموافقة الأربعة.","color":"#E67E22"},
    {"num":"٨","title":"الفلتر الشرعي","desc":"الأولوية للأصول النقية تماماً. المختلطة تُقبل بشرط حساب نسبة التطهير وخصمها آلياً.","color":"#C9A84C"},
    {"num":"٩","title":"الانتظار الذكي 30 يوماً","desc":"لا إعادة استثمار للسيولة المُحررة من الجراحة قبل 30 يوماً (مونجر). بروتوكول إلزامي.","color":"#9B59B6"},
    {"num":"١٠","title":"الفصل السيادي","desc":"المجلس يتعامل مع الثروة الشخصية حصراً. أي تقاطع مع المسيرة المهنية أو الأكاديمية = رفض فوري.","color":"#E74C3C"},
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
    except: return False

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
    surgical = []
    for sym, info in STOCKS_META.items():
        p = prices.get(sym)
        if not p: continue
        loss = ((p - info["cost"]) / info["cost"]) * 100
        if loss <= -20:
            surgical.append((info["name"], sym, p, loss))
    if not surgical: return

    now_str = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    rows = "".join([
        f"<tr><td style='padding:6px 10px;'>{n} ({s})</td>"
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

    tg_lines = [f"⬡ <b>مجلس أبو عبدالله — تنبيه جراحي</b>\n🔴 {now_str}\n"]
    for n,s,p,l in surgical:
        tg_lines.append(f"🔴 <b>{n}</b> ({s}): {p:.2f} ر | خسارة {l:.1f}%")
    tg_lines.append("\n⚖️ وقف الخسارة 20% — قرار عاجل مطلوب")

    send_email(f"🔴 تنبيه جراحي — {len(surgical)} أسهم تجاوزت 20%", email_html)
    send_telegram("\n".join(tg_lines))

# ─────────────────────────────────────────
# PDF REPORT — إصلاح خلل العربية
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
        pdf.cell(0, 15, "Abu Abdullah Sovereign Council", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "Portfolio Genesis Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(168, 184, 204)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}  |  Sovereign Charter V10.0  |  CONFIDENTIAL",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(4)

        # divider line
        pdf.set_draw_color(201, 168, 76)
        pdf.set_line_width(0.5)
        pdf.line(14, pdf.get_y(), 196, pdf.get_y())
        pdf.ln(5)

        # KPIs
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(201, 168, 76)
        pdf.cell(0, 10, "Portfolio Overview", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(232, 237, 245)
        kpis = [
            ("Monthly Income",     "103,959 SAR"),
            ("Monthly Surplus",    "58,924 SAR (56.7%)"),
            ("Total Deposits",     "3,735,756 SAR"),
            ("Total Debt",         "2,815,970 SAR"),
            ("Family Safety Valve","270,208 SAR"),
            ("Annual Surplus",     "707,088 SAR/year"),
        ]
        for label, val in kpis:
            pdf.set_text_color(168, 184, 204)
            pdf.cell(75, 7, label + ":", border=0)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 7, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)

        # Stocks Table
        if prices:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 10, "Stock Portfolio — Live Prices", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(22, 32, 64)
            pdf.set_text_color(232, 197, 122)
            headers = ["Symbol", "Name (EN)", "Cost", "Current", "Loss %", "Status"]
            widths  = [18, 50, 22, 22, 20, 28]

            # name mapping English
            name_en = {
                "2001":"Chemanol","4164":"Al-Nahdi","4051":"Bawan",
                "4007":"Al-Hammadi","2330":"Advanced","2222":"Aramco",
                "4250":"Jabal Omar","3010":"Arab Cement","4336":"Mulkia REIT",
                "4325":"Massar","LCID":"Lucid Group",
            }

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
                c_sym = "$" if sym == "LCID" else "SAR"
                row = [sym, name_en.get(sym, sym), f"{info['cost']:.2f}", f"{p:.2f} {c_sym}", f"{loss:.1f}%", status]
                for val, w in zip(row, widths):
                    pdf.cell(w, 7, str(val), border=1, align="C")
                pdf.ln()
                pdf.set_text_color(232, 237, 245)
            pdf.ln(4)

        # Portfolio Summary
        if prices:
            tv = sum(prices.get(s,0)*i["shares"] for s,i in STOCKS_META.items() if prices.get(s))
            tc = sum(i["cost"]*i["shares"] for i in STOCKS_META.values())
            lp = ((tv-tc)/tc*100) if tc else 0
            surgical_count = sum(1 for s,i in STOCKS_META.items()
                                  if prices.get(s) and ((prices[s]-i["cost"])/i["cost"]*100) <= -20)

            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(201, 168, 76)
            pdf.cell(0, 9, "Portfolio Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("Helvetica", "", 10)
            summaries = [
                ("Market Value", f"{tv:,.0f} SAR"),
                ("Total Loss",   f"{lp:.1f}%  ({tv-tc:,.0f} SAR)"),
                ("Surgical Stocks", f"{surgical_count} stocks exceed -20% threshold"),
            ]
            for lbl, val in summaries:
                pdf.set_text_color(168, 184, 204)
                pdf.cell(55, 7, lbl + ":", border=0)
                clr = (231,76,60) if lp < -20 else (230,126,34) if lp < 0 else (46,204,113)
                pdf.set_text_color(*clr)
                pdf.cell(0, 7, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)

        # Sessions
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(201, 168, 76)
        pdf.cell(0, 10, "Upcoming Council Sessions", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 9)
        session_en = {
            "2026-03-22": "Surgical Session — Stocks + Crypto",
            "2026-03-29": "Missing Surplus Report + Truth Balance Sheet",
            "2026-03-31": "Real Estate Valuations + Jala Land Settlement",
            "2026-04-01": "Unified Monthly Report",
            "2026-04-05": "Land ROT + Exit Formulas",
        }
        for s in SESSIONS:
            pdf.set_text_color(168, 184, 204)
            pdf.cell(30, 7, s["date"], border=0)
            pdf.set_text_color(232, 237, 245)
            pdf.cell(100, 7, session_en.get(s["date"], s["date"]), border=0)
            pdf.set_text_color(168, 184, 204)
            pdf.cell(0, 7, s["who"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Footer
        pdf.set_y(-18)
        pdf.line(14, pdf.get_y(), 196, pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 110, 130)
        pdf.cell(0, 5,
                 f"CONFIDENTIAL — Abu Abdullah Sovereign Council — Sovereign Charter V10.0 — {datetime.now().strftime('%d/%m/%Y')}",
                 align="C")

        buf = BytesIO()
        pdf_bytes = pdf.output()
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

القوانين المقدسة العشرة:
١. وقف الخسارة 20% — آلي فوري لا استثناء
٢. فلتر الائتمان 33% (استثناء 40% بموافقة الأربعة فقط)
٣. صمام العائلة 270,208 ريال — محظور المساس به مطلقاً
٤. تحريم الروافع — صفر مديونية استثمارية
٥. أرضية السيولة 20% دائماً
٦. سقف التركيز 15% لأصل واحد
٧. فترة التبريد 48 ساعة (استثناء القنص بموافقة الأربعة)
٨. الفلتر الشرعي — نسبة التطهير آلية
٩. الانتظار الذكي 30 يوم بعد الجراحة (مونجر)
١٠. الفصل السيادي — الثروة الشخصية فقط

الجرد الكامل (08-03-2026):
الدخل الشهري: 103,959 ريال (رواتب 90,000 + عوائد ~13,959)
الفائض الشهري: 58,924 ريال (56.7%) | السنوي: 707,088 ريال
الودائع الكلية: 3,735,756 ريال | الديون المتبقية: 2,815,970 ريال
القسط الشهري: 24,249 ريال | المصاريف الكلية: 45,035 ريال

الأسهم — تكاليف الشراء:
كيمانول(2001): 19.30 | النهدي(4164): 126.24 | باعظيم(4051): 7.43
الحمادي(4007): 39.94 | المتقدمة(2330): 40.85 | أرامكو(2222): 28.68
جبل عمر(4250): 23.89 | أسمنت العربية(3010): 35.73
ملكية ريت(4336): 5.00 | مسار(4325): 22.78 | LCID: $28.27

العقارات: منزل(2.4M ر) + 3 أراضٍ بحصة 50% (تكلفة 1,550,100 ر) + أراضي الجله(بعقد بلا صك ⚠️)
الشركات: BMP Law 100%✅ · لؤي هندسية 37%🔴 · SEAT 49%🔵 · دريم فالي 12%🔵 · انفستكورب 1991 وحدة⏳
العملات: TRX 15,645 ($0.33→$0.29) · CHR 13,473 (-92.3% ☠️)

المجلس الـ 21:
جدار المناعة: PwC · بويز · أكمان · طالب
هيئة الحكماء: بافيت · داليو · نافال · لي كا شينج · مونجر · رؤية2030
كتيبة التنفيذ: بوري · PTJ · آيكان · بيزوس · سوروس · ثيل · جينسن · تيم كوك · ماركس · تشانوس · بريمر

المعادلة الذهبية: قرار الشراء = قيمة بافيت + توقيت PTJ + فيتو بوري + اختبار طالب

مهام مُعتمدة قائمة:
- 22 مارس: الجلسة الجراحية (أسهم + كريبتو) — PTJ·بوري·سوروس·تشانوس·مونجر
- 29 مارس: تقرير الفائض الضائع + ميزانية الحقيقة — بوري + PwC
- 31 مارس: تسوية أراضي الجله + تقييمات عقارية — بويز + لي كا شينج
- 1 أبريل: التقرير الشهري الموحد — تيم كوك
- 5 أبريل: ROT الأراضي + معادلات خروج الشراكات — آيكان + لي + بويز

أجب دائماً بالعربية. كن دقيقاً. استشهد بالأعضاء والأرقام والمواد."""

    pc = prices_ctx_str()
    if pc:         base += f"\n\n{'='*40}\nالأسعار الحية ({st.session_state.last_update}):\n{pc}"
    if file_ctx:   base += f"\n\n{'='*40}\nمحتوى الملف:\n{file_ctx}"
    if search_ctx: base += f"\n\n{'='*40}\nنتائج البحث:\n{search_ctx}"
    return base

# ─────────────────────────────────────────
# ✅ إصلاح خلل ١ — AI CALL مع تاريخ المحادثة
# ─────────────────────────────────────────
def call_brain(q, file_ctx="", search_ctx=""):
    key = secret("ANTHROPIC_API_KEY") or st.session_state.get("manual_key","")
    if not key: return "🔴 أدخل API Key."
    try:
        client = anthropic.Anthropic(api_key=key)
        system = build_system(
            file_ctx if not file_ctx.startswith("__PDF__") else "",
            search_ctx
        )

        # ✅ إصلاح: إرسال تاريخ المحادثة الكامل (آخر 12 رسالة)
        history = []
        for m in st.session_state.messages[-12:]:
            history.append({"role": m["role"], "content": m["content"]})

        if file_ctx.startswith("__PDF__"):
            pdf_b64 = file_ctx.replace("__PDF__","")
            new_msg = {"role":"user","content":[
                {"type":"document","source":{"type":"base64","media_type":"application/pdf","data":pdf_b64}},
                {"type":"text","text":q}
            ]}
        else:
            new_msg = {"role":"user","content":q}

        msgs = history + [new_msg]

        # ✅ إصلاح خلل ٢ — الموديل المحدّث + max_tokens مرتفع
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2500,
            system=system,
            messages=msgs
        )
        return resp.content[0].text
    except anthropic.AuthenticationError: return "🔴 مفتاح API خاطئ — تحقق من st.secrets."
    except anthropic.RateLimitError:      return "🟡 تجاوزت الحد — انتظر دقيقة ثم أعد المحاولة."
    except Exception as e:                return f"🔴 خطأ: {str(e)}"

# ─────────────────────────────────────────
# FILE READER
# ─────────────────────────────────────────
def read_file(f):
    n = f.name.lower()
    try:
        if   n.endswith(".pdf"):
            return "__PDF__" + base64.b64encode(f.read()).decode()
        elif n.endswith(".csv"):
            df = pd.read_csv(f)
            return f"CSV: {f.name}\n{df.to_string(max_rows=100)}"
        elif n.endswith((".xlsx",".xls")):
            df = pd.read_excel(f)
            return f"Excel: {f.name}\n{df.to_string(max_rows=100)}"
        elif n.endswith(".txt"):
            return f.read().decode("utf-8","ignore")
        else:
            return f"ملف: {f.name}"
    except Exception as e:
        return f"خطأ في قراءة الملف: {e}"

# ─────────────────────────────────────────
# ✅ إصلاح خلل ٤ — بحث الويب بـ DuckDuckGo HTML (أكثر موثوقية)
# ─────────────────────────────────────────
def web_search(q):
    # محاولة أولى: DuckDuckGo HTML scraping
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SovereignCouncil/1.0)"}
        r = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": q, "kl": "ar-ar"},
            headers=headers,
            timeout=12
        )
        if r.status_code == 200 and len(r.text) > 500:
            # استخراج النتائج من HTML بدون BeautifulSoup
            import re
            # نظّف HTML
            text = re.sub(r'<[^>]+>', ' ', r.text)
            text = re.sub(r'\s+', ' ', text).strip()
            # خذ جزءاً مناسباً
            if len(text) > 100:
                return text[500:2500] if len(text) > 2500 else text
    except: pass

    # محاولة ثانية: DuckDuckGo Instant Answer JSON
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": q, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10
        )
        d = r.json()
        parts = []
        if d.get("AbstractText"):
            parts.append(d["AbstractText"])
        for t in d.get("RelatedTopics", [])[:6]:
            if isinstance(t, dict) and t.get("Text"):
                parts.append(f"• {t['Text'][:200]}")
        if parts:
            return "\n".join(parts)
    except: pass

    # محاولة ثالثة: Wikipedia API للأسهم والشركات
    try:
        r = requests.get(
            "https://ar.wikipedia.org/w/api.php",
            params={"action":"query","list":"search","srsearch":q,"format":"json","srlimit":3},
            timeout=8
        )
        data = r.json()
        results = data.get("query",{}).get("search",[])
        if results:
            parts = [f"• {res['snippet'].replace('<span class=\"searchmatch\">','').replace('</span>','')}"
                     for res in results[:3]]
            return f"نتائج ويكيبيديا لـ '{q}':\n" + "\n".join(parts)
    except: pass

    return f"⚠️ لم تُعثر على نتائج حالية لـ: {q}\nنصيحة: جرّب البحث في Google Finance أو تداول مباشرة."

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
_defaults = {
    "page":"📊 لوحة القيادة", "messages":[], "topic":"الميثاق V10.0",
    "manual_key":"", "prices":{}, "last_update":None,
    "uploaded_files":[], "search_results":{},
    "db_loaded":False,
}
for k,v in _defaults.items():
    if k not in st.session_state: st.session_state[k]=v

# تحميل الرسائل من Supabase عند أول فتح
if not st.session_state.db_loaded and get_supabase():
    loaded = db_load_messages(50)
    if loaded: st.session_state.messages = loaded
    st.session_state.db_loaded = True

def has_key():      return bool(secret("ANTHROPIC_API_KEY") or st.session_state.get("manual_key"))
def has_supabase(): return get_supabase() is not None
def has_email():    return bool(secret("EMAIL_ADDRESS") and secret("EMAIL_PASSWORD"))
def has_telegram(): return bool(secret("TELEGRAM_BOT_TOKEN") and secret("TELEGRAM_CHAT_ID"))

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='padding:0.5rem 0 0.8rem;border-bottom:1px solid rgba(201,168,76,0.2);margin-bottom:0.7rem;text-align:center;'>
    <div style='font-size:1.1rem;font-weight:900;color:#E8C97A;'>⬡ مجلس أبو عبدالله</div>
    <div style='font-size:0.58rem;color:#A8B8CC;'>الميثاق السيادي V10.0 · النسخة المتكاملة</div>
    </div>""", unsafe_allow_html=True)

    # ✅ إصلاح خلل ٥ — 5 أعمدة لـ 5 مؤشرات
    statuses = [
        ("🔑 API",      has_key()),
        ("🗄️ ذاكرة",   has_supabase()),
        ("📧 بريد",    has_email()),
        ("✈️ TG",       has_telegram()),
        ("📊 أسعار",   bool(st.session_state.prices)),
    ]
    cols_s = st.columns(5)
    for i, (lbl, ok) in enumerate(statuses):
        with cols_s[i]:
            clr = "#69db7c" if ok else "#ff8a80"
            ic  = "✅" if ok else "❌"
            st.markdown(
                f"<div style='font-size:0.52rem;color:{clr};text-align:center;line-height:1.4;'>{lbl}<br>{ic}</div>",
                unsafe_allow_html=True
            )

    if not has_key():
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        mk = st.text_input("🔑 API Key","",type="password",placeholder="sk-ant-...",label_visibility="collapsed")
        if mk: st.session_state.manual_key=mk; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # زر جلب الأسعار
    if st.button("🔄 جلب الأسعار من Google Sheet", use_container_width=True):
        with st.spinner("جاري الجلب..."):
            p, err = fetch_prices()
        if err:
            st.error(f"خطأ: {err}")
        elif not p:
            st.error("لم تُجلب أسعار — تحقق من Google Sheet")
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

    st.markdown("<hr>", unsafe_allow_html=True)

    # الأقسام
    for icon, label in PAGES:
        full = f"{icon} {label}"
        is_a = st.session_state.page == full
        if st.button(f"{'← ' if is_a else ''}{full}", key=f"nav_{full}", use_container_width=True):
            st.session_state.page = full; st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ محادثة", use_container_width=True):
            st.session_state.messages = []
            db_clear_messages(); st.rerun()
    with c2:
        if st.button("🗑️ ملفات", use_container_width=True):
            st.session_state.uploaded_files = []; st.rerun()

    st.markdown("""<div style='font-size:0.54rem;color:#A8B8CC;text-align:center;line-height:1.7;margin-top:0.3rem;'>
    📊 Google Sheet · 🗄️ Supabase · 📧 Gmail · ✈️ Telegram · 📥 PDF
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
pg = st.session_state.page

# ══════════════════════════════════════════
# PAGE: لوحة القيادة
# ══════════════════════════════════════════
if pg == "📊 لوحة القيادة":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📊 لوحة القيادة — مجلس أبو عبدالله</div>
    <div style='font-size:0.62rem;color:#A8B8CC;margin-top:0.2rem;'>الجرد 08-03-2026 · أسعار Google Sheet · تنبيهات تلقائية</div>
    </div>""", unsafe_allow_html=True)

    svcs = []
    if has_supabase(): svcs.append("🗄️ ذاكرة دائمة")
    if has_email():    svcs.append("📧 تنبيه بريد")
    if has_telegram(): svcs.append("✈️ Telegram")
    if PDF_AVAILABLE:  svcs.append("📥 تصدير PDF")
    if svcs:
        st.markdown(f"<div class='sok'>{'  ·  '.join(svcs)}</div><div style='height:8px;'></div>", unsafe_allow_html=True)

    # KPI Cards
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(l,v,clr) in zip([c1,c2,c3,c4,c5],[
        ("💚 الفائض الشهري","58,924 ر","#2ECC71"),
        ("🏦 الودائع","3,735,756 ر","#C9A84C"),
        ("💸 الديون","2,815,970 ر","#E74C3C"),
        ("🛡️ الصمام","270,208 ر","#C9A84C"),
        ("📅 الجلسة القادمة","29 مارس","#E67E22"),
    ]):
        with col:
            st.markdown(f"<div class='pc'><div class='pl'>{l}</div><div class='pv' style='color:{clr};font-size:0.9rem;'>{v}</div></div>",
                        unsafe_allow_html=True)

    # الجلسات
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.78rem;font-weight:800;color:#E8C97A;margin-bottom:0.5rem;'>📅 الجلسات القادمة</div>",
                unsafe_allow_html=True)
    sess_cols = st.columns(len(SESSIONS))
    for col, s in zip(sess_cols, SESSIONS):
        with col:
            date_obj  = datetime.strptime(s["date"],"%Y-%m-%d")
            days_left = (date_obj - datetime.now()).days
            urgency   = "🔴" if days_left <= 1 else "🟠" if days_left <= 5 else "🔵"
            days_txt  = "اليوم!" if days_left == 0 else f"بعد {days_left} يوم" if days_left > 0 else "انتهت"
            st.markdown(f"""<div style='background:rgba(22,32,64,0.6);border:1px solid {s["color"]}44;
            border-top:2px solid {s["color"]};border-radius:8px;padding:0.6rem;text-align:center;'>
            <div style='font-size:0.6rem;color:{s["color"]};font-weight:700;'>{s["date"]}</div>
            <div style='font-size:0.62rem;font-weight:700;margin:0.2rem 0;'>{s["title"][:28]}...</div>
            <div style='font-size:0.55rem;color:#A8B8CC;'>{urgency} {days_txt}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # الأسهم
    if not st.session_state.prices:
        st.markdown("""<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);
        border-radius:12px;padding:2.5rem;text-align:center;'>
        <div style='font-size:2rem;'>📊</div>
        <div style='font-size:0.88rem;font-weight:700;color:#E8C97A;margin:0.5rem 0;'>اضغط "🔄 جلب الأسعار" في الشريط الجانبي</div>
        <div style='font-size:0.72rem;color:#A8B8CC;'>يجلب الأسعار · يحفظها في Supabase · يرسل تنبيهات إذا تجاوزت 20%</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size:0.75rem;font-weight:800;color:#E8C97A;margin-bottom:0.7rem;'>📈 المحفظة · {st.session_state.last_update}</div>",
                    unsafe_allow_html=True)
        surgical=[]
        tv=tc=0
        cols=st.columns(5)
        for i,(sym,info) in enumerate(STOCKS_META.items()):
            p = st.session_state.prices.get(sym)
            if not p: continue
            loss = ((p-info["cost"])/info["cost"])*100
            val  = p*info["shares"]; tv+=val; tc+=info["cost"]*info["shares"]
            if   loss<=-20: css="d"; icon="🔴"; clr="#E74C3C"; surgical.append(f"{info['name']}({loss:.1f}%)")
            elif loss<0:    css="w"; icon="🟡"; clr="#E67E22"
            else:           css="ok";icon="🟢"; clr="#2ECC71"
            c="$" if sym=="LCID" else "ر"
            with cols[i%5]:
                st.markdown(f"""<div class='pc {css}'>
                <div class='pl'>{info['name']} ({sym})</div>
                <div class='pv' style='color:{clr};'>{p:.2f}{c}</div>
                <div class='pg' style='color:{clr};'>{icon} {loss:.1f}%</div>
                <div style='font-size:0.57rem;color:#A8B8CC;'>{val:,.0f} ر</div>
                </div>""", unsafe_allow_html=True)

        lp = ((tv-tc)/tc*100) if tc else 0
        st.markdown(f"""<div style='background:rgba(22,32,64,0.6);border:1px solid rgba(201,168,76,0.18);
        border-radius:10px;padding:0.9rem 1.4rem;margin-top:0.7rem;
        display:flex;align-items:center;justify-content:space-around;flex-wrap:wrap;gap:1rem;direction:rtl;'>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>القيمة السوقية</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#C9A84C;'>{tv:,.0f} ر</span></div>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>إجمالي الخسارة</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#E74C3C;'>{lp:.1f}% ({tv-tc:,.0f} ر)</span></div>
        <div><span style='font-size:0.63rem;color:#A8B8CC;'>جراحية</span><br>
        <span style='font-family:IBM Plex Mono;font-size:1.2rem;font-weight:700;color:#E74C3C;'>{len(surgical)} أسهم</span></div>
        </div>""", unsafe_allow_html=True)

        if surgical:
            st.markdown(f"<div class='alert-r'>🔴 <strong>جراحية:</strong> {' · '.join(surgical)}</div>",
                        unsafe_allow_html=True)

        if st.button("🧠 تحليل جراحي فوري بالأسعار الحالية", use_container_width=True):
            q = "حلّل المحفظة بالأسعار الحية وقدّم توصية جراحية مفصلة لكل سهم تجاوز حد الـ20%، مع ذكر المادة المنتهكة من الميثاق وتوصية واضحة من أعضاء المجلس المختصين."
            st.session_state.messages.append({"role":"user","content":q})
            db_save_message("user", q)
            with st.spinner("يفكر..."): ans = call_brain(q)
            st.session_state.messages.append({"role":"assistant","content":ans})
            db_save_message("assistant", ans)
            st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# PAGE: غرفة المشورة
# ══════════════════════════════════════════
elif pg == "🧠 غرفة المشورة":
    n_files = len(st.session_state.uploaded_files)
    n_srch  = len(st.session_state.search_results)
    ctx_info = []
    if n_files:                    ctx_info.append(f"<span class='sinfo'>📎 {n_files} ملف</span>")
    if n_srch:                     ctx_info.append(f"<span class='sok'>🔍 {n_srch} بحث</span>")
    if st.session_state.prices:    ctx_info.append(f"<span class='sok'>📊 أسعار حية</span>")
    if has_supabase():             ctx_info.append(f"<span class='sinfo'>🗄️ ذاكرة دائمة</span>")
    if ctx_info:
        st.markdown(f"<div style='margin-bottom:0.6rem;'>{'  '.join(ctx_info)}</div>", unsafe_allow_html=True)

    st.markdown(f"""<div class='shdr' style='display:flex;align-items:center;gap:1rem;'>
    <div style='font-size:1.5rem;'>🧠</div>
    <div style='flex:1;'>
        <div style='font-size:0.95rem;font-weight:800;color:#E8C97A;'>غرفة المشورة — دماغ المجلس السيادي</div>
        <div style='font-size:0.62rem;color:#A8B8CC;'>ذاكرة كاملة · سياق أعمق · 21 عضواً</div>
    </div>
    <div style='background:rgba(155,89,182,0.12);border:1px solid rgba(155,89,182,0.28);color:#c39bd3;
    font-size:0.63rem;font-weight:700;padding:0.18rem 0.65rem;border-radius:100px;'>{st.session_state.topic}</div>
    </div>""", unsafe_allow_html=True)

    # مواضيع
    topics=["الميثاق V10.0","أعضاء المجلس","الجرد","الأسهم والجراحة","العقارات","الديون","القوانين","القرارات","الشراكات","التنسيق"]
    tc2=st.columns(5)
    for i,t in enumerate(topics):
        with tc2[i%5]:
            if st.button(t, key=f"tp_{t}", use_container_width=True):
                st.session_state.topic=t; st.rerun()

    # أسئلة سريعة
    qqs=[
        "حلّل المحفظة جراحياً","الانتظار الذكي 30 يوم؟",
        "من يملك حق النقض؟","مهام بوري الثلاث؟",
        "صمام العائلة وقيمته؟","المعادلة الذهبية للشراء؟",
        "بند الفناء متى يُفعَّل؟","ملخص الجرد الكامل"
    ]
    st.markdown("<div style='font-size:0.62rem;color:#A8B8CC;margin:0.4rem 0 0.25rem;'>⚡ أسئلة سريعة:</div>",
                unsafe_allow_html=True)
    qc2=st.columns(4)
    for i,q in enumerate(qqs):
        with qc2[i%4]:
            if st.button(q, key=f"qq_{i}", use_container_width=True):
                if not has_key(): st.error("أدخل API Key أولاً")
                else:
                    fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF__")])
                    sc="\n\n".join([f"بحث '{k}':\n{v}" for k,v in st.session_state.search_results.items()])
                    st.session_state.messages.append({"role":"user","content":q})
                    db_save_message("user",q)
                    with st.spinner("يفكر..."): ans=call_brain(q,fc,sc)
                    st.session_state.messages.append({"role":"assistant","content":ans})
                    db_save_message("assistant",ans)
                    st.rerun()

    st.markdown("<hr style='margin:0.5rem 0;'>", unsafe_allow_html=True)

    # عرض المحادثة
    if not st.session_state.messages:
        mem_note = " · الذاكرة محفوظة في Supabase" if has_supabase() else ""
        st.markdown(f"""<div class='msg-ai'>مرحباً يا أبا عبدالله — دماغ المجلس السيادي جاهز{mem_note}.<br><br>
        أحمل الميثاق V10.0 كاملاً، الـ21 عضو، الجرد المفصّل (08-03-2026)، القوانين، القرارات المعتمدة، والأسعار الحية.<br>
        الذاكرة محفوظة بين الجلسات — محادثاتنا لا تضيع. 🟢</div>""", unsafe_allow_html=True)
    else:
        for m in st.session_state.messages[-30:]:
            css="msg-user" if m["role"]=="user" else "msg-ai"
            st.markdown(f"<div class='{css}'>{m['content'].replace(chr(10),'<br>')}</div>",
                        unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.4rem 0;'>", unsafe_allow_html=True)

    # نموذج الإرسال
    with st.form("cf", clear_on_submit=True):
        ci,cb=st.columns([5,1])
        with ci:
            uq=st.text_area("","",placeholder="اسأل دماغ المجلس...",label_visibility="collapsed",height=65)
        with cb:
            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
            s=st.form_submit_button("↗", use_container_width=True)
        if s and uq.strip():
            if not has_key(): st.error("أدخل API Key")
            else:
                fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF__")])
                pdf_ctx=next((f["content"] for f in st.session_state.uploaded_files if f["content"].startswith("__PDF__")),"")
                sc="\n\n".join([f"بحث '{k}':\n{v}" for k,v in st.session_state.search_results.items()])
                final_fc = pdf_ctx if pdf_ctx else fc
                st.session_state.messages.append({"role":"user","content":uq.strip()})
                db_save_message("user",uq.strip())
                with st.spinner("يفكر..."): ans=call_brain(uq.strip(),final_fc,sc)
                st.session_state.messages.append({"role":"assistant","content":ans})
                db_save_message("assistant",ans)
                st.rerun()

# ══════════════════════════════════════════
# PAGE: الجلسات
# ══════════════════════════════════════════
elif pg == "📅 الجلسات":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📅 الجلسات — أجندة المجلس السيادي</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>خمس جلسات استراتيجية · مارس–أبريل 2026</div>
    </div>""", unsafe_allow_html=True)

    today = datetime.now().date()
    for s in SESSIONS:
        d    = datetime.strptime(s["date"],"%Y-%m-%d").date()
        diff = (d - today).days
        if   diff < 0:  status="✅ انتهت";            badge_clr="#2ECC71"
        elif diff == 0: status="🔴 اليوم!";            badge_clr="#E74C3C"
        elif diff <= 3: status=f"🟠 بعد {diff} أيام"; badge_clr="#E67E22"
        else:           status=f"🔵 بعد {diff} يوم";  badge_clr="#3498DB"

        st.markdown(f"""<div class='cal-item' style='border-right:3px solid {s["color"]};'>
        <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;'>
        <div>
            <div style='font-size:0.85rem;font-weight:800;'>{s["title"]}</div>
            <div style='font-size:0.65rem;color:#A8B8CC;margin-top:0.25rem;'>
                📅 {s["date"]} &nbsp;·&nbsp; 👥 {s["who"]}
            </div>
        </div>
        <div style='background:{badge_clr}22;color:{badge_clr};border:1px solid {badge_clr}55;
        padding:0.18rem 0.7rem;border-radius:100px;font-size:0.7rem;font-weight:700;white-space:nowrap;'>{status}</div>
        </div></div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""<div class='alert-b'>
    💡 لمزامنة Google Calendar تلقائياً: افتح Google Calendar ← إعدادات ← نسخ الرابط السري (ICS) ← أضفه في Streamlit Secrets بمفتاح CALENDAR_ICS_URL
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# PAGE: رفع الملفات
# ══════════════════════════════════════════
elif pg == "📎 رفع الملفات":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📎 رفع وتحليل الملفات</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>PDF · Excel · CSV · TXT — يُحلَّل بسياق الميثاق والجرد</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class='alert-b'>
    💡 الأنواع المدعومة: PDF (قراءة بصرية) · Excel/CSV (تحليل جدولي) · TXT (نص حر)
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("ارفع ملفاً", type=["pdf","xlsx","xls","csv","txt"], label_visibility="collapsed")
    if uploaded:
        with st.spinner(f"قراءة {uploaded.name}..."):
            content = read_file(uploaded)
        existing = [f["name"] for f in st.session_state.uploaded_files]
        if uploaded.name not in existing:
            st.session_state.uploaded_files.append({
                "name":uploaded.name, "content":content,
                "time":datetime.now().strftime("%I:%M %p")
            })
            st.success(f"✅ تم رفع: {uploaded.name}")
            st.rerun()
        else:
            st.info("ℹ️ الملف محمّل مسبقاً")

    if st.session_state.uploaded_files:
        st.markdown("<div style='font-size:0.78rem;font-weight:800;color:#E8C97A;margin:0.8rem 0 0.5rem;'>الملفات المحمّلة</div>",
                    unsafe_allow_html=True)
        for i,f in enumerate(st.session_state.uploaded_files):
            c1,c2,c3=st.columns([4,2,1])
            with c1:
                ic = "📄" if f["content"].startswith("__PDF__") else "📊"
                st.markdown(f"<div style='font-size:0.8rem;padding:0.5rem 0;'>{ic} {f['name']}</div>",
                            unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='font-size:0.67rem;color:#A8B8CC;padding:0.5rem 0;'>{f['time']}</div>",
                            unsafe_allow_html=True)
            with c3:
                if st.button("🗑️", key=f"df_{i}"):
                    st.session_state.uploaded_files.pop(i); st.rerun()

        qs=["لخّص أبرز الأرقام في هذا الملف","ابحث عن أي مخاطر مالية","قارن مع جرد المجلس","حلّل وفق الميثاق V10.0"]
        qc3=st.columns(2)
        for i,q in enumerate(qs):
            with qc3[i%2]:
                if st.button(q, key=f"fa_{i}", use_container_width=True):
                    if not has_key(): st.error("أدخل API Key")
                    else:
                        fc="\n\n".join([f["content"] for f in st.session_state.uploaded_files if not f["content"].startswith("__PDF__")])
                        pdf_ctx=next((f["content"] for f in st.session_state.uploaded_files if f["content"].startswith("__PDF__")),"")
                        final=pdf_ctx if pdf_ctx else fc
                        st.session_state.messages.append({"role":"user","content":q})
                        db_save_message("user",q)
                        with st.spinner("يحلل..."): ans=call_brain(q,final,"")
                        st.session_state.messages.append({"role":"assistant","content":ans})
                        db_save_message("assistant",ans)
                        st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# PAGE: بحث الويب
# ══════════════════════════════════════════
elif pg == "🔍 بحث الويب":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>🔍 بحث الويب الحي</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>أخبار الأسهم والاقتصاد — تُضاف لسياق دماغ المجلس</div>
    </div>""", unsafe_allow_html=True)

    quick_s=[
        "أخبار سهم كيمانول 2001","أخبار جبل عمر للتطوير 4250",
        "تداول TASI اليوم","أخبار أسمنت العربية 3010",
        "أسعار النفط اليوم","اقتصاد السعودية 2026",
        "Lucid Group LCID news","أخبار العقارات السعودية"
    ]
    sc2=st.columns(4)
    for i,q in enumerate(quick_s):
        with sc2[i%4]:
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                with st.spinner(f"يبحث عن: {q[:20]}..."):
                    r = web_search(q)
                st.session_state.search_results[q]=r
                st.success(f"✅ {q[:25]}")
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    with st.form("sf", clear_on_submit=True):
        cs,cb2=st.columns([5,1])
        with cs:
            cq=st.text_input("","",placeholder="ابحث عن أي خبر أو سهم...",label_visibility="collapsed")
        with cb2:
            sb2=st.form_submit_button("🔍", use_container_width=True)
        if sb2 and cq.strip():
            with st.spinner("يبحث..."): r=web_search(cq.strip())
            st.session_state.search_results[cq.strip()]=r; st.rerun()
        elif sb2 and not cq.strip():
            st.warning("اكتب كلمة بحث أولاً")

    for q,result in st.session_state.search_results.items():
        with st.expander(f"🔍 {q}"):
            st.markdown(f"<div style='font-size:0.73rem;color:#A8B8CC;line-height:1.7;direction:rtl;'>{result}</div>",
                        unsafe_allow_html=True)
            c_a,c_d2=st.columns([3,1])
            with c_a:
                if st.button(f"🧠 اسأل دماغ المجلس", key=f"as_{q[:15]}", use_container_width=True):
                    aq=f"بناءً على نتائج البحث عن '{q}' — ما تأثيرها على محفظتي وفق الميثاق؟"
                    st.session_state.messages.append({"role":"user","content":aq})
                    db_save_message("user",aq)
                    with st.spinner("يفكر..."): ans=call_brain(aq,"",f"بحث '{q}':\n{result}")
                    st.session_state.messages.append({"role":"assistant","content":ans})
                    db_save_message("assistant",ans)
                    st.session_state.page="🧠 غرفة المشورة"; st.rerun()
            with c_d2:
                if st.button("🗑️", key=f"ds_{q[:15]}"):
                    del st.session_state.search_results[q]; st.rerun()

# ══════════════════════════════════════════
# PAGE: الأسعار التاريخية
# ══════════════════════════════════════════
elif pg == "📈 الأسعار التاريخية":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📈 الأسعار التاريخية — المقارنة عبر الزمن</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>كل عملية جلب تُحفظ تلقائياً — تتبّع حركة الأسعار</div>
    </div>""", unsafe_allow_html=True)

    if not has_supabase():
        st.markdown("""<div class='alert-r'>🗄️ الأسعار التاريخية تحتاج Supabase — أضف SUPABASE_URL و SUPABASE_KEY في Secrets</div>""",
                    unsafe_allow_html=True)
    else:
        history = db_load_price_history(10)
        if not history:
            st.markdown("""<div style='text-align:center;padding:2rem;color:#A8B8CC;'>
            لا يوجد تاريخ بعد — اجلب الأسعار من الشريط الجانبي وستُحفظ تلقائياً
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:0.78rem;color:#A8B8CC;margin-bottom:0.7rem;'>آخر {len(history)} عمليات جلب محفوظة في Supabase</div>",
                        unsafe_allow_html=True)
            sym_sel = st.selectbox(
                "اختر سهماً للمقارنة",
                list(STOCKS_META.keys()),
                format_func=lambda x: f"{x} — {STOCKS_META[x]['name']}"
            )
            if sym_sel:
                cost      = STOCKS_META[sym_sel]["cost"]
                rows_data = []
                for h in history:
                    p = h["prices"].get(sym_sel)
                    if p:
                        loss = ((p - cost) / cost) * 100
                        t    = h["time"][:16].replace("T"," ")
                        rows_data.append({"الوقت":t,"السعر":p,"الخسارة%":round(loss,1)})
                if rows_data:
                    df_hist = pd.DataFrame(rows_data)
                    st.line_chart(df_hist.set_index("الوقت")["السعر"])
                    for row in rows_data:
                        clr = "#E74C3C" if row["الخسارة%"] <= -20 else "#E67E22" if row["الخسارة%"] < 0 else "#2ECC71"
                        st.markdown(f"""<div class='hist-row'>
                        <span style='color:#A8B8CC;'>{row["الوقت"]}</span> ·
                        <span style='color:#C9A84C;font-family:IBM Plex Mono;'>{row["السعر"]:.2f} ر</span> ·
                        <span style='color:{clr};'>{row["الخسارة%"]:.1f}%</span>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.info("لا يوجد بيانات لهذا السهم في التاريخ المحفوظ")

# ══════════════════════════════════════════
# ✅ إصلاح خلل ٦ — المجلس: محتوى كامل
# ══════════════════════════════════════════
elif pg == "👥 المجلس":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>👥 المجلس الاقتصادي الأعلى — 21 عضواً</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>الميثاق السيادي V10.0 · تجسيد الأنا الكامل</div>
    </div>""", unsafe_allow_html=True)

    # تصفية حسب المجموعة
    groups = list(dict.fromkeys(m["group"] for m in MEMBERS))
    sel_group = st.radio("الفئة", groups, horizontal=True, label_visibility="collapsed")

    filtered = [m for m in MEMBERS if m["group"] == sel_group]
    for m in filtered:
        with st.expander(f"#{m['num']} — {m['name']}"):
            st.markdown(f"""<div class='member-card'>
            <div style='display:flex;gap:1rem;align-items:flex-start;'>
            <div style='background:{m["color"]}22;border:1px solid {m["color"]}55;border-radius:8px;
            padding:0.5rem 0.8rem;font-size:1.4rem;flex-shrink:0;text-align:center;min-width:48px;'>
            {m["num"]}</div>
            <div style='flex:1;'>
                <div style='font-size:0.9rem;font-weight:800;color:#E8C97A;'>{m["name"]}</div>
                <div style='font-size:0.72rem;color:#A8B8CC;margin:0.2rem 0 0.6rem;'>{m["role"]}</div>
                <div style='font-size:0.75rem;font-weight:700;color:{m["color"]};margin-bottom:0.3rem;'>المهام المعتمدة:</div>
                {''.join([f"<div style='font-size:0.72rem;color:#E8EDF5;margin-bottom:0.2rem;'>• {t}</div>" for t in m["tasks"]])}
            </div>
            </div>
            </div>""", unsafe_allow_html=True)

            if st.button(f"🧠 استشر {m['name']}", key=f"consult_{m['num']}", use_container_width=True):
                q = f"تحدث بضمير المتكلم بصفتك {m['name']} ({m['role']}) — ما رأيك في الوضع الراهن للمحفظة وما أولوياتك؟"
                st.session_state.messages.append({"role":"user","content":q})
                db_save_message("user",q)
                with st.spinner(f"يفكر {m['name']}..."): ans=call_brain(q)
                st.session_state.messages.append({"role":"assistant","content":ans})
                db_save_message("assistant",ans)
                st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# ✅ إصلاح خلل ٦ — التقارير
# ══════════════════════════════════════════
elif pg == "📁 التقارير":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📁 أرشيف التقارير السيادية</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>Genesis Audit v1.0 · الجرد 08-03-2026</div>
    </div>""", unsafe_allow_html=True)

    reports = [
        {"title":"Genesis Audit v1.0","date":"08-03-2026","status":"مكتمل ✅","desc":"الجرد الشامل للأصول والخصوم — نقطة الصفر السيادية","color":"#2ECC71"},
        {"title":"تقرير الفائض الضائع","date":"29-03-2026","status":"قادم 🔵","desc":"بوري + PwC — أين ذهب الفائض السنوي 707,088 ريال؟","color":"#3498DB"},
        {"title":"ميزانية الحقيقة","date":"29-03-2026","status":"قادم 🔵","desc":"Truth Balance Sheet — أرقام موثّقة لا تقديرية","color":"#3498DB"},
        {"title":"تقييمات العقارات","date":"31-03-2026","status":"قادم 🔵","desc":"لي كا شينج + بويز — المنزل + 3 أراضٍ + تسوية الجله","color":"#E67E22"},
        {"title":"التقرير الشهري الموحد","date":"01-04-2026","status":"قادم 🔵","desc":"تيم كوك — جرد الأكسجين والسيولة الشهري","color":"#2ECC71"},
        {"title":"معادلات الخروج","date":"05-04-2026","status":"قادم 🔵","desc":"آيكان + لي + بويز — ROT الأراضي وصيغ الخروج من الشراكات","color":"#C9A84C"},
    ]

    for r in reports:
        col_clr = r["color"]
        st.markdown(f"""<div style='background:rgba(22,32,64,0.5);border:1px solid {col_clr}33;
        border-right:3px solid {col_clr};border-radius:8px;padding:0.8rem 1rem;margin-bottom:0.5rem;'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
        <div>
            <div style='font-size:0.85rem;font-weight:800;'>{r["title"]}</div>
            <div style='font-size:0.68rem;color:#A8B8CC;margin-top:0.2rem;'>📅 {r["date"]} · {r["desc"]}</div>
        </div>
        <div style='background:{col_clr}22;color:{col_clr};border:1px solid {col_clr}44;
        padding:0.15rem 0.6rem;border-radius:100px;font-size:0.7rem;font-weight:700;white-space:nowrap;'>{r["status"]}</div>
        </div></div>""", unsafe_allow_html=True)

    if st.session_state.prices and PDF_AVAILABLE:
        st.markdown("<hr>", unsafe_allow_html=True)
        pdf_buf = generate_pdf(st.session_state.prices)
        if pdf_buf:
            st.download_button(
                "📥 تحميل Genesis Audit PDF",
                data=pdf_buf,
                file_name=f"genesis_audit_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.markdown("<div class='alert-y'>⚠️ اجلب الأسعار أولاً لتفعيل تصدير PDF</div>", unsafe_allow_html=True)

    if st.button("🧠 انتقل لغرفة المشورة", use_container_width=True):
        st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# ✅ إصلاح خلل ٦ — القناصون
# ══════════════════════════════════════════
elif pg == "🎯 القناصون":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>🎯 قاعة القناصين — تنبيهات وفرص</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>رادار الخسائر · القانون 20% · فرص القنص الفني</div>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.prices:
        st.markdown("<div class='alert-y'>⚠️ اجلب الأسعار أولاً لتفعيل رادار القناصين</div>", unsafe_allow_html=True)
    else:
        surgical, watch, ok_list = [], [], []
        for sym, info in STOCKS_META.items():
            p = st.session_state.prices.get(sym)
            if not p: continue
            loss = ((p - info["cost"]) / info["cost"]) * 100
            val  = p * info["shares"]
            entry = {"sym":sym,"name":info["name"],"p":p,"cost":info["cost"],"loss":loss,"val":val,"shares":info["shares"]}
            if   loss <= -20: surgical.append(entry)
            elif loss <  0:   watch.append(entry)
            else:             ok_list.append(entry)

        # جراحية
        if surgical:
            st.markdown(f"<div class='alert-r'>🔴 <strong>{len(surgical)} أسهم تجاوزت حد 20% — قرار عاجل مطلوب</strong></div>",
                        unsafe_allow_html=True)
            for e in sorted(surgical, key=lambda x: x["loss"]):
                c="$" if e["sym"]=="LCID" else "ر"
                st.markdown(f"""<div style='background:rgba(231,76,60,0.07);border:1px solid rgba(231,76,60,0.3);
                border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.4rem;'>
                <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;'>
                <div>
                    <span style='font-weight:800;'>{e["name"]} ({e["sym"]})</span>
                    <span style='font-size:0.7rem;color:#A8B8CC;margin-right:0.5rem;'>{e["shares"]} سهم</span>
                </div>
                <div style='display:flex;gap:0.8rem;align-items:center;flex-wrap:wrap;'>
                    <span style='font-family:IBM Plex Mono;font-size:0.85rem;color:#C9A84C;'>الآن: {e["p"]:.2f}{c}</span>
                    <span style='font-family:IBM Plex Mono;font-size:0.85rem;color:#A8B8CC;'>تكلفة: {e["cost"]:.2f}{c}</span>
                    <span class='swarn'>{e["loss"]:.1f}%</span>
                    <span style='font-family:IBM Plex Mono;font-size:0.82rem;color:#E74C3C;'>{e["val"]:,.0f} ر</span>
                </div>
                </div></div>""", unsafe_allow_html=True)

        # متابعة
        if watch:
            st.markdown(f"<div class='alert-y' style='margin-top:0.5rem;'>🟡 {len(watch)} أسهم تحت المتابعة (خسارة أقل من 20%)</div>",
                        unsafe_allow_html=True)

        # رابحة
        if ok_list:
            st.markdown(f"<div class='alert-g' style='margin-top:0.5rem;'>🟢 {len(ok_list)} أسهم رابحة أو في التعادل</div>",
                        unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🧠 طلب توصية جراحية من PTJ + بوري", use_container_width=True):
            q = "بصفتك بول تودور جونز ومايكل بوري معاً — قدّم توصية جراحية تقنية وجنائية لكل سهم تجاوز 20%، مع تحديد سعر الخروج الأمثل وفق المادة 3 من الميثاق."
            st.session_state.messages.append({"role":"user","content":q})
            db_save_message("user",q)
            with st.spinner("PTJ + بوري يفكران..."): ans=call_brain(q)
            st.session_state.messages.append({"role":"assistant","content":ans})
            db_save_message("assistant",ans)
            st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# ✅ إصلاح خلل ٦ — الحوكمة
# ══════════════════════════════════════════
elif pg == "⚖️ الحوكمة":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>⚖️ الحوكمة — القوانين المقدسة</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>المادة (3) من الميثاق السيادي V10.0 — Hard Constraints</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='alert-r'>🚨 هذه المادة أوامر برمجية صلبة — لا يملك المجلس صلاحية الاجتهاد فيها. أي خرق = بند الفناء فوراً.</div>",
                unsafe_allow_html=True)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    for law in LAWS:
        st.markdown(f"""<div class='law-item' style='border-right-color:{law["color"]};'>
        <div style='display:flex;gap:0.8rem;align-items:flex-start;'>
        <div style='background:{law["color"]}22;color:{law["color"]};border:1px solid {law["color"]}44;
        border-radius:6px;padding:0.15rem 0.5rem;font-size:0.75rem;font-weight:800;
        font-family:IBM Plex Mono;flex-shrink:0;'>#{law["num"]}</div>
        <div>
            <div style='font-weight:800;font-size:0.85rem;color:{law["color"]};'>{law["title"]}</div>
            <div style='font-size:0.75rem;color:#A8B8CC;margin-top:0.2rem;'>{law["desc"]}</div>
        </div>
        </div></div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""<div class='alert-b'>
    🛡️ <strong>بروتوكول بند الفناء:</strong> يُفعَّل عند خسارة 25% من رأس المال المدار — إقالة جماعية فورية. 
    حالة الاستنفار القصوى: تُعلَّن عند خسارة 10% من القيمة الإجمالية للثروة.
    </div>""", unsafe_allow_html=True)

    if st.button("🧠 اسأل طالب عن مخاطر الحوكمة", use_container_width=True):
        q = "بصفتك ناسم طالب — اختبر المحفظة الحالية مقابل القوانين المقدسة العشرة. ما القوانين المنتهكة أو المهددة حالياً؟"
        st.session_state.messages.append({"role":"user","content":q})
        db_save_message("user",q)
        with st.spinner("طالب يفكر..."): ans=call_brain(q)
        st.session_state.messages.append({"role":"assistant","content":ans})
        db_save_message("assistant",ans)
        st.session_state.page="🧠 غرفة المشورة"; st.rerun()

# ══════════════════════════════════════════
# ✅ إصلاح خلل ٦ — الذاكرة
# ══════════════════════════════════════════
elif pg == "📜 الذاكرة":
    st.markdown("""<div class='shdr'>
    <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>📜 الذاكرة السيادية — Supabase</div>
    <div style='font-size:0.63rem;color:#A8B8CC;'>سجل القرارات الجراحية · شيفرة استعادة الوعي</div>
    </div>""", unsafe_allow_html=True)

    if not has_supabase():
        st.markdown("""<div class='alert-r'>🗄️ الذاكرة تحتاج Supabase — أضف SUPABASE_URL و SUPABASE_KEY في Streamlit Secrets</div>""",
                    unsafe_allow_html=True)
    else:
        msgs_db = db_load_messages(30)
        total   = len(msgs_db)
        user_c  = sum(1 for m in msgs_db if m["role"]=="user")
        asst_c  = total - user_c

        # إحصاءات
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"<div class='pc'><div class='pl'>إجمالي الرسائل</div><div class='pv' style='color:#C9A84C;'>{total}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='pc'><div class='pl'>أسئلة المجلس</div><div class='pv' style='color:#3498DB;'>{user_c}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='pc'><div class='pl'>ردود دماغ المجلس</div><div class='pv' style='color:#9B59B6;'>{asst_c}</div></div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.78rem;color:#A8B8CC;margin-bottom:0.5rem;'>آخر {min(10,total)} رسالة من Supabase</div>",
                    unsafe_allow_html=True)

        if msgs_db:
            for m in msgs_db[-10:]:
                css     = "msg-user" if m["role"]=="user" else "msg-ai"
                preview = m["content"][:250]+"..." if len(m["content"])>250 else m["content"]
                st.markdown(f"<div class='{css}' style='font-size:0.75rem;'>{preview}</div>",
                            unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align:center;padding:1.5rem;color:#A8B8CC;'>لا توجد رسائل محفوظة بعد — ابدأ محادثة في غرفة المشورة</div>",
                        unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""<div class='alert-b'>
        🔑 <strong>شيفرة استعادة الوعي:</strong> انسخ هذا النص في بداية أي جلسة جديدة لاستعادة الذاكرة:<br>
        <code style='font-size:0.72rem;color:#E8C97A;'>"أبو عبدالله — استعادة وعي المجلس — جرد 08-03-2026 — الميثاق V10.0"</code>
        </div>""", unsafe_allow_html=True)

    if st.button("🧠 انتقل لغرفة المشورة", use_container_width=True):
        st.session_state.page="🧠 غرفة المشورة"; st.rerun()
