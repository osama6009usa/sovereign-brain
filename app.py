import streamlit as st
import anthropic

st.set_page_config(
    page_title="دماغ المجلس السيادي",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&family=IBM+Plex+Mono:wght@400;600&display=swap');
html, body, [class*="css"] {
    direction: rtl; text-align: right;
    font-family: 'Tajawal', sans-serif !important;
    background-color: #0A0F1E !important;
    color: #E8EDF5 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.main .block-container { padding: 1.5rem 2rem; max-width: 1200px; background: #0A0F1E; }
[data-testid="stSidebar"] {
    background: #08090F !important;
    border-left: 1px solid rgba(201,168,76,0.2) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.2rem 1rem; }
.msg-ai {
    background: rgba(22,32,64,0.8);
    border: 1px solid rgba(155,89,182,0.25);
    border-radius: 14px 14px 14px 0;
    padding: 1rem 1.2rem; margin: 0.6rem 0;
    font-size: 0.9rem; line-height: 1.75;
    direction: rtl; text-align: right; color: #E8EDF5;
}
.msg-user {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 14px 14px 0 14px;
    padding: 1rem 1.2rem; margin: 0.6rem 0;
    font-size: 0.9rem; direction: rtl;
    text-align: right; color: #E8C97A;
}
.stTextArea textarea {
    direction: rtl !important; text-align: right !important;
    font-family: 'Tajawal', sans-serif !important;
    background: rgba(22,32,64,0.7) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    color: #E8EDF5 !important; border-radius: 10px !important;
    font-size: 0.88rem !important;
}
.stButton button {
    background: rgba(201,168,76,0.12) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: #E8C97A !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important; border-radius: 8px !important;
}
.metric-card {
    background: rgba(22,32,64,0.6);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px; padding: 0.9rem 1rem; text-align: center;
}
.metric-label { font-size: 0.65rem; color: #A8B8CC; margin-bottom: 0.3rem; }
.metric-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.3rem; font-weight: 700; }
.status-ok {
    background: rgba(46,204,113,0.1); border: 1px solid rgba(46,204,113,0.3);
    color: #69db7c; padding: 0.3rem 0.8rem; border-radius: 100px;
    font-size: 0.7rem; font-weight: 700; display: inline-block;
}
hr { border-color: rgba(201,168,76,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ── قاعدة المعرفة السيادية ──
SYSTEM_PROMPT = """أنت "دماغ المجلس السيادي" — المرجع القطعي لـ "أبو عبدالله" (القاضي السيادي) في إدارة ثروته الشخصية وفق الميثاق السيادي V10.0.

هويتك:
- دماغ مجلس اقتصادي من 21 شخصية استثمارية عالمية
- لغتك: دقيقة، مباشرة، ملتزمة بالحوكمة، بلا مجاملة
- كل إجابة تستند للميثاق أو الجرد أو القرارات المعتمدة
- تُشير للعضو المختص في كل إجابة
- الترميز اللوني: 🟢 يقين قطعي / 🟡 توقع مدروس / 🔴 بيانات ناقصة

القوانين المقدسة:
١. وقف الخسارة 20% — آلي فوري لا استثناء
٢. فلتر الائتمان 33%
٣. صمام العائلة 270,208 ريال — محظور المساس به
٤. تحريم الروافع — صفر مديونية للاستثمار
٥. أرضية السيولة 20% دائماً
٦. سقف التركيز 15% لأصل واحد
٧. فترة التبريد 48 ساعة
٨. الفلتر الشرعي
٩. الانتظار الذكي 30 يوم (مونجر) — بعد أي جراحة
١٠. الفصل السيادي — الثروة الشخصية فقط

الجرد المالي (08-03-2026):
- الدخل: 103,959 ريال/شهر | الفائض: 58,924 ريال (56.7%)
- الودائع: 3,735,756 ريال | الديون: 2,815,970 ريال
- أسهم سعودية: -24.1% | جراحية: كيمانول(-34.7%) أسمنت(-39.4%) جبل عمر(-37.3%) مسار(-21.5%) النهدي(-20.1%)
- LCID: -65.4% | CHR: -92.3% | TRX: -12.1%
- العقارات: منزل(2.4M) + أراضٍ 3 (حصة 50%) + الجله (بلا صك — خطر وجودي)
- الشركات: BMP 100% / لؤي 37% / SEAT 49% / دريم فالي 12% / انفستكورب (NAV مجهول)

أعضاء المجلس:
١. وكيل PwC — نزاهة مالية، فيتو شرعي
٢. ديفيد بويز — قانوني دولي، تكليف: الجله + معادلات الخروج
٣. بيل أكمان — تحري الشركاء، تبريد 24 ساعة
٤. ناسم طالب — Anti-Fragility، البجعة السوداء
٥. وارن بافيت — قيمة جوهرية، هامش أمان 30%
٦. راي داليو — توازن أصول، All Weather
٧. نافال رافيكانت — روافع، هدف الحرية 10.8M ريال
٨. لي كا شينج — عقار، ROT معيار 4%
٩. تشارلي مونجر — نماذج ذهنية، الانتظار الذكي 30 يوم
١٠. خبير رؤية 2030 — مواءمة وطنية، نطاق محدود
١١. مايكل بوري — تشريح جنائي، ميزانية الحقيقة
١٢. PTJ — توقيت ونبض السوق
١٣. كارل آيكان — ناشط، ROT الأراضي، معادلات الخروج مع بويز
١٤. جيف بيزوس — كفاءة تشغيلية، مبدأ اليوم الأول
١٥. جورج سوروس — انعكاسية، رادار الحيتان
١٦. بيتر ثيل — احتكار، نطاق محدود
١٧. جينسن هوانغ — تقنية وذكاء اصطناعي
١٨. تيم كوك — لوجستيات، جرد الأكسجين
١٩. هوارد ماركس — بندول المخاطرة /10
٢٠. جيمس تشانوس — صائد احتيال، نطاق محدود
٢١. إيان بريمر — جيوسياسي، رادار النفط

التكليفات المعتمدة:
- بوري + PwC: الفائض الضائع ~3.5M (29 مارس)
- آيكان + لي كا شينج: ROT الأراضي (5 أبريل)
- آيكان + بويز: معادلات الخروج (5 أبريل)
- بويز: الجله لصكوك (31 مارس)
- الجلسة الجراحية: 22 مارس 2026

أجب دائماً بالعربية. دقيق ومفصّل. استشهد بالأعضاء والأرقام. استخدم الترميز اللوني."""

TOPICS = [
    ("📜", "الميثاق السيادي V10.0"),
    ("👥", "أعضاء المجلس ومهامهم"),
    ("💰", "الجرد المالي الكامل"),
    ("📈", "الأسهم والجلسة الجراحية"),
    ("🏗️", "الأصول العقارية"),
    ("💸", "الديون والتدفق النقدي"),
    ("⚖️", "القوانين والبروتوكولات"),
    ("✅", "القرارات المعتمدة"),
    ("🤝", "الشراكات والشركات"),
    ("🔗", "التنسيق بين الأعضاء"),
]

QUICK_QUESTIONS = [
    "ما بروتوكول الانتظار الذكي 30 يوم؟",
    "من يملك حق النقض وكيف؟",
    "مهام مايكل بوري كاملة؟",
    "الأسهم المرشحة للجراحة؟",
    "ما هو صمام العائلة؟",
    "المعادلة الذهبية للقرار؟",
    "متى يُفعَّل بند الفناء؟",
    "ملخص الجرد المالي؟",
    "تكليفات آيكان مع بويز؟",
    "القيود السيادية على الأعضاء؟",
]

# ── قراءة API Key من Secrets تلقائياً ──
def get_api_key():
    # أولاً: من Streamlit Secrets (التلقائي بعد الإعداد)
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
        if key and key.startswith("sk-"):
            return key, "secrets"
    except Exception:
        pass
    # ثانياً: من إدخال المستخدم اليدوي
    if "manual_api_key" in st.session_state and st.session_state.manual_api_key:
        return st.session_state.manual_api_key, "manual"
    return None, None

# ── Session State ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = "الميثاق السيادي V10.0"
if "manual_api_key" not in st.session_state:
    st.session_state.manual_api_key = ""

api_key, key_source = get_api_key()

# ── استدعاء الدماغ ──
def call_brain(question: str, topic: str) -> str:
    key, _ = get_api_key()
    if not key:
        return "🔴 لم يتم إعداد API Key — أدخله في الشريط الجانبي أو في Streamlit Secrets."
    try:
        client = anthropic.Anthropic(api_key=key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"الموضوع: {topic}\n\nالسؤال: {question}"}]
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "🔴 **مفتاح خاطئ** — تحقق من صحة API Key."
    except anthropic.RateLimitError:
        return "🟡 **تجاوز الحد** — انتظر دقيقة وحاول مجدداً."
    except Exception as e:
        return f"🔴 **خطأ:** {str(e)}"

# ── الشريط الجانبي ──
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 1rem;border-bottom:1px solid rgba(201,168,76,0.2);margin-bottom:1rem;'>
        <div style='font-size:1.1rem;font-weight:800;color:#E8C97A;'>⬡ دماغ المجلس</div>
        <div style='font-size:0.68rem;color:#A8B8CC;margin-top:0.2rem;'>الميثاق السيادي V10.0</div>
    </div>
    """, unsafe_allow_html=True)

    # حالة الاتصال
    if api_key and key_source == "secrets":
        st.markdown("<div class='status-ok'>🟢 متصل تلقائياً</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.62rem;color:#A8B8CC;margin-top:0.4rem;'>المفتاح محفوظ في Secrets</div>", unsafe_allow_html=True)
    elif api_key and key_source == "manual":
        st.markdown("<div class='status-ok'>🟢 متصل</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.7rem;color:#ff8a80;margin-bottom:0.5rem;'>🔑 أدخل API Key للبدء</div>", unsafe_allow_html=True)
        manual_key = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed"
        )
        if manual_key:
            st.session_state.manual_api_key = manual_key
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # الموضوعات
    st.markdown("<div style='font-size:0.62rem;color:#A8B8CC;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:0.5rem;'>📁 موضوعات المكتبة</div>", unsafe_allow_html=True)
    for icon, topic in TOPICS:
        is_active = st.session_state.current_topic == topic
        label = f"{'← ' if is_active else ''}{icon} {topic}"
        if st.button(label, key=f"t_{topic}", use_container_width=True):
            st.session_state.current_topic = topic
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style='margin-top:1rem;font-size:0.58rem;color:#A8B8CC;line-height:1.6;direction:rtl;'>
        مدعوم بـ Claude Sonnet<br>
        الميثاق + الجرد + القرارات<br>
        <span style='color:rgba(201,168,76,0.4);'>سري · مجلس أبو عبدالله</span>
    </div>
    """, unsafe_allow_html=True)

# ── المنطقة الرئيسية ──
st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(22,32,64,0.95),rgba(15,23,41,0.9));border:1px solid rgba(201,168,76,0.25);border-top:2px solid #C9A84C;border-radius:14px;padding:1.2rem 1.8rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:1rem;'>
    <div style='font-size:2rem;'>🧠</div>
    <div style='flex:1;'>
        <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>غرفة المشورة — دماغ المجلس السيادي</div>
        <div style='font-size:0.68rem;color:#A8B8CC;'>مرجع قطعي · الميثاق V10.0 · الجرد 08-03-2026</div>
    </div>
    <div style='background:rgba(155,89,182,0.12);border:1px solid rgba(155,89,182,0.3);color:#c39bd3;font-size:0.7rem;font-weight:700;padding:0.25rem 0.8rem;border-radius:100px;'>
        {st.session_state.current_topic}
    </div>
</div>
""", unsafe_allow_html=True)

# مؤشرات المحفظة
c1, c2, c3, c4, c5 = st.columns(5)
for col, (lbl, val, clr) in zip([c1,c2,c3,c4,c5], [
    ("💚 الفائض الشهري", "58,924 ر", "#2ECC71"),
    ("🏦 الودائع", "3.7M ر", "#C9A84C"),
    ("💸 الديون", "2.8M ر", "#E74C3C"),
    ("📉 خسارة الأسهم", "-24.1%", "#E74C3C"),
    ("🛡️ صمام العائلة", "270K ر", "#C9A84C"),
]):
    with col:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>{lbl}</div><div class='metric-value' style='color:{clr};'>{val}</div></div>", unsafe_allow_html=True)

st.markdown("<div style='margin:0.8rem 0 0.4rem;font-size:0.68rem;color:#A8B8CC;'>⚡ أسئلة سريعة:</div>", unsafe_allow_html=True)

# أسئلة سريعة
cols = st.columns(5)
for i, q in enumerate(QUICK_QUESTIONS[:5]):
    with cols[i]:
        short = q[:18] + "..." if len(q) > 18 else q
        if st.button(short, key=f"q_{i}", use_container_width=True):
            if not api_key:
                st.error("أدخل API Key أولاً")
            else:
                st.session_state.messages.append({"role": "user", "content": q})
                with st.spinner("دماغ المجلس يفكر..."):
                    ans = call_brain(q, st.session_state.current_topic)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# المحادثة
if not st.session_state.messages:
    st.markdown("""
    <div class='msg-ai'>
        مرحباً يا أبا عبدالله — أنا دماغ المجلس السيادي.<br><br>
        أحمل الميثاق السيادي V10.0 كاملاً، ملفات الـ21 عضواً، الجرد المالي 08-03-2026، القوانين المقدسة، وجميع القرارات والتكليفات.<br><br>
        اختر موضوعاً من القائمة أو اسألني مباشرة. 🟢
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        css = "msg-user" if msg["role"] == "user" else "msg-ai"
        content = msg["content"].replace("\n", "<br>")
        st.markdown(f"<div class='{css}'>{content}</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin:0.6rem 0;'>", unsafe_allow_html=True)

# خانة الإدخال
with st.form("chat_form", clear_on_submit=True):
    col_in, col_btn = st.columns([5, 1])
    with col_in:
        user_q = st.text_area(
            "السؤال",
            placeholder="اسأل دماغ المجلس...",
            label_visibility="collapsed",
            height=75,
        )
    with col_btn:
        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        send = st.form_submit_button("↗ إرسال", use_container_width=True)

    if send and user_q.strip():
        if not api_key:
            st.error("أدخل API Key في الشريط الجانبي أولاً")
        else:
            st.session_state.messages.append({"role": "user", "content": user_q.strip()})
            with st.spinner("دماغ المجلس يفكر..."):
                ans = call_brain(user_q.strip(), st.session_state.current_topic)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()

st.markdown("""
<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);border-right:3px solid #C9A84C;border-radius:8px;padding:0.7rem 1rem;margin-top:0.8rem;font-size:0.75rem;color:#E8C97A;direction:rtl;'>
    ⚖️ <strong>قانون الانتظار الذكي (مونجر):</strong> لا إعادة استثمار لأي سيولة محررة قبل 30 يوماً من الجلسة الجراحية
</div>
""", unsafe_allow_html=True)
