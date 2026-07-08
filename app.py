import streamlit as st
import joblib
import re
import json
from pathlib import Path
import google.generativeai as genai

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="TruthLens AI",
    page_icon="📰",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

css = Path("assets/style.css").read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

# ==========================================
# GEMINI
# ==========================================

GEMINI_API_KEY = "AQ.Ab8RN6IdBM6n8iJ_i7XMrr8c1lxMF5OH3_4YZd5EuTz3OwbdSw"

genai.configure(api_key=GEMINI_API_KEY)

gemini = genai.GenerativeModel("gemini-2.5-flash")

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("📰 TruthLens AI")

    st.caption("AI Fake News Detection")

    st.divider()

    st.page_link(
        "app.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/History.py",
        label="📜 History"
    )

    st.page_link(
        "pages/Performance.py",
        label="📊 Model Performance"
    )

    st.page_link(
        "pages/About.py",
        label="ℹ About"
    )

    st.divider()

    st.write("### Project")

    st.write("Dataset")

    st.caption("Fake & Real News")

    st.write("Model")

    st.caption("TF-IDF + Logistic Regression")

    st.write("LLM")

    st.caption("Gemini 2.5 Flash")

    st.divider()

    st.caption("Version 1.0")

# ==========================================
# NAVBAR
# ==========================================

st.markdown("""
<div class='navbar'>

<div class='logo'>
📰 <b>TruthLens AI</b>
</div>

<div class='menu'>
Dashboard
&nbsp;&nbsp;&nbsp;&nbsp;
Detect
&nbsp;&nbsp;&nbsp;&nbsp;
Performance
&nbsp;&nbsp;&nbsp;&nbsp;
About
</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# MAIN LAYOUT
# ==========================================

left, right = st.columns([1.35, 1])

# ==========================================
# LEFT CARD
# ==========================================

with left:

    st.subheader("📰 AI Fake News Detector")

    st.write(
        "Paste a news article below and let TruthLens AI determine whether it is real or fake."
    )

    tab1, tab2 = st.tabs([
        "📄 Paste Text",
        "📁 Upload File"
    ])

    with tab1:

        news = st.text_area(
            "",
            height=320,
            placeholder="Paste your article here..."
        )

    with tab2:

        uploaded = st.file_uploader(
            "Upload TXT or PDF",
            type=["txt", "pdf"]
        )

    analyze = st.button(
        "🔍 Analyze News",
        use_container_width=True
    )

# ==========================================
# RIGHT CARD
# ==========================================

with right:

    prediction_placeholder = st.empty()

    confidence_placeholder = st.empty()

    trust_placeholder = st.empty()

    summary_placeholder = st.empty()

st.divider()

bottom_left, bottom_right = st.columns(2)

# ==========================================
# FEATURES
# ==========================================

with bottom_left:

    st.subheader("🚀 Features")

    st.success("✔ Machine Learning")

    st.success("✔ TF-IDF")

    st.success("✔ Logistic Regression")

    st.success("✔ Gemini AI")

    st.success("✔ Fake News Detection")

    st.success("✔ Explainable AI")

# ==========================================
# AI RESULT
# ==========================================

with bottom_right:

    explanation_placeholder = st.empty()

    verification_placeholder = st.empty()


# =====================================================
# ANALYZE
# =====================================================

if analyze:

    if news.strip() == "":
        st.warning("⚠️ Please enter a news article.")
        st.stop()

    # -----------------------------
    # Machine Learning Prediction
    # -----------------------------

    clean_news = clean_text(news)

    news_vector = vectorizer.transform([clean_news])

    prediction = model.predict(news_vector)[0]

    probability = model.predict_proba(news_vector)[0]

    confidence = float(max(probability) * 100)

    trust_score = int(confidence)

    # -----------------------------
    # Gemini
    # -----------------------------

    with st.spinner("🤖 Gemini is analyzing the article..."):

        prompt = f"""
You are TruthLens AI.

A Machine Learning model has predicted:

Prediction:
{"REAL NEWS" if prediction==1 else "FAKE NEWS"}

Confidence:
{confidence:.2f}%

Article:

{news}

Return ONLY valid JSON.

{{
"summary":"",
"neutral_language":0,
"source_reliability":0,
"evidence":0,
"sensational_language":0,
"logical_consistency":0,
"verification":"",
"explanation":""
}}

Rules

summary <=40 words

explanation <=120 words

verification <=1 sentence

Scores are integers 1-10

Return JSON only.
"""

        response = gemini.generate_content(prompt)

    try:

        text = response.text.strip()

        if text.startswith("```"):

            text = text.replace("```json", "")

            text = text.replace("```", "")

            text = text.strip()

        result = json.loads(text)

    except:

        st.error("Gemini returned invalid JSON")

        st.code(response.text)

        st.stop()

    # =====================================================
    # RIGHT PANEL
    # =====================================================

    with prediction_placeholder.container():

        st.subheader("🎯 Prediction")

        if prediction == 1:

            st.success("✅ REAL NEWS")

        else:

            st.error("❌ FAKE NEWS")

    with confidence_placeholder.container():

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        with c2:

            st.metric(
                "Trust Score",
                f"{trust_score}/100"
            )

    with summary_placeholder.container():

        st.subheader("📰 AI Summary")

        st.info(result["summary"])

        st.subheader("📊 Credibility Analysis")

        scores = {

            "Neutral Language":
            result["neutral_language"],

            "Source Reliability":
            result["source_reliability"],

            "Evidence":
            result["evidence"],

            "Sensational Language":
            result["sensational_language"],

            "Logical Consistency":
            result["logical_consistency"]

        }

        for title, score in scores.items():

            st.write(f"**{title}**")

            st.progress(score / 10)

            st.caption(f"{score}/10")

    with explanation_placeholder.container():

        st.subheader("🤖 AI Explanation")

        st.write(result["explanation"])

    with verification_placeholder.container():

        st.subheader("✅ Verification Recommendation")

        st.success(result["verification"])

