import streamlit as st
from groq import Groq
import json
import random
import time

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketMind – AI Sales & Marketing Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  –  Dark corporate-futuristic with electric-cyan accents
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080c14;
    color: #c9d4e8;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1220; }
::-webkit-scrollbar-thumb { background: #00e5ff44; border-radius: 4px; }

/* ════════════════════════════════
   HERO BANNER
════════════════════════════════ */
.hero-wrap {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    padding: 3.2rem 3rem 2.8rem;
    margin-bottom: 2rem;
    background: linear-gradient(135deg, #050a14 0%, #0a1428 50%, #050e1f 100%);
    border: 1px solid #00e5ff22;
}
.hero-wrap::before {
    content: "";
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 85% 50%, #00e5ff14 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 5% 80%, #7c3aed18 0%, transparent 60%);
    pointer-events: none;
}
.hero-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(0,229,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.04) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
}
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: #00e5ff;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    opacity: 0.85;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.1rem;
    font-weight: 800;
    line-height: 1.05;
    margin: 0 0 0.6rem;
    background: linear-gradient(135deg, #ffffff 30%, #00e5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: #7a92b8;
    font-weight: 400;
    max-width: 580px;
    line-height: 1.65;
    margin-bottom: 1.6rem;
}
.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.hbadge {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    padding: 0.3rem 0.85rem;
    border-radius: 4px;
    border: 1px solid #00e5ff33;
    color: #00e5ff;
    background: rgba(0,229,255,0.07);
    text-transform: uppercase;
}

/* ════════════════════════════════
   METRIC CARDS
════════════════════════════════ */
.metric-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.metric-card {
    flex: 1;
    background: linear-gradient(135deg, #0d1828 0%, #0a1422 100%);
    border: 1px solid #1a2a40;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s;
}
.metric-card:hover { border-color: #00e5ff44; }
.metric-card::after {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    opacity: 0.5;
}
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #00e5ff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label { font-size: 0.78rem; color: #5a7090; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
.metric-delta { font-size: 0.75rem; color: #22c55e; margin-top: 0.3rem; font-family: 'Space Mono', monospace; }

/* ════════════════════════════════
   FEATURE CARDS GRID
════════════════════════════════ */
.feat-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.9rem; margin-bottom: 2rem; }
.feat-card {
    background: #0a1220;
    border: 1px solid #192535;
    border-radius: 14px;
    padding: 1.3rem 1rem;
    text-align: center;
    cursor: default;
    transition: transform 0.2s, border-color 0.2s, background 0.2s;
}
.feat-card:hover {
    transform: translateY(-4px);
    border-color: #00e5ff55;
    background: #0d1930;
}
.feat-icon { font-size: 1.9rem; margin-bottom: 0.5rem; }
.feat-name { font-size: 0.8rem; font-weight: 600; color: #c0d0e8; margin-bottom: 0.2rem; }
.feat-desc { font-size: 0.7rem; color: #415870; line-height: 1.4; }

/* ════════════════════════════════
   SIDEBAR
════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050a14 0%, #08111e 100%) !important;
    border-right: 1px solid #0e1e30 !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] span { color: #7a92b8 !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #00e5ff !important;
}
[data-testid="stSidebar"] hr { border-color: #0e2030 !important; }

/* ════════════════════════════════
   TABS
════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #090f1c;
    border-radius: 10px;
    padding: 4px;
    gap: 3px;
    border: 1px solid #101e30;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #4a6080;
    border-radius: 7px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.45rem 1rem;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00b8cc, #00e5ff) !important;
    color: #050a14 !important;
    font-weight: 700 !important;
}

/* ════════════════════════════════
   BUTTONS
════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #00b8cc 0%, #00e5ff 100%);
    color: #050a14;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.03em;
    padding: 0.55rem 1.5rem;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 0 20px #00e5ff22;
}
.stButton > button:hover {
    opacity: 0.85;
    transform: translateY(-2px);
    box-shadow: 0 0 30px #00e5ff44;
}

/* ════════════════════════════════
   INPUTS & SELECTS
════════════════════════════════ */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    background: #08111e !important;
    border: 1px solid #1a2d45 !important;
    border-radius: 8px !important;
    color: #c9d4e8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #00e5ff55 !important;
    box-shadow: 0 0 0 3px #00e5ff11 !important;
}
.stSelectbox > div > div {
    background: #08111e !important;
    border: 1px solid #1a2d45 !important;
    border-radius: 8px !important;
    color: #c9d4e8 !important;
}
.stSlider > div > div > div { background: #00e5ff !important; }
.stRadio > div { gap: 0.5rem; }
.stCheckbox > label > span { color: #7a92b8 !important; }

/* ════════════════════════════════
   AI RESPONSE BOX
════════════════════════════════ */
.ai-box {
    background: linear-gradient(135deg, #080f1e 0%, #0b1525 100%);
    border: 1px solid #1e3050;
    border-left: 3px solid #00e5ff;
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1.2rem;
    color: #b8ccdf;
    line-height: 1.8;
    font-size: 0.93rem;
    position: relative;
    overflow: hidden;
}
.ai-box::before {
    content: "";
    position: absolute; top: 0; right: 0;
    width: 200px; height: 200px;
    background: radial-gradient(circle, #00e5ff08 0%, transparent 70%);
    pointer-events: none;
}
.ai-box-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #1a2d45;
}
.ai-box-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #00e5ff;
}
.ai-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00e5ff;
    animation: pulse-dot 1.5s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

/* ════════════════════════════════
   SCORE BADGE
════════════════════════════════ */
.score-ring {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 110px; height: 110px;
    border-radius: 50%;
    border: 3px solid;
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 auto;
}
.score-high { border-color: #22c55e; color: #22c55e; background: #22c55e0d; }
.score-mid  { border-color: #f59e0b; color: #f59e0b; background: #f59e0b0d; }
.score-low  { border-color: #ef4444; color: #ef4444; background: #ef44440d; }

/* ════════════════════════════════
   HISTORY CARD
════════════════════════════════ */
.hist-card {
    background: #08111e;
    border: 1px solid #141f30;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.65rem;
    font-size: 0.83rem;
    color: #6a8090;
    transition: border-color 0.2s;
}
.hist-card:hover { border-color: #00e5ff33; color: #9ab0c8; }
.hist-cat {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #00e5ff;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.25rem;
}

/* ════════════════════════════════
   SECTION HEADER
════════════════════════════════ */
.sec-hdr {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #0e1e2e;
}
.sec-hdr-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: #e0eaf8;
}
.sec-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, #00e5ff22, transparent);
}

/* Mono tag */
.mono-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 0.15rem 0.55rem;
    border-radius: 4px;
    background: #00e5ff11;
    color: #00e5ff;
    border: 1px solid #00e5ff22;
}

/* Progress bar */
.prog-bar-wrap { margin: 0.3rem 0 0.8rem; }
.prog-label { display: flex; justify-content: space-between; font-size: 0.78rem; color: #5a7090; margin-bottom: 0.2rem; }
.prog-track { height: 6px; background: #0e1e30; border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #00b8cc, #00e5ff); }

/* Footer */
.footer-bar {
    text-align: center;
    color: #263545;
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #0e1e2e;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init():
    for k, v in {
        "history": [],
        "api_key": "",
        "groq_client": None,
        "total_generated": random.randint(2140, 2950),
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ─────────────────────────────────────────────────────────────────────────────
# GROQ HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_client():
    key = st.session_state.api_key.strip()
    if not key:
        return None
    if st.session_state.groq_client is None:
        st.session_state.groq_client = Groq(api_key=key)
    return st.session_state.groq_client

def llm(messages, temperature=0.8, max_tokens=1800):
    client = get_client()
    if not client:
        return "⚠️ **API key required.** Please enter your Groq API key in the sidebar to unlock all features."
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        st.session_state.total_generated += 1
        return r.choices[0].message.content
    except Exception as e:
        return f"❌ **Groq API Error:** {str(e)}"

def save_hist(cat, q, r):
    st.session_state.history.insert(0, {"cat": cat, "q": q[:90], "r": r[:300]})
    st.session_state.history = st.session_state.history[:20]

def render_response(title, content):
    st.markdown(f"""
    <div class="ai-box">
        <div class="ai-box-header">
            <div class="ai-dot"></div>
            <div class="ai-box-title">{title}</div>
            <span class="mono-tag">MARKETMIND AI</span>
        </div>
        <div>{content.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 MarketMind")
    st.markdown("*AI Sales & Marketing Intelligence*")
    st.divider()

    st.markdown("### 🔑 Groq API Key")
    api_in = st.text_input("", type="password", placeholder="gsk_...", label_visibility="collapsed", value=st.session_state.api_key)
    if api_in != st.session_state.api_key:
        st.session_state.api_key = api_in
        st.session_state.groq_client = None
    if st.session_state.api_key:
        st.success("✅ Connected to Groq")
    else:
        st.caption("Get a free key → console.groq.com")

    st.divider()
    st.markdown("### 🏢 Company Context")
    company_name   = st.text_input("Company / Brand Name", placeholder="e.g. TechNova Inc.")
    industry       = st.selectbox("Industry", [
        "SaaS / Software", "E-Commerce / Retail", "FinTech", "HealthTech",
        "EdTech", "Marketing Agency", "Manufacturing", "Real Estate",
        "Consulting", "Media & Entertainment", "Logistics", "Other"
    ])
    target_market  = st.selectbox("Target Market", ["B2B Enterprise", "B2B SMB", "B2C Mass Market", "B2C Niche", "B2B2C"])
    company_stage  = st.selectbox("Company Stage", ["Pre-Revenue / Startup", "Early-Stage (Seed)", "Growth (Series A/B)", "Scale-Up", "Enterprise"])

    st.divider()
    st.markdown("### 🎯 Campaign Defaults")
    default_tone   = st.selectbox("Default Tone", ["Professional", "Conversational", "Bold & Edgy", "Empathetic", "Data-Driven", "Inspirational"])
    default_budget = st.selectbox("Marketing Budget", ["Bootstrapped (<$5K)", "Small ($5K-$25K)", "Medium ($25K-$100K)", "Large ($100K-$500K)", "Enterprise ($500K+)"])

    st.divider()
    if st.button("🗑️ Clear All History"):
        st.session_state.history = []
        st.success("History cleared!")

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-grid"></div>
    <div class="hero-label">⚡ Generative AI · Sales & Marketing Intelligence Platform</div>
    <div class="hero-title">Market<span style="color:#00e5ff">Mind</span></div>
    <div class="hero-sub">Transform your go-to-market strategy with AI-generated campaigns, precision lead scoring, and real-time market intelligence — all powered by Groq LLMs.</div>
    <div class="hero-badges">
        <span class="hbadge">🤖 Groq LLM</span>
        <span class="hbadge">📣 Campaign Gen</span>
        <span class="hbadge">🎯 Lead Scoring</span>
        <span class="hbadge">💼 Pitch Builder</span>
        <span class="hbadge">📊 Market Intel</span>
        <span class="hbadge">💡 Biz Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Dashboard metrics
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("2,847+", "Campaigns Generated", "+12% this week"),
    ("94%",    "Pitch Conversion Rate", "+3.2% vs avg"),
    ("8.6/10", "Lead Score Accuracy",  "Model confidence"),
    ("180+",   "Markets Analyzed",     "Global coverage"),
    (str(st.session_state.total_generated), "Your Generations", "this session"),
]
for col, (num, label, delta) in zip([c1,c2,c3,c4,c5], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num">{num}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta">↑ {delta}</div>
        </div>""", unsafe_allow_html=True)

# Feature Cards
st.markdown("""
<div class="feat-grid">
    <div class="feat-card"><div class="feat-icon">📣</div><div class="feat-name">Campaign Generator</div><div class="feat-desc">Full multi-channel campaigns in seconds</div></div>
    <div class="feat-card"><div class="feat-icon">💼</div><div class="feat-name">Pitch Builder</div><div class="feat-desc">Personalized sales pitches that convert</div></div>
    <div class="feat-card"><div class="feat-icon">🎯</div><div class="feat-name">Lead Scorer</div><div class="feat-desc">AI-powered lead qualification & ranking</div></div>
    <div class="feat-card"><div class="feat-icon">📊</div><div class="feat-name">Market Analyst</div><div class="feat-desc">Competitive intel & market sizing</div></div>
    <div class="feat-card"><div class="feat-icon">💡</div><div class="feat-name">Biz Insights</div><div class="feat-desc">Data-driven strategic recommendations</div></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📣 Campaign Generator", "💼 Sales Pitch Builder", "🎯 Lead Scorer", "📊 Market Analyst", "💡 Business Insights", "📋 History"])

ctx = f"""Company: {company_name if company_name else 'the user company'} | Industry: {industry} | Market: {target_market} | Stage: {company_stage} | Tone: {default_tone} | Budget: {default_budget}"""

# ═══════════════════════════════════════════════════════════════
# TAB 1 — CAMPAIGN GENERATOR
# ═══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">📣 Campaign Generator</div><div class="sec-line"></div><span class="mono-tag">MULTI-CHANNEL</span></div>', unsafe_allow_html=True)
    st.markdown("*Generate complete, ready-to-launch marketing campaigns tailored to your brand and goals.*")

    r1c1, r1c2 = st.columns([2, 1])
    with r1c1:
        product      = st.text_area("Product / Service to Promote", placeholder="e.g. AI-powered project management tool that automates task assignment and deadline tracking for remote teams...", height=90)
        campaign_goal = st.text_input("Campaign Goal", placeholder="e.g. Generate 500 qualified leads in Q1, Drive 30% increase in free trial signups")
    with r1c2:
        channels     = st.multiselect("Marketing Channels", ["LinkedIn Ads", "Google Ads", "Email Marketing", "Instagram/Meta", "Twitter/X", "Content Marketing", "Webinar", "Cold Outreach", "SEO/Blog", "YouTube"], default=["LinkedIn Ads", "Email Marketing", "Content Marketing"])
        campaign_dur = st.selectbox("Campaign Duration", ["2-week Sprint", "1 Month", "1 Quarter", "6 Months", "Annual"])

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        usp         = st.text_input("Unique Selling Proposition", placeholder="e.g. 10x faster than competitors, 50% cost reduction")
    with r2c2:
        persona     = st.text_input("Target Persona", placeholder="e.g. VP of Engineering at 200-500 person SaaS companies")
    with r2c3:
        campaign_kpi = st.selectbox("Primary KPI", ["Leads Generated", "Revenue", "Brand Awareness", "Customer Acquisition", "Retention / Upsell", "App Installs"])

    incl_copy = st.checkbox("Include ad copy & creative briefs", value=True)
    incl_cal  = st.checkbox("Include content calendar", value=True)
    incl_budget_split = st.checkbox("Include budget allocation breakdown", value=True)

    if st.button("⚡ Generate Campaign", key="camp_btn"):
        if not product.strip():
            st.warning("Please describe your product or service.")
        else:
            channels_str = ", ".join(channels) if channels else "multi-channel"
            sys_p = f"""You are MarketMind, an elite AI marketing strategist with expertise in B2B/B2C demand generation, 
brand strategy, and performance marketing across all digital channels. You create campaigns that win awards and drive revenue.
Context: {ctx}"""
            usr_p = f"""Create a comprehensive {campaign_dur} marketing campaign for:

Product/Service: {product}
Campaign Goal: {campaign_goal if campaign_goal else 'Drive awareness and lead generation'}
Channels: {channels_str}
Target Persona: {persona if persona else 'Ideal customer profile'}
USP: {usp if usp else 'To be determined by AI'}
Primary KPI: {campaign_kpi}

Structure the campaign with these sections:
1. 🎯 Campaign Strategy & Positioning
2. 📌 Campaign Theme & Messaging Framework (Hero message, supporting messages, CTAs)
3. 📣 Channel-by-Channel Execution Plan (for each selected channel)
{"4. ✍️ Ad Copy & Creative Briefs (3 ad variations per key channel)" if incl_copy else ""}
{"5. 📅 Content Calendar (week-by-week breakdown)" if incl_cal else ""}
{"6. 💰 Budget Allocation Breakdown (% per channel with rationale)" if incl_budget_split else ""}
7. 📊 KPIs, Success Metrics & Measurement Framework
8. ⚠️ Risk Mitigation & Contingency Plan

Be specific, actionable, and include real-world tactics, tools, and benchmarks."""
            with st.spinner("🧠 MarketMind is crafting your campaign..."):
                out = llm([{"role":"system","content":sys_p},{"role":"user","content":usr_p}], temperature=0.82)
            render_response("📣 Your AI-Generated Campaign", out)
            save_hist("Campaign", product[:60], out)

# ═══════════════════════════════════════════════════════════════
# TAB 2 — SALES PITCH BUILDER
# ═══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">💼 Sales Pitch Builder</div><div class="sec-line"></div><span class="mono-tag">CONVERT & CLOSE</span></div>', unsafe_allow_html=True)
    st.markdown("*Build hyper-personalized sales pitches engineered to resonate with specific prospects.*")

    p1c1, p1c2 = st.columns([3, 2])
    with p1c1:
        prospect_name   = st.text_input("Prospect Name / Company", placeholder="e.g. John Smith, VP Sales at Acme Corp")
        prospect_pain   = st.text_area("Prospect's Pain Points / Challenges", placeholder="e.g. Their sales team spends 40% of time on manual data entry, missing quotas by 20%, poor CRM adoption...", height=100)
    with p1c2:
        pitch_type      = st.selectbox("Pitch Type", ["Cold Outreach Email", "LinkedIn Message", "Discovery Call Script", "Executive Presentation", "Proposal / Business Case", "Follow-Up Email", "Demo Script", "One-Pager"])
        deal_size       = st.selectbox("Deal Size", ["<$5K (Transactional)", "$5K–$25K (Commercial)", "$25K–$100K (Enterprise)", "$100K+ (Strategic)"])
        sales_stage     = st.selectbox("Sales Stage", ["Prospecting", "Discovery", "Demo / Evaluation", "Proposal", "Negotiation", "Closing"])

    p2c1, p2c2 = st.columns(2)
    with p2c1:
        prospect_industry = st.text_input("Prospect's Industry", placeholder="e.g. Financial Services, 500 employees")
        value_prop        = st.text_input("Key Value Proposition", placeholder="e.g. We reduce sales cycle by 35%")
    with p2c2:
        objections        = st.text_input("Likely Objections to Address", placeholder="e.g. price, timing, internal build vs buy")
        competition       = st.text_input("Competitive Context", placeholder="e.g. They're currently using Salesforce")

    urgency = st.slider("Urgency Level", 1, 10, 6, help="1 = Low pressure / nurturing, 10 = High urgency / closing")

    if st.button("🚀 Build Sales Pitch", key="pitch_btn"):
        if not prospect_pain.strip() and not prospect_name.strip():
            st.warning("Please fill in prospect details to generate a personalized pitch.")
        else:
            sys_p = f"""You are MarketMind's Sales Intelligence Engine — a world-class B2B sales strategist trained in SPIN Selling, 
Challenger Sale, MEDDIC, and Sandler methods. You craft pitches that open doors and close deals.
Context: {ctx}"""
            usr_p = f"""Create a high-converting {pitch_type} for:

Prospect: {prospect_name if prospect_name else 'Target Prospect'}
Prospect Industry: {prospect_industry if prospect_industry else 'Not specified'}
Pain Points: {prospect_pain if prospect_pain else 'General business challenges'}
Key Value Prop: {value_prop if value_prop else 'Our product/service'}
Deal Size: {deal_size}
Sales Stage: {sales_stage}
Objections to Address: {objections if objections else 'Price, timing, ROI'}
Competitive Context: {competition if competition else 'Status quo'}
Urgency Level: {urgency}/10

Deliver:
1. 🎯 Strategic Approach (why this angle works for this prospect)
2. 📝 The Pitch (full, word-for-word {pitch_type})
3. 💡 Personalization Hooks (specific triggers and proof points to use)
4. ❓ Discovery Questions (5 high-impact questions to uncover deeper needs)
5. 🛡️ Objection Handling Scripts (for each listed objection)
6. ➡️ Next Steps & Call-to-Action
7. 📊 Predicted Conversion Probability & Reasoning

Make it feel human, not scripted. Match the {default_tone} tone."""
            with st.spinner("🧠 Crafting your personalized pitch..."):
                out = llm([{"role":"system","content":sys_p},{"role":"user","content":usr_p}], temperature=0.78, max_tokens=2000)
            render_response(f"💼 {pitch_type} — Ready to Send", out)
            save_hist("Sales Pitch", f"{pitch_type}: {prospect_name}", out)

# ═══════════════════════════════════════════════════════════════
# TAB 3 — LEAD SCORER
# ═══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">🎯 Lead Scorer & Qualifier</div><div class="sec-line"></div><span class="mono-tag">AI SCORING</span></div>', unsafe_allow_html=True)
    st.markdown("*Enter lead details to get an AI-powered qualification score, priority ranking, and engagement strategy.*")

    l1c1, l1c2, l1c3 = st.columns(3)
    with l1c1:
        lead_name     = st.text_input("Lead Name", placeholder="e.g. Sarah Johnson")
        lead_title    = st.text_input("Job Title", placeholder="e.g. Chief Revenue Officer")
        lead_company  = st.text_input("Company", placeholder="e.g. GlobalTech Solutions")
    with l1c2:
        lead_industry = st.text_input("Industry", placeholder="e.g. SaaS, 1000-5000 employees")
        lead_revenue  = st.selectbox("Company Revenue", ["<$1M", "$1M–$10M", "$10M–$50M", "$50M–$200M", "$200M–$1B", "$1B+"])
        lead_location = st.text_input("Location / Region", placeholder="e.g. North America, Bay Area")
    with l1c3:
        lead_source   = st.selectbox("Lead Source", ["Inbound Website", "LinkedIn Organic", "Paid Ad Click", "Referral", "Event / Webinar", "Cold Outreach", "Partner Channel", "Product Signup"])
        lead_engage   = st.selectbox("Engagement Level", ["No engagement yet", "Opened 1 email", "Multiple email opens", "Downloaded content", "Attended webinar", "Requested demo", "Visited pricing page"])
        lead_timeline = st.selectbox("Buying Timeline", ["Unknown", "12+ months", "6-12 months", "3-6 months", "1-3 months", "Immediate / Active eval"])

    lead_notes = st.text_area("Additional Notes / Context", placeholder="e.g. Mentioned budget approved, currently evaluating 3 vendors, decision by end of quarter...", height=80)

    # Multi-lead batch option
    st.markdown("**— OR — Batch Score Multiple Leads**")
    batch_leads = st.text_area("Paste multiple leads (one per line: Name, Title, Company, Industry)", placeholder="Alice Chen, VP Marketing, FinServe Inc, FinTech\nBob Kumar, CTO, MedStart, HealthTech\nCarol Park, Head of Sales, RetailCo, E-Commerce", height=90)

    if st.button("🎯 Score This Lead", key="score_btn"):
        if not lead_name and not batch_leads:
            st.warning("Please enter at least a lead name or batch leads.")
        else:
            is_batch = bool(batch_leads.strip())
            sys_p = f"""You are MarketMind's Lead Intelligence Engine — an expert in BANT, MEDDIC, and predictive lead scoring. 
You analyze leads with the precision of a data scientist and the intuition of a veteran sales rep.
Context: {ctx}"""

            if is_batch:
                usr_p = f"""Score and rank these leads for {company_name if company_name else 'our company'} in {industry}:

{batch_leads}

For each lead provide:
- 🏆 Score (0-100) with letter grade (A/B/C/D)
- 🎯 Priority Tier (Hot / Warm / Cold / Disqualify)
- 💡 Key Qualification Signals
- ⚡ Recommended First Action
- ⏱️ Suggested Outreach Timing

Then provide: 📊 Batch Summary & Pipeline Forecast"""
            else:
                usr_p = f"""Perform a comprehensive lead scoring analysis for:

Lead: {lead_name} | {lead_title} | {lead_company}
Industry: {lead_industry} | Revenue: {lead_revenue} | Location: {lead_location}
Lead Source: {lead_source} | Engagement: {lead_engage} | Timeline: {lead_timeline}
Additional Context: {lead_notes if lead_notes else 'None'}

Deliver a full scoring report:
1. 🏆 Overall Lead Score (0–100) with detailed breakdown by dimension
2. 🎯 Qualification Tier (A-Hot / B-Warm / C-Nurture / D-Disqualify) with rationale
3. ✅ BANT Analysis (Budget / Authority / Need / Timeline scoring)
4. 💼 ICP Fit Analysis (Ideal Customer Profile match percentage)
5. ⚡ Engagement & Intent Signals Assessment
6. 🔮 Win Probability Estimate & Reasoning
7. 📋 Recommended Next Actions (prioritized, with specific messaging)
8. ⏱️ Optimal Contact Timing & Cadence
9. ⚠️ Risk Factors & Red Flags
10. 💰 Estimated Deal Value & Sales Cycle Length"""

            with st.spinner("🧠 Analyzing and scoring lead..."):
                out = llm([{"role":"system","content":sys_p},{"role":"user","content":usr_p}], temperature=0.6, max_tokens=1800)

            # Try to extract a score number for visual ring
            score_num = None
            for line in out.split('\n'):
                for w in line.split():
                    w_clean = w.strip('()[]/:')
                    if w_clean.isdigit() and 30 <= int(w_clean) <= 100:
                        score_num = int(w_clean)
                        break
                if score_num:
                    break

            if score_num is not None:
                if score_num >= 70:
                    ring_cls, grade = "score-high", "A"
                elif score_num >= 45:
                    ring_cls, grade = "score-mid", "B"
                else:
                    ring_cls, grade = "score-low", "C"
                sc1, sc2, sc3 = st.columns([1,1,3])
                with sc1:
                    st.markdown(f'<div style="display:flex;justify-content:center;padding:1rem 0"><div class="score-ring {ring_cls}">{score_num}<small style="font-size:0.7rem">/ 100</small></div></div>', unsafe_allow_html=True)
                with sc2:
                    dims = ["Company Fit","Engagement","Timeline","Authority","Budget"]
                    vals = [min(100,score_num + random.randint(-15,15)) for _ in dims]
                    for d,v in zip(dims,vals):
                        st.markdown(f'<div class="prog-bar-wrap"><div class="prog-label"><span>{d}</span><span>{v}%</span></div><div class="prog-track"><div class="prog-fill" style="width:{v}%"></div></div></div>', unsafe_allow_html=True)

            render_response("🎯 Lead Intelligence Report", out)
            save_hist("Lead Scorer", lead_name if lead_name else "Batch Leads", out)

# ═══════════════════════════════════════════════════════════════
# TAB 4 — MARKET ANALYST
# ═══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">📊 Market Intelligence Analyst</div><div class="sec-line"></div><span class="mono-tag">COMPETITIVE INTEL</span></div>', unsafe_allow_html=True)
    st.markdown("*Deep AI-powered market research, competitive analysis, and opportunity mapping.*")

    m1c1, m1c2 = st.columns([2, 1])
    with m1c1:
        market_topic = st.text_area("Market / Topic to Analyze", placeholder="e.g. AI-powered CRM software market for mid-market B2B SaaS companies in North America...", height=90)
        competitors  = st.text_input("Key Competitors to Include", placeholder="e.g. Salesforce, HubSpot, Pipedrive, Zoho CRM")
    with m1c2:
        analysis_type = st.selectbox("Analysis Type", [
            "Full Market Deep-Dive",
            "Competitive Landscape",
            "TAM / SAM / SOM Sizing",
            "SWOT Analysis",
            "Porter's Five Forces",
            "Go-to-Market Strategy",
            "Pricing Intelligence",
            "Customer Segment Analysis",
        ])
        geo_focus    = st.selectbox("Geographic Focus", ["Global", "North America", "Europe", "Asia-Pacific", "Latin America", "Middle East & Africa", "Specific Country"])

    m2c1, m2c2, m2c3 = st.columns(3)
    with m2c1: time_horizon = st.selectbox("Time Horizon", ["Current State (2024-25)", "1-Year Outlook", "3-Year Forecast", "5-Year Strategic"])
    with m2c2: depth_level  = st.selectbox("Report Depth", ["Executive Summary", "Standard Analysis", "Deep Research"])
    with m2c3: incl_opp     = st.checkbox("Include Opportunity Matrix", value=True)

    if st.button("🔍 Run Market Analysis", key="mkt_btn"):
        if not market_topic.strip():
            st.warning("Please describe the market or topic to analyze.")
        else:
            sys_p = f"""You are MarketMind's Market Intelligence Engine — a senior strategy consultant with expertise in 
market research, competitive analysis, and business strategy. You provide McKinsey-grade insights with startup execution clarity.
Context: {ctx}"""
            usr_p = f"""Conduct a {depth_level} {analysis_type} for:

Market/Topic: {market_topic}
Key Competitors: {competitors if competitors else 'Top players in this space'}
Geographic Focus: {geo_focus}
Time Horizon: {time_horizon}
Company Context: {company_name if company_name else 'Our company'} in {industry}, targeting {target_market}

Deliver a structured intelligence report with:
1. 📊 Executive Summary & Key Findings
2. 🌍 Market Overview (size, growth rate, key drivers & headwinds)
3. 🏆 Competitive Landscape (player positioning, strengths, weaknesses, market share estimates)
4. 👥 Customer Segmentation & Buying Behavior
5. 📈 Market Trends & Disruption Signals (3-5 major trends)
6. ⚙️ Technology & Innovation Landscape
{"7. 🎯 Opportunity Matrix (high-impact opportunities ranked by feasibility vs. potential)" if incl_opp else ""}
8. ⚠️ Risks, Barriers & Regulatory Considerations
9. 💡 Strategic Recommendations (5 actionable moves for {company_name if company_name else 'our company'})
10. 🔮 {time_horizon} Predictions & Scenario Planning

Use specific data points, percentages, and named examples wherever possible."""
            with st.spinner("🧠 Conducting market intelligence analysis..."):
                out = llm([{"role":"system","content":sys_p},{"role":"user","content":usr_p}], temperature=0.72, max_tokens=2200)
            render_response(f"📊 {analysis_type} — {market_topic[:50]}", out)
            save_hist("Market Analysis", market_topic[:60], out)

# ═══════════════════════════════════════════════════════════════
# TAB 5 — BUSINESS INSIGHTS
# ═══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">💡 Business Insights Engine</div><div class="sec-line"></div><span class="mono-tag">STRATEGIC AI</span></div>', unsafe_allow_html=True)
    st.markdown("*Get AI-generated strategic insights, growth recommendations, and data-driven decisions.*")

    # Quick insight prompts
    st.markdown("**⚡ Quick Insight Prompts:**")
    qi_cols = st.columns(4)
    quick_insights = [
        "How to improve our sales conversion rate?",
        "What pricing strategy should we use?",
        "How to reduce customer churn below 5%?",
        "Which market segment should we prioritize?",
    ]
    if "qi_val" not in st.session_state:
        st.session_state.qi_val = ""
    for i, (qc, qi) in enumerate(zip(qi_cols, quick_insights)):
        with qc:
            if st.button(f"💡 {qi[:28]}...", key=f"qi_{i}"):
                st.session_state.qi_val = qi

    insight_query = st.text_area(
        "Your business question or challenge",
        value=st.session_state.qi_val,
        placeholder="e.g. Our MRR growth has plateaued at $45K for 3 months. We have 120 customers, 70% in SMB, ACV $4,500. How should we break through?",
        height=110,
    )
    if st.session_state.qi_val:
        st.session_state.qi_val = ""

    i1c1, i1c2, i1c3 = st.columns(3)
    with i1c1: insight_type = st.selectbox("Insight Type", ["Growth Strategy", "Revenue Optimization", "Customer Success", "Product-Market Fit", "Pricing Strategy", "Sales Process", "Marketing ROI", "Churn Reduction", "Expansion Strategy", "Operational Efficiency"])
    with i1c2: data_context = st.text_input("Key Metrics / Data Points", placeholder="e.g. MRR $45K, 120 customers, CAC $1,200, LTV $8,400, NPS 42")
    with i1c3: urgency_level = st.selectbox("Decision Urgency", ["Strategic (Long-term)", "Tactical (1-6 months)", "Operational (Immediate)"])

    include_framework = st.checkbox("Apply strategic framework (OKRs, North Star, RICE, etc.)", value=True)
    include_scenarios  = st.checkbox("Include 3 scenario analysis (Best/Base/Worst case)", value=True)

    if st.button("💡 Generate Business Insights", key="insight_btn"):
        if not insight_query.strip():
            st.warning("Please enter your business question or challenge.")
        else:
            sys_p = f"""You are MarketMind's Business Intelligence Engine — a fractional CMO/CSO with 20+ years experience 
scaling B2B and B2C businesses from $0 to $100M+. You combine data analytics with strategic intuition to deliver 
actionable insights that directly impact revenue and growth.
Context: {ctx}"""
            usr_p = f"""Provide deep business insights for:

Question/Challenge: {insight_query}
Insight Type: {insight_type}
Key Metrics: {data_context if data_context else 'Not provided — use industry benchmarks'}
Urgency: {urgency_level}
Company: {company_name if company_name else 'Our company'} | {industry} | {target_market} | {company_stage}

Deliver a comprehensive insights report:
1. 🔍 Problem Diagnosis (root cause analysis, what the data tells us)
2. 🎯 Core Strategic Insight (the key unlock most businesses miss)
3. 💡 Top 5 Actionable Recommendations (prioritized by impact & effort)
4. 🗓️ 90-Day Action Plan (week-by-week execution roadmap)
{"5. 📊 Strategic Framework Application (OKRs, RICE scoring, or North Star metric)" if include_framework else ""}
{"6. 🔮 Scenario Analysis (Best Case / Base Case / Worst Case projections)" if include_scenarios else ""}
7. ⚡ Quick Wins (things you can do this week for immediate impact)
8. 📈 Expected Business Impact & Success Metrics
9. ⚠️ Common Pitfalls to Avoid
10. 🔗 Resources & Next Steps

Be brutally honest, data-driven, and specific. No generic advice."""
            with st.spinner("🧠 Generating strategic insights..."):
                out = llm([{"role":"system","content":sys_p},{"role":"user","content":usr_p}], temperature=0.75, max_tokens=2200)
            render_response(f"💡 {insight_type} — Strategic Insights", out)
            save_hist("Business Insights", insight_query[:60], out)

# ═══════════════════════════════════════════════════════════════
# TAB 6 — HISTORY
# ═══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec-hdr"><div class="sec-hdr-title">📋 Session History</div><div class="sec-line"></div><span class="mono-tag">RECENT ACTIVITY</span></div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("🔍 No activity yet. Start generating campaigns, pitches, and insights!")
    else:
        st.markdown(f"<p style='color:#3a5570;font-size:0.8rem;font-family:Space Mono,monospace'>{len(st.session_state.history)} INTERACTIONS THIS SESSION</p>", unsafe_allow_html=True)
        for item in st.session_state.history:
            with st.expander(f"[{item['cat']}] {item['q']}"):
                st.markdown(f'<div class="hist-card">{item["r"]}...</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    ⚡ MARKETMIND · POWERED BY GROQ LLM + LLAMA 3.3 · BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)
