import streamlit as st
from train_model import AnemiaPredictor
from visuals import Visualizer
from pdf_genarator import generate_medical_report
import random
import os

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HemoScan – Blood Analysis System",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg-base:        #060d14;
    --bg-card:        #0c1a26;
    --bg-card2:       #0f2236;
    --bg-input:       #0a1820;
    --accent-teal:    #00d4aa;
    --accent-cyan:    #00b4d8;
    --accent-green:   #39d353;
    --accent-red:     #ff4d6d;
    --accent-amber:   #ffb703;
    --text-primary:   #e8f4f8;
    --text-secondary: #7eb8d4;
    --text-muted:     #3d6878;
    --border:         #122333;
    --border-glow:    rgba(0, 212, 170, 0.25);
    --shadow-card:    0 8px 32px rgba(0,0,0,0.5);
    --radius:         12px;
    --radius-sm:      8px;
}

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-base) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,180,216,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 30% at 90% 90%, rgba(0,212,170,0.05) 0%, transparent 60%);
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Hero Banner ── */
.hemoscan-hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
}
.hemoscan-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,212,170,0.04) 0%, transparent 60%);
    pointer-events: none;
    border-radius: var(--radius);
}
.hemoscan-logo {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.75rem;
}
.hemoscan-logo .dot {
    width: 10px; height: 10px;
    background: var(--accent-teal);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent-teal);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.5; transform:scale(1.4); }
}
.hemoscan-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2rem, 5vw, 3.2rem) !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    background: linear-gradient(135deg, #ffffff 20%, var(--accent-teal) 60%, var(--accent-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    line-height: 1.1 !important;
}
.hemoscan-sub {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase;
    color: var(--accent-teal) !important;
    margin-top: 0.5rem !important;
    opacity: 0.9;
}
.hemoscan-tagline {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-top: 0.75rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-divider {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-teal), transparent);
    margin: 1.5rem auto 0;
    border-radius: 2px;
}

/* ── Section Headers ── */
h2, h3 {
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stHeader"],
.stHeader, h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase;
    color: var(--text-secondary) !important;
    padding: 0.5rem 0 !important;
    border: none !important;
}

/* ── Section Label Cards ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 1rem;
    background: var(--bg-card2);
    border-left: 3px solid var(--accent-teal);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin-bottom: 1.2rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-teal);
}
.section-label .icon { font-size: 1rem; }

/* ── Form Containers ── */
[data-testid="stForm"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 2rem !important;
    box-shadow: var(--shadow-card) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stForm"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-teal), var(--accent-cyan), transparent);
}

/* ── Input Labels ── */
label, [data-testid="stWidgetLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    margin-bottom: 0.25rem !important;
}

/* ── Text Inputs ── */
input[type="text"],
input[type="number"],
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type="text"]:focus,
input[type="number"]:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.12) !important;
    outline: none !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.12) !important;
}

/* ── Number Input Steppers ── */
[data-testid="stNumberInput"] button {
    background: var(--bg-card2) !important;
    border-color: var(--border) !important;
    color: var(--text-secondary) !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--accent-teal) !important;
    color: #000 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: var(--radius-sm) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

/* Primary Button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-teal) 0%, var(--accent-cyan) 100%) !important;
    color: #000 !important;
    border: none !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.85rem !important;
    box-shadow: 0 4px 20px rgba(0,212,170,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,212,170,0.5) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* Secondary Button */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--accent-teal) !important;
    border: 1px solid var(--accent-teal) !important;
    padding: 0.55rem 1.5rem !important;
    font-size: 0.8rem !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(0,212,170,0.08) !important;
    box-shadow: 0 0 16px rgba(0,212,170,0.2) !important;
}

/* Form Submit Button */
[data-testid="stFormSubmitButton"] > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: var(--bg-card2) !important;
    color: var(--accent-teal) !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--accent-teal) !important;
    color: #000 !important;
    box-shadow: 0 4px 20px rgba(0,212,170,0.35) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
/* Success */
[data-testid="stAlert"][data-baseweb="notification"][kind="success"],
div[data-testid="stAlert"] .st-success {
    background: rgba(57,211,83,0.1) !important;
    border-left: 3px solid var(--accent-green) !important;
    color: var(--accent-green) !important;
}
/* Error */
div[data-testid="stAlert"] .st-danger,
[data-testid="stAlert"][kind="error"] {
    background: rgba(255,77,109,0.1) !important;
    border-left: 3px solid var(--accent-red) !important;
}
/* Info */
[data-testid="stAlert"][kind="info"] {
    background: rgba(0,180,216,0.08) !important;
    border-left: 3px solid var(--accent-cyan) !important;
    color: var(--text-primary) !important;
}
/* Warning */
[data-testid="stAlert"][kind="warning"] {
    background: rgba(255,183,3,0.08) !important;
    border-left: 3px solid var(--accent-amber) !important;
    color: var(--accent-amber) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.25rem 1.5rem !important;
    transition: transform 0.2s, border-color 0.2s !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-teal), transparent);
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px) !important;
    border-color: var(--border-glow) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--accent-teal) !important;
    letter-spacing: 0.02em !important;
}

/* ── Divider ── */
hr, [data-testid="stDivider"] {
    border-color: var(--border) !important;
    opacity: 1 !important;
}

/* ── Container / Border ── */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.5rem !important;
    box-shadow: var(--shadow-card) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: var(--accent-teal) !important;
}
.stSpinner > div {
    border-top-color: var(--accent-teal) !important;
}

/* ── Images ── */
[data-testid="stImage"] img {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border) !important;
    transition: transform 0.3s, border-color 0.3s !important;
}
[data-testid="stImage"] img:hover {
    transform: scale(1.01) !important;
    border-color: var(--border-glow) !important;
}

/* ── Caption / Write ── */
[data-testid="stCaptionContainer"],
.stCaption {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    text-align: center !important;
    font-style: italic !important;
}

/* ── st.write outputs ── */
[data-testid="stMarkdownContainer"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--text-primary) !important;
    line-height: 1.6 !important;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, rgba(0,212,170,0.15), rgba(0,180,216,0.15)) !important;
    color: var(--accent-teal) !important;
    border: 1px solid var(--accent-teal) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1.75rem !important;
    transition: all 0.25s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, var(--accent-teal), var(--accent-cyan)) !important;
    color: #000 !important;
    box-shadow: 0 6px 24px rgba(0,212,170,0.4) !important;
    transform: translateY(-2px) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--text-muted);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-teal); }

/* ── Columns gap ── */
[data-testid="stHorizontalBlock"] {
    gap: 1.25rem !important;
}

/* ── Report section headers (custom HTML divs) ── */
.report-header {
    background: linear-gradient(135deg, #0f2236 0%, #0c1a26 100%);
    padding: 1rem 1.5rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-cyan);
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.report-header::after {
    content: '';
    position: absolute;
    right: -20px; top: -20px;
    width: 80px; height: 80px;
    background: radial-gradient(circle, rgba(0,212,170,0.08), transparent);
    border-radius: 50%;
}
.report-header h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--accent-cyan) !important;
    margin: 0 !important;
}

/* ── Status badge for st.write outputs ── */
.status-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0;
    font-size: 0.92rem;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
}
.status-row:last-child { border-bottom: none; }
.badge {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    background: rgba(0,212,170,0.15);
    color: var(--accent-teal);
    border: 1px solid rgba(0,212,170,0.3);
}

/* ── Responsive spacing ── */
.block-container {
    max-width: 1200px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}

/* ── Footer ── */
.hemoscan-footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}
.hemoscan-footer span { color: var(--accent-teal); }
</style>
""", unsafe_allow_html=True)

# ─── Hero Banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hemoscan-hero">
    <div class="hemoscan-logo">
        <span class="dot"></span>
        <span style="font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;
                     letter-spacing:0.25em;text-transform:uppercase;color:#7eb8d4;">
            CLINICAL DIAGNOSTICS
        </span>
        <span class="dot"></span>
    </div>
    <h1 class="hemoscan-title">HemoScan</h1>
    <p class="hemoscan-sub">Blood Analysis System — Powered by Oiron</p>
    <p class="hemoscan-tagline">AI-driven complete blood count interpretation &amp; anemia classification</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
if "user_submitted" not in st.session_state:
    st.session_state.user_submitted = False
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ─── User Details Form ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label"><span class="icon">👤</span> Patient Information</div>', unsafe_allow_html=True)

with st.form("user_form"):
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    submit_user = st.form_submit_button("Save Patient Details")

    if submit_user:
        if name == "" or age == 0 or gender == "":
            st.error("Please fill in all details")
            submit_user = False
            st.session_state.user_submitted = False
        else:
            st.session_state.user_submitted = True
            st.success("Patient details saved successfully.")

# ─── Blood Parameters Form ───────────────────────────────────────────────────────
if "blood_submitted" not in st.session_state:
    st.session_state.blood_submitted = False

st.markdown('<div class="section-label" style="margin-top:2rem;"><span class="icon">🩸</span> CBC Blood Parameters</div>', unsafe_allow_html=True)

with st.form("blood_form"):
    col1, col2 = st.columns(2)
    with col1:
        hb = st.number_input("Hemoglobin (Hb)")
    with col2:
        hb_unit = st.selectbox("Hb Unit", ["g/dL", "g/L"])

    col3, col4 = st.columns(2)
    with col3:
        mch = st.number_input("MCH")
    with col4:
        mch_unit = st.selectbox("MCH Unit", ["pg", "fg"])

    col5, col6 = st.columns(2)
    with col5:
        mchc = st.number_input("MCHC")
    with col6:
        mchc_unit = st.selectbox("MCHC Unit", ["g/dL", "g/L"])

    col7, col8 = st.columns(2)
    with col7:
        mcv = st.number_input("MCV")
    with col8:
        mcv_unit = st.selectbox("MCV Unit", ["fL"])

    submit_blood = st.form_submit_button("Submit Blood Values")

    if submit_blood:
        if hb == 0 or mch == 0 or mchc == 0 or mcv == 0:
            st.error("Please enter all blood values")
            submit_blood = False
            st.session_state.blood_submitted = False
        else:
            st.session_state.blood_submitted = True
            st.success("Blood values submitted successfully.")

# ─── Unit Conversion ─────────────────────────────────────────────────────────────
def convert_to_standard(hb, hb_unit, mch, mch_unit, mchc, mchc_unit, mcv, mcv_unit):
    if hb_unit == "g/L":
        hb = hb / 10
    if mch_unit == "fg":
        mch = mch / 1000
    if mchc_unit == "g/L":
        mchc = mchc / 10
    if mcv_unit == "L":
        mcv = mcv * 1e15
    return hb, mch, mchc, mcv

if submit_blood:
    hb, mch, mchc, mcv = convert_to_standard(
        hb, hb_unit, mch, mch_unit, mchc, mchc_unit, mcv, mcv_unit
    )

    st.markdown("""
    <div style="background:var(--bg-card2);border:1px solid var(--border);border-radius:var(--radius);
                padding:1.25rem 1.5rem;margin-top:1rem;">
        <p style="font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:700;
                  letter-spacing:0.18em;text-transform:uppercase;color:var(--text-muted);
                  margin-bottom:0.75rem;">Standardised Values (SI Units)</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("Values processed & standardised successfully.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hb", f"{hb:.2f} g/dL")
    c2.metric("MCH", f"{mch:.2f} pg")
    c3.metric("MCHC", f"{mchc:.2f} g/dL")
    c4.metric("MCV", f"{mcv:.2f} fL")

# ─── Predict Button ──────────────────────────────────────────────────────────────
if st.session_state.user_submitted and st.session_state.blood_submitted:
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🔬  Run Anemia Analysis", type="primary"):
        with st.spinner("Running diagnostic analysis…"):
            prediction = AnemiaPredictor()
            result = prediction.predict(gender, hb, mch, mchc, mcv)
            st.session_state.prediction_result = result

            visual = Visualizer(gender, hb, mch, mchc, mcv)
            visual.pipline_visual()

# ─── Results Panel ───────────────────────────────────────────────────────────────
if st.session_state.prediction_result is not None:
    result = st.session_state.prediction_result

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.divider()

    with st.container(border=True):
        st.markdown("""
        <div class="report-header">
            <h3>🧬 &nbsp; Anemia Prediction Report</h3>
        </div>
        """, unsafe_allow_html=True)
        print(result)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label ="Diagnosis", value=result["Diagnosis"])

        with col2:
            st.metric(label="Risk Probability", value=result["Risk"])
        with col3:
            st.metric(label="Type", value=result["Type"])

        st.info(f"💡  Recommendation: {result['Recommendation']}")

        st.divider()

        # ── Visual Analysis ──
        st.markdown("""
        <div class="report-header">
            <h3>📊 &nbsp; Blood Report Visual Analysis</h3>
        </div>
        """, unsafe_allow_html=True)

        try:
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.image("reports/cbc_comparison_chart.png",
                             caption="CBC Parameter Comparison", width='stretch')
                    st.caption("Comparison of patient CBC values against normal reference ranges.")
                with col2:
                    st.image("reports/cbc_radar_chart.png",
                             caption="CBC Radar Analysis", width='stretch')
                    st.caption("Radar visualization highlighting deviations in blood parameters.")

                st.divider()
                st.image("reports/hemoglobin_risk_indicator.png",
                         caption="Hemoglobin Risk Indicator", width='stretch')
                st.caption("Visual indicator showing hemoglobin level relative to anemia risk thresholds.")

        except FileNotFoundError:
            st.error("Visual analysis not available. Please ensure the model generates these visualisations.")

else:
    st.warning("⚠️  Please submit both Patient Details and Blood Parameters to proceed with analysis.")

# ─── PDF Report Generator ────────────────────────────────────────────────────────
if st.session_state.prediction_result is not None:
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    if st.button("📄  Generate Full Medical Report", type="secondary"):
        with st.spinner("Generating PDF report…"):
            patient_id = "patient_" + str(random.randint(10000, 99999))
            file_path = f"reports/{patient_id}_report.pdf"
            generate_medical_report(
                patient_id=patient_id, name=name, age=age, gender=gender,
                hb=hb, mch=mch, mchc=mchc, mcv=mcv,
                prediction=st.session_state.prediction_result["Diagnosis"],
                risk=st.session_state.prediction_result["Risk"],
                anemia_type=st.session_state.prediction_result["Recommendation"]
            )
            st.success("PDF report generated successfully!")

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️  Download Report",
                    data=f,
                    file_name=f"{patient_id}_report.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Error: Report file not found.")

# ─── Model Probability Panel ─────────────────────────────────────────────────────
if "model_probability" not in st.session_state:
    st.session_state.model_probability = False

if st.session_state.prediction_result is not None:
    st.divider()
    st.session_state.model_probability = st.button("📈  View Model Probability Details", type="secondary")
    st.session_state.model_probability = True if st.session_state.model_probability else False

if st.session_state.model_probability:
    st.markdown("""
    <div class="report-header" style="margin-top:1rem;">
        <h3>🤖 &nbsp; Model Probability Details</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        col1, col2 = st.columns(2)
        try:
            with col1:
                st.image("reports/prediction_probability.png",
                         caption="Model Probability Distribution", width='stretch')
                st.caption("Distribution of predicted probabilities for each anemia type.")
            with col2:
                st.image("reports/feature_importance.png",
                         caption="Feature Importance", width='stretch')
                st.caption("Importance of each feature in the model's prediction.")

            if st.button("✕  Hide Probability Details", type="secondary"):
                st.session_state.model_probability = False
        except FileNotFoundError:
            st.error("Probability details not available. Please ensure the model generates these visualisations.")

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hemoscan-footer">
    <span>HemoScan</span> · Blood Analysis System &nbsp;|&nbsp; Powered by Oiron &nbsp;|&nbsp;
    AI diagnostic tool — not a substitute for professional medical advice.
</div>
""", unsafe_allow_html=True)