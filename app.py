import streamlit as st
import anthropic
import time

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="دماغ المجلس السيادي",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* Global RTL + Dark Theme */
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
    font-family: 'Tajawal', sans-serif !important;
    background-color: #0A0F1E !important;
    color: #E8EDF5 !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.main .block-container {
    padding: 1.5rem 2rem;
    max-width: 1200px;
    background: #0A0F1E;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #08090F !important;
    border-left: 1px solid rgba(201,168,76,0.2) !important;
    min-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.2rem 1rem;
}

/* Header */
.sovereign-header {
    background: linear-gradient(135deg, rgba(22,32,64,0.95), rgba(15,23,41,0.9));
    border: 1px solid rgba(201,168,76,0.25);
    border-top: 2px solid #C9A84C;
    border-radius: 14px;
    padding: 1.2rem 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Chat messages */
.msg-ai {
    background: rgba(22,32,64,0.8);
    border: 1px solid rgba(155,89,182,0.25);
    border-radius: 14px 14px 14px 0;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.9rem;
    line-height: 1.75;
    direction: rtl;
    text-align: right;
    color: #E8EDF5;
    position: relative;
}
.msg-ai::before {
    content: '🧠';
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 1.1rem;
    background: rgba(155,89,182,0.2);
    border: 1px solid rgba(155,89,182,0.35);
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 30px;
    text-align: center;
}

.msg-user {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 14px 14px 0 14px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.9rem;
    direction: rtl;
    text-align: right;
    color: #E8C97A;
}

/* Quick chips */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 0.8rem 0;
    direction: rtl;
}
.chip {
    background: rgba(155,89,182,0.08);
    border: 1px solid rgba(155,89,182,0.25);
    color: #A8B8CC;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.75rem;
    cursor: pointer;
    font-family: 'Tajawal', sans-serif;
    transition: all 0.2s;
    display: inline-block;
}

/* Input box */
.stTextArea textarea {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Tajawal', sans-serif !important;
    background: rgba(22,32,64,0.7) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    color: #E8EDF5 !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
.stTextArea textarea:focus {
    border-color: rgba(155,89,182,0.5) !important;
    box-shadow: 0 0 0 2px rgba(155,89,182,0.1) !important;
}

/* Buttons */
.stButton button {
    background: rgba(201,168,76,0.12) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: #E8C97A !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: rgba(201,168,76,0.22) !important;
    border-color: rgba(201,168,76,0.5) !important;
}

/* Sidebar topic buttons */
.topic-btn {
    width: 100%;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    color: #A8B8CC;
    font-family: 'Tajawal', sans-serif;
    font-size: 0.78rem;
    cursor: pointer;
    text-align: right;
    direction: rtl;
    margin-bottom: 0.2rem;
    transition: all 0.2s;
    display: block;
}

/* Dividers */
hr {
    border-color: rgba(201,168,76,0.15) !important;
}

/* Metrics */
.metric-card {
    background: rgba(22,32,64,0.6);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
    direction: rtl;
}
.metric-label {
    font-size: 0.65rem;
    color: #A8B8CC;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
}

/* Scrollable chat area */
.chat-scroll {
    max-height: 520px;
    overflow-y: auto;
    padding: 0.5rem;
    border: 1px solid rgba(201,168,76,0.12);
    border-radius: 12px;
    background: rgba(8,12,28,0.5);
    margin-bottom: 1rem;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.25);
    color: #69db7c;
    padding: 0.2rem 0.7rem;
    border-radius: 100px;
    font-size: 0.68rem;
    font-weight: 700;
}
.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2ECC71;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Alert boxes */
.alert-red {
    background: rgba(231,76,60,0.07);
    border: 1px solid rgba(231,76,60,0.25);
    border-right: 3px solid #E74C3C;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #ff8a80;
    font-size: 0.8rem;
    direction: rtl;
    margin: 0.6rem 0;
}
.alert-gold {
    background: rgba(201,168,76,0.07);
    border: 1px solid rgba(201,168,76,0.25);
    border-right: 3px solid #C9A84C;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #E8C97A;
    font-size: 0.8rem;
    direction: rtl;
    margin: 0.6rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Knowledge Base ────────────────────────────────────────────
SYSTEM_PROMPT = """أنت "دماغ المجلس السيادي" — المرجع القطعي والمساعد الشخصي لـ "أبو عبدالله" (القاضي السيادي) في إدارة ثروته الشخصية وفق الميثاق السيادي V10.0.

هويتك وسلوكك:
- أنت دماغ مجلس اقتصادي مكون من 21 شخصية استثمارية عالمية
- تتكلم بلغة المجلس: دقيقة، مباشرة، ملتزمة بالحوكمة، بلا مجاملة ولا إنشاء
- كل إجابة تستند للميثاق أو الجرد المالي أو القرارات المعتمدة
- عند الإجابة تُشير للعضو المختص (مثلاً: "بوري يرى..." أو "مونجر يحذر من...")
- تستخدم الترميز اللوني: 🟢 يقين قطعي / 🟡 توقع مدروس / 🔴 حدس أو بيانات ناقصة

القوانين المقدسة (لا تحيد عنها أبداً):
١. وقف الخسارة 20% — آلي فوري لا استثناء
٢. فلتر الائتمان 33% (استثناء 40% بإجماع جدار المناعة)
٣. صمام العائلة 270,208 ريال — محظور المساس به
٤. تحريم الروافع — صفر مديونية للاستثمار
٥. أرضية السيولة 20% دائماً
٦. سقف التركيز 15% لأصل واحد
٧. فترة التبريد 48 ساعة
٨. الفلتر الشرعي — PwC يحسب التطهير
٩. الانتظار الذكي 30 يوم (مونجر) — لا إعادة استثمار بعد الجراحة
١٠. الفصل السيادي — الثروة الشخصية فقط

الجرد المالي (08-03-2026):
- الدخل: 103,959 ريال/شهر | الفائض: 58,924 ريال (56.7%)
- الودائع: 3,735,756 ريال | الديون: 2,815,970 ريال
- أسهم سعودية: 314,993 ريال (-24.1%) | 5 أسهم جراحية: كيمانول(-34.7%) أسمنت(-39.4%) جبل عمر(-37.3%) مسار(-21.5%) النهدي(-20.1%)
- LCID: -65.4% | CHR: -92.3% | TRX: -12.1%
- العقارات: منزل (2.4M) + 3 أراضٍ (حصة 50%) + أراضي الجله (بلا صك — خطر وجودي)
- الشركات: BMP 100% / لؤي 37% / SEAT 49% / دريم فالي 12% / انفستكورب 1991 وحدة (NAV مجهول)

أعضاء المجلس الـ21:
١. وكيل PwC — نزاهة مالية وامتثال شرعي — فيتو شرعي
٢. ديفيد بويز — قانوني دولي — تكليف: أراضي الجله + معادلات الخروج مع آيكان
٣. بيل أكمان — تحري الشركاء — بروتوكول تبريد 24 ساعة
٤. ناسم طالب — Anti-Fragility — البجعة السوداء — 86% دخل عمل = خطر وجودي
٥. وارن بافيت — قيمة جوهرية — هامش أمان 30% إلزامي
٦. راي داليو — توازن أصول — All Weather Portfolio
٧. نافال رافيكانت — روافع ونمو أسّي — هدف الحرية 10.8M ريال
٨. لي كا شينج — عقار — ROT معيار 4% — تنسيق مع آيكان
٩. تشارلي مونجر — نماذج ذهنية — محامي الشيطان — بروتوكول الانتظار 30 يوم
١٠. خبير رؤية 2030 — مواءمة وطنية — نطاق محدود
١١. مايكل بوري — تشريح جنائي — ميزانية الحقيقة — تحقيق الفائض الضائع
١٢. بول تودور جونز — توقيت ونبض — ساعة الدخول السيادية
١٣. كارل آيكان — ناشط — ROT الأراضي — معادلات الخروج مع بويز
١٤. جيف بيزوس — كفاءة تشغيلية — مبدأ اليوم الأول
١٥. جورج سوروس — انعكاسية — رادار الحيتان السعودي
١٦. بيتر ثيل — احتكار — نطاق محدود للأصول المالية
١٧. جينسن هوانغ — تقنية وذكاء اصطناعي
١٨. تيم كوك — لوجستيات — لوحة القيادة — جرد الأكسجين
١٩. هوارد ماركس — بندول المخاطرة /10
٢٠. جيمس تشانوس — صائد احتيال — نطاق محدود
٢١. إيان بريمر — جيوسياسي — رادار النفط

التكليفات المعتمدة:
- بوري + PwC: تحقيق الفائض الضائع ~3.5M (29 مارس)
- آيكان + لي كا شينج: ROT للأراضي الثلاث (5 أبريل)
- آيكان + بويز: معادلات خروج الشراكات (5 أبريل)
- بويز: تحويل الجله لصكوك (31 مارس)
- الجلسة الجراحية: 22 مارس 2026

أجب دائماً بالعربية. كن دقيقاً ومفصلاً. استشهد بالأعضاء والأرقام. استخدم الترميز اللوني. إذا لم تجد المعلومة قل ذلك بوضوح."""

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
    "ما هو بروتوكول الانتظار الذكي 30 يوماً؟",
    "من يملك حق النقض وفي أي الحالات؟",
    "ما هي مهام مايكل بوري المعتمدة كاملة؟",
    "ما الأسهم المرشحة للجلسة الجراحية؟",
    "ما هو صمام العائلة ومتى يُمنع المساس به؟",
    "كيف تعمل المعادلة الذهبية لاتخاذ القرار؟",
    "ما هو بند الفناء ومتى يُفعَّل؟",
    "لخّص الجرد المالي بأبرز الأرقام",
    "ما تكليفات كارل آيكان مع بويز ولي كا شينج؟",
    "ما القيود السيادية على أعضاء المجلس؟",
]

# ── Session State ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = "الميثاق السيادي V10.0"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ── Helper: call API ──────────────────────────────────────────
def call_brain(question: str, topic: str) -> str:
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)
        full_q = f"الموضوع المختار: {topic}\n\nالسؤال: {question}"
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": full_q}]
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "🔴 **خطأ في المفتاح** — تحقق من صحة Anthropic API Key في الشريط الجانبي."
    except anthropic.RateLimitError:
        return "🟡 **تجاوز الحد** — انتظر دقيقة ثم حاول مجدداً."
    except Exception as e:
        return f"🔴 **خطأ غير متوقع:** {str(e)}"

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div style='padding:0.5rem 0 1rem; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:1rem;'>
        <div style='font-size:1.1rem;font-weight:800;color:#E8C97A;'>⬡ دماغ المجلس</div>
        <div style='font-size:0.68rem;color:#A8B8CC;margin-top:0.2rem;'>الميثاق السيادي V10.0</div>
    </div>
    """, unsafe_allow_html=True)

    # API Key input
    st.markdown("<div style='font-size:0.68rem;color:#A8B8CC;margin-bottom:0.3rem;'>🔑 Anthropic API Key</div>", unsafe_allow_html=True)
    api_key = st.text_input(
        label="API Key",
        type="password",
        placeholder="sk-ant-...",
        label_visibility="collapsed",
        key="api_key_input"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.markdown("<div class='status-badge'><span class='status-dot'></span> مُتصل</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:0.65rem;color:#ff8a80;'>أدخل المفتاح للبدء</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Topics
    st.markdown("<div style='font-size:0.62rem;color:#A8B8CC;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:0.5rem;'>📁 موضوعات المكتبة</div>", unsafe_allow_html=True)

    for icon, topic in TOPICS:
        is_active = st.session_state.current_topic == topic
        color = "#C9A84C" if is_active else "#A8B8CC"
        bg = "rgba(201,168,76,0.1)" if is_active else "transparent"
        border = "1px solid rgba(201,168,76,0.3)" if is_active else "1px solid transparent"
        if st.button(
            f"{icon} {topic}",
            key=f"topic_{topic}",
            use_container_width=True
        ):
            st.session_state.current_topic = topic
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Footer
    st.markdown("""
    <div style='margin-top:1rem;font-size:0.6rem;color:#A8B8CC;line-height:1.6;direction:rtl;'>
        مدعوم بـ Claude Sonnet<br>
        قاعدة المعرفة: الميثاق + الجرد + القرارات<br>
        <span style='color:rgba(201,168,76,0.5);'>سري وخاص — مجلس أبو عبدالله</span>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────

# Header
st.markdown(f"""
<div class='sovereign-header'>
    <div style='font-size:2rem;'>🧠</div>
    <div style='flex:1;'>
        <div style='font-size:1rem;font-weight:800;color:#E8C97A;'>غرفة المشورة — دماغ المجلس السيادي</div>
        <div style='font-size:0.68rem;color:#A8B8CC;margin-top:0.2rem;'>
            مرجع قطعي الحقيقة · الميثاق السيادي V10.0 · الجرد 08-03-2026
        </div>
    </div>
    <div>
        <div style='font-size:0.65rem;color:#A8B8CC;margin-bottom:0.2rem;'>الموضوع الحالي</div>
        <div style='background:rgba(155,89,182,0.12);border:1px solid rgba(155,89,182,0.3);color:#c39bd3;font-size:0.7rem;font-weight:700;padding:0.25rem 0.8rem;border-radius:100px;'>
            {st.session_state.current_topic}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4, col5 = st.columns(5)
metrics = [
    ("💚 الفائض الشهري", "58,924", "#2ECC71"),
    ("🏦 الودائع", "3.7M", "#C9A84C"),
    ("💸 الديون", "2.8M", "#E74C3C"),
    ("📉 خسارة الأسهم", "-24.1%", "#E74C3C"),
    ("🛡️ صمام العائلة", "270K", "#C9A84C"),
]
for col, (label, value, color) in zip([col1,col2,col3,col4,col5], metrics):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value' style='color:{color};'>{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin:1rem 0 0.5rem;'>", unsafe_allow_html=True)

# Quick questions
st.markdown("<div style='font-size:0.68rem;color:#A8B8CC;margin-bottom:0.4rem;'>⚡ أسئلة سريعة:</div>", unsafe_allow_html=True)

# Display chips in rows
cols_per_row = 5
for i in range(0, len(QUICK_QUESTIONS), cols_per_row):
    row_qs = QUICK_QUESTIONS[i:i+cols_per_row]
    cols = st.columns(len(row_qs))
    for col, q in zip(cols, row_qs):
        with col:
            short_label = q[:20] + "..." if len(q) > 20 else q
            if st.button(short_label, key=f"chip_{q}", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("أدخل API Key أولاً في الشريط الجانبي")
                else:
                    st.session_state.messages.append({"role": "user", "content": q})
                    with st.spinner("دماغ المجلس يفكر..."):
                        answer = call_brain(q, st.session_state.current_topic)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
    break  # show only first row for clean UI

st.markdown("<hr style='margin:0.8rem 0;'>", unsafe_allow_html=True)

# Chat messages
if not st.session_state.messages:
    st.markdown("""
    <div class='msg-ai'>
        مرحباً يا أبا عبدالله — أنا دماغ المجلس السيادي.<br><br>
        أحمل الميثاق السيادي V10.0 كاملاً، ملفات الـ21 عضواً، الجرد المالي 08-03-2026،
        القوانين المقدسة، وجميع القرارات والتكليفات الصادرة.<br><br>
        اختر موضوعاً من القائمة الجانبية أو اسألني مباشرة. 🟢
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            content = msg['content'].replace('\n', '<br>').replace('**', '<strong>').replace('**', '</strong>')
            st.markdown(f"<div class='msg-ai'>{content}</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin:0.8rem 0;'>", unsafe_allow_html=True)

# Input area
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_area(
            label="السؤال",
            placeholder="اسأل دماغ المجلس عن الميثاق أو الأعضاء أو الجرد أو القرارات...",
            label_visibility="collapsed",
            height=80,
            key="user_question"
        )
    with col_btn:
        st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("↗ إرسال", use_container_width=True)

    if submitted and user_input.strip():
        if not st.session_state.api_key:
            st.markdown("<div class='alert-red'>⚠️ أدخل Anthropic API Key في الشريط الجانبي أولاً</div>", unsafe_allow_html=True)
        else:
            st.session_state.messages.append({"role": "user", "content": user_input.strip()})
            with st.spinner("دماغ المجلس يفكر..."):
                answer = call_brain(user_input.strip(), st.session_state.current_topic)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

# Bottom alert
st.markdown("""
<div class='alert-gold' style='margin-top:1rem;'>
    ⚖️ <strong>قانون الانتظار الذكي:</strong> لا إعادة استثمار لأي سيولة محررة قبل 30 يوماً من الجلسة الجراحية — مونجر
</div>
""", unsafe_allow_html=True)
