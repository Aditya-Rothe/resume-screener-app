import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(__file__))

from utils.extractor import extract_text_from_pdf, extract_text_from_input
from utils.matcher import compute_match_score, get_matched_keywords, get_score_feedback

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main { background-color: #0f0f13; }
    .block-container { padding: 2rem 3rem; }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.2rem;
        color: #f8f8f2;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: #9ca3af;
        margin-bottom: 2rem;
    }

    .section-card {
        background: #1a1a24;
        border: 1px solid #2a2a38;
        border-radius: 16px;
        padding: 1.6rem;
        margin-bottom: 1.2rem;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 0.6rem;
    }

    .score-badge {
        font-family: 'DM Serif Display', serif;
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
    }

    .score-label {
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
        margin-top: 0.4rem;
    }

    .keyword-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 3px;
    }

    .pill-match {
        background: #14532d;
        color: #86efac;
        border: 1px solid #22c55e44;
    }

    .pill-miss {
        background: #450a0a;
        color: #fca5a5;
        border: 1px solid #ef444444;
    }

    .tip-box {
        background: #1e1b4b;
        border-left: 3px solid #6366f1;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #c7d2fe;
        font-size: 0.9rem;
        margin-top: 1rem;
    }

    .stTextArea textarea {
        background: #12121a !important;
        color: #e2e8f0 !important;
        border: 1px solid #2a2a38 !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        cursor: pointer;
        transition: opacity 0.2s;
        margin-top: 0.5rem;
    }

    .stButton > button:hover { opacity: 0.88; }

    .stFileUploader {
        background: #12121a !important;
        border: 1px dashed #2a2a38 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stFileUploader"] {
        background: #12121a;
        border: 1px dashed #3a3a50;
        border-radius: 10px;
        padding: 1rem;
    }

    .stRadio label { color: #9ca3af !important; font-size: 0.9rem; }
    .stRadio div[role="radiogroup"] { gap: 0.5rem; }

    hr { border-color: #2a2a38; margin: 1.5rem 0; }

    h3 { color: #f8f8f2 !important; font-family: 'DM Serif Display', serif !important; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Resume Screener</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Paste a job description. Upload your resume. See how well you match — instantly.</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ── LEFT: Inputs ──────────────────────────────────────────────────────────────
with left:
    # Resume Input
    st.markdown('<div class="section-label">📄 Your Resume</div>', unsafe_allow_html=True)
    resume_input_type = st.radio(
        "Input method",
        ["Upload PDF", "Paste Text"],
        horizontal=True,
        label_visibility="collapsed"
    )

    resume_text = ""
    if resume_input_type == "Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            if resume_text and not resume_text.startswith("Error"):
                st.success(f"✅ Resume loaded — {len(resume_text.split())} words extracted")
            else:
                st.error(resume_text)
    else:
        resume_text = st.text_area(
            "Paste your resume text",
            height=220,
            placeholder="Paste your full resume content here...",
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # JD Input
    st.markdown('<div class="section-label">💼 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste job description",
        height=220,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

    analyze = st.button("⚡ Analyze Match")


# ── RIGHT: Results ────────────────────────────────────────────────────────────
with right:
    if analyze:
        if not resume_text or not jd_text:
            st.warning("Please provide both your resume and a job description.")
        else:
            with st.spinner("Analyzing..."):
                score = compute_match_score(resume_text, jd_text)
                keywords = get_matched_keywords(resume_text, jd_text)
                feedback = get_score_feedback(score)

            # ── Score Gauge ───────────────────────────────────────────────
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix': '%', 'font': {'size': 44, 'color': '#f8f8f2', 'family': 'DM Serif Display'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#4a4a6a', 'tickfont': {'color': '#9ca3af'}},
                    'bar': {'color': feedback['color'], 'thickness': 0.25},
                    'bgcolor': '#1a1a24',
                    'bordercolor': '#2a2a38',
                    'steps': [
                        {'range': [0, 30], 'color': '#1f0a0a'},
                        {'range': [30, 50], 'color': '#1f150a'},
                        {'range': [50, 75], 'color': '#1a1a0a'},
                        {'range': [75, 100], 'color': '#0a1f0a'},
                    ],
                    'threshold': {
                        'line': {'color': feedback['color'], 'width': 3},
                        'thickness': 0.8,
                        'value': score
                    }
                }
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#f8f8f2'},
                height=260,
                margin=dict(t=20, b=10, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Score label
            st.markdown(
                f'<div class="score-label" style="color:{feedback["color"]}">{feedback["label"]}</div>',
                unsafe_allow_html=True
            )

            # Tip box
            st.markdown(
                f'<div class="tip-box">💡 {feedback["suggestion"]}</div>',
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Keyword Stats ─────────────────────────────────────────────
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("JD Keywords", keywords['total_jd_keywords'])
            with col2:
                st.metric("Matched", keywords['match_count'], delta=f"{keywords['match_count']} found")
            with col3:
                st.metric("Missing", len(keywords['missing']), delta=f"-{len(keywords['missing'])}", delta_color="inverse")

            st.markdown("---")

            # ── Matched Keywords ──────────────────────────────────────────
            if keywords['matched']:
                st.markdown('<div class="section-label">✅ Matched Keywords</div>', unsafe_allow_html=True)
                pills_html = " ".join(
                    f'<span class="keyword-pill pill-match">{kw}</span>'
                    for kw in keywords['matched']
                )
                st.markdown(pills_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Missing Keywords ──────────────────────────────────────────
            if keywords['missing']:
                st.markdown('<div class="section-label">❌ Missing Keywords — Add These to Your Resume</div>', unsafe_allow_html=True)
                pills_html = " ".join(
                    f'<span class="keyword-pill pill-miss">{kw}</span>'
                    for kw in keywords['missing']
                )
                st.markdown(pills_html, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                    height:400px; color:#4a4a6a; text-align:center;">
            <div style="font-size:4rem; margin-bottom:1rem;">🎯</div>
            <div style="font-size:1.1rem; font-weight:600; color:#6366f1;">Your results will appear here</div>
            <div style="font-size:0.85rem; margin-top:0.5rem; color:#4a4a6a;">
                Upload your resume + paste a job description<br>then click Analyze Match
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#4a4a6a; font-size:0.8rem;">'
    'Built with Python • NLTK • Scikit-learn • Streamlit &nbsp;|&nbsp; '
    'Resume Screener — NLP Project'
    '</div>',
    unsafe_allow_html=True
)