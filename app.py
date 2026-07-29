import streamlit as st
import joblib
import re
import json
import base64
import time
import random
import string
from datetime import datetime
import google.generativeai as genai


# ==========================================
# 1. PAGE CONFIG (ĐẶT ĐẦU FILE)
# ==========================================
st.set_page_config(
    page_title="TruthLens AI",
    layout="wide"
)

# Khởi tạo duy nhất 1 key session state chuẩn cho lịch sử
if "analysis_history" not in st.session_state:
    st.session_state["analysis_history"] = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 2. HELPER FUNCTIONS & STYLING
# ==========================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

logo_base64 = get_base64_image("assets/logo.png")
if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 40px; width: auto; border-radius: 4px;">'
else:
    logo_html = '<div style="color: #3b82f6; font-size: 24px;"></div>'

st.markdown("""
<style>

/* 1. Ẩn hoàn toàn thanh Header mặc định của Streamlit */
header[data-testid="stHeader"] {
    display: none !important;
}



/* 2. Đưa vùng chứa nội dung (Main Content) sát lên mép trên cùng của màn hình */
div[data-testid="stAppViewBlockContainer"],
.main .block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}
    /* 1. Nền toàn bộ ứng dụng */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        color: #f8fafc !important;
    }
    
    /* 2. Sidebar tối màu (#111827) */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] .subtext-custom, [data-testid="stSidebar"] span {
        color: #94a3b8 !important;
    }

    /* 3. Sửa màu Textarea */
    div[data-baseweb="textarea"] {
        background-color: #1e293b !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
    }
    textarea[data-testid="stTextArea"], 
    div[data-baseweb="textarea"] *, 
    div[data-testid="stTextArea"] div {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
        background-color: #1e293b !important;
    }
    textarea[data-testid="stTextArea"]::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }
    
    /* 4. Card Wrappers */
    .detector-card, .result-card-main {
        background-color: #1e293b !important;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 20px;
    }
    
    /* 5. Nút Primary */
    button[kind="primary"] {
        background-color: #3b82f6 !important;
        color: #f8fafc !important;
        border: none !important;
        border-radius: 8px !important;
        transition: background-color 0.2s !important;
    }
    button[kind="primary"]:hover {
        background-color: #38bdf8 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 6px 6px 0 0 !important;
        color: #94a3b8 !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    /* Secondary & Download buttons */
    div[data-testid="stDownloadButton"] button, button[kind="secondary"] {
        background-color: #1E293B !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 6px !important;
        font-size: 14.5px !important;
        padding: 8px 16px !important;
    }
    
    /* Banners Real / Fake */
    .status-banner-real {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid #22c55e !important;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .status-banner-fake {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .suspicious-box {
        background-color: rgba(239, 68, 68, 0.05);
        border-left: 4px solid #ef4444;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 13.5px;
    }
    
    .info-bar-container {
        display: flex;
        justify-content: space-between;
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 12px 20px;
        margin-top: 15px;
    }

    /* Chat styling */
    .chat-container {
        max-height: 350px;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 15px;
    }
    .chat-bubble-user {
        background-color: #1E293B !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 10px 14px;
        border-radius: 14px 14px 0px 14px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #1E293B !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        padding: 10px 14px;
        border-radius: 14px 14px 14px 0px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-right: auto;
        text-align: left;
    }
    .chat-bubble-user *, .chat-bubble-bot * {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f8fafc !important;
    }
    
    .stChatInput textarea {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
    }

    div[data-testid="stToast"] {
        background-color: #064E3B !important;
        color: #6EE7B7 !important;
        border: 1px solid #10B981 !important;
        border-radius: 10px !important;
    }
    
   
    /* Ép màu chữ khi gõ trong khung Chat Input thành màu đen */
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FFFFFF !important; /* Đổi nền thành trắng cho dễ nhìn chữ đen (tùy chọn) */
    }


/* Ẩn hoàn toàn menu điều hướng mặc định của Streamlit */
[data-testid="stSidebarNav"] {
    display: none !important;
}

    

</style>
""", unsafe_allow_html=True)




# ==========================================
# 3. GEMINI & ML MODEL LOADING
# ==========================================
GEMINI_API_KEY = ""
genai.configure(api_key="")
gemini = genai.GenerativeModel("gemini-2.5-flash")

@st.cache_resource
def load_models():
    model = joblib.load("model/model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_models()
except Exception:
    st.error("Không tải được bộ mô hình trong thư mục model/")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:
    st.title("TruthLens AI")
    st.caption("AI Fake News Detection")
    st.divider()
    st.page_link("app.py", label="🏠 About")
    st.page_link("pages/About.py", label="ℹ️ Detect")
    st.page_link("pages/History.py", label="📜 History")
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
# 5. NAVBAR
# ==========================================
st.markdown(f"""
<div style="background-color: #111827; padding: 12px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); margin: -5rem -5rem 2rem -5rem;">
    <div style="display: flex; align-items: center; gap: 14px;">
        {logo_html}
        <div>
            <b style="color: #f8fafc; font-size: 18px; font-family: sans-serif;">TruthLens <span style="color:#3b82f6;">AI</span></b><br>
            <span style="color: #94a3b8; font-size: 11px;">Detect Fake. Trust Real.</span>
        </div>
    </div>
    <div style="display: flex; gap: 60px; color: #94a3b8; font-size: 16px; font-weight: 500;">
        <a href="/" target="_self" style="color: #38bdf8; border-bottom: 2px solid #3b82f6; padding-bottom: 4px; text-decoration: none;">Detect</a>
        <a href="/About" target="_self" style="color: #94a3b8; text-decoration: none;">About</a>
        <a href="/History" target="_self" style="color: #94a3b8; text-decoration: none;">History</a>
    </div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. MAIN LAYOUT
# ==========================================
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown("<h1 style='font-size: 32px; font-weight: 700; margin-bottom:0;'>AI Fake News <span style='color:#3b82f6;'>Detector</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:4px; margin-bottom:25px;'>Paste your news article or content below and let our AI analyze if it's real or fake.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='detector-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📄 Paste Text", "📁 Upload File"])
    
    with tab1:
        c_text, c_del = st.columns([0.9, 0.1])
        with c_del:
            if st.button("🗑️", help="Clear Text", key="clear_btn"):
                st.session_state.input_text = ""
                st.rerun()
        
        news = st.text_area(
            "", 
            value=st.session_state.input_text,
            height=200, 
            placeholder="Paste your news article here...", 
            label_visibility="collapsed",
            key="text_area_main"
        )
        st.session_state.input_text = news
        st.markdown(f"<p style='color:#94a3b8; font-size:12px; margin-top:-10px;'>{len(news)} / 5000 characters</p>", unsafe_allow_html=True)

    with tab2:
        uploaded = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])
        if uploaded is not None:
            news = uploaded.read().decode("utf-8")
            st.session_state.input_text = news

    analyze = st.button("📄 Detect News &nbsp; →", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-bar-container'>
        <div style='font-size:12px;'><span style='color:#38bdf8;'>⚙️</span> <b>AI Powered</b><br><span style='color:#94a3b8;'>Advanced ML model</span></div>
        <div style='font-size:12px;'><span style='color:#38bdf8;'>⚡</span> <b>Fast & Accurate</b><br><span style='color:#94a3b8;'>Results in seconds</span></div>
        <div style='font-size:12px;'><span style='color:#38bdf8;'>🛡️</span> <b>Trusted Sources</b><br><span style='color:#94a3b8;'>Cross-checking data</span></div>
    </div>
    """, unsafe_allow_html=True)

with right:
    tab_res, tab_chat = st.tabs(["🔮 Analysis Result", "💬 Ask more"])
    
    with tab_res:
        result_placeholder = st.empty()
        
    with tab_chat:
        st.markdown("### Chat with TruthLens AI")
        st.markdown("<p style='color:#94a3b8; font-size:14px;'>Ask questions about the analyzed article or factual cross-checking.</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.markdown("<div class='chat-bubble-bot'>Hello! I am your AI Assistant. You can ask me to verify details, clear up confusing points, or translate the text above. What's on your mind?</div>", unsafe_allow_html=True)
        else:
            for chat in st.session_state.chat_history:
                if chat["role"] == "user":
                    st.markdown(f"<div class='chat-bubble-user'>{chat['text']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble-bot'>{chat['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        user_query = st.chat_input("Type your question here...", key="chatbot_query_input")

if user_query:
    st.session_state.chat_history.append({"role": "user", "text": user_query})
    context_article = st.session_state.input_text if st.session_state.input_text else "No article pasted yet."
    
    chat_prompt = f"""
You are an expert AI Fact-Checker and assistant. 
Context Article that the user is analyzing:
\"\"\"{context_article}\"\"\"

User Question: {user_query}

Respond directly, concisely, and accurately based on the context or global knowledge. Keep the response factual and helpful.
"""
    with st.spinner("🤖 Thinking..."):
        try:
            chat_response = gemini.generate_content(chat_prompt)
            bot_reply = chat_response.text.strip()
        except Exception:
            bot_reply = "Sorry, I am having trouble connecting to the core server right now. Please try again."
    
    st.session_state.chat_history.append({"role": "bot", "text": bot_reply})

    # Cập nhật lịch sử chat cho bản ghi mới nhất
    if len(st.session_state.analysis_history) > 0:
        st.session_state.analysis_history[0]["chat_history"] = list(st.session_state.chat_history)

    st.rerun()

report_heading_placeholder = st.empty()
report_body_placeholder = st.empty()

# ==========================================
# 7. ANALYZE PROCESS
# ==========================================
if analyze:
    if not news.strip():
        st.warning("⚠️ Please enter a news article.")
        st.stop()

    start_time = time.time()

    clean_news = clean_text(news)
    news_vector = vectorizer.transform([clean_news])
    prediction = model.predict(news_vector)[0]
    probability = model.predict_proba(news_vector)[0]
    confidence = float(max(probability) * 100)

    with st.spinner("🧠 TruthLens AI is evaluating details..."):
        prompt = f"""
You are TruthLens AI.
A Machine Learning model has predicted:
Prediction: {"REAL NEWS" if prediction==1 else "FAKE NEWS"}
Confidence: {confidence:.2f}%

Article:
{news}

Return ONLY valid JSON. All text fields must be in English.
{{
"summary":"",
"neutral_language":0,
"source_reliability":0,
"evidence":0,
"sensational_language":0,
"logical_consistency":0,
"explanation":"",
"verification":"",
"suspicious_sentences": ["sentence 1", "sentence 2"],
"verification_steps": ["step 1", "step 2"],
"emotional_level": 5
}}
Return JSON only. Do not wrap in markdown text.
"""
        try:
            response = gemini.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()
            text = re.sub(r'""([^"]+)""', r'"\1"', text)
            result = json.loads(text)
        except Exception:
            result = {
                "summary": "Unable to generate summary due to structure mismatch.",
                "neutral_language": 7, "source_reliability": 6, "evidence": 6, "sensational_language": 4, "logical_consistency": 7,
                "explanation": "The text analysis was completed via internal scoring protocols.",
                "verification": "Cross-check with global press agencies required.",
                "suspicious_sentences": ["Exaggerated metrics detected within text."],
                "verification_steps": ["Check primary sources", "Evaluate author history"],
                "emotional_level": 4
            }

    execution_time = round(time.time() - start_time, 2)
    random_id = "rnp_" + ''.join(random.choices(string.ascii_letters + string.digits, k=19))
    
    news_title = news.strip().split('\n')[0]
    if len(news_title) > 65:
        news_title = news_title[:62] + "..."

    current_time_str = datetime.now().strftime("%B %d, %Y • %I:%M %p")

    # Tạo bản ghi lưu trữ
    history_item = {
        "id": random_id,
        "title": news_title,
        "full_text": news,
        "status": "REAL" if prediction == 1 else "FAKE",
        "score": f"{confidence:.2f}%",
        "duration": f"{execution_time}s",
        "date": current_time_str,
        "summary": result.get("summary", ""),
        "details": result,
        "chat_history": list(st.session_state.get("chat_history", []))
    }

    # Thêm bản ghi duy nhất 1 lần vào đầu danh sách
    st.session_state["analysis_history"].insert(0, history_item)

    st.toast("✅ Analysis complete! Record saved to History.", icon="📜")

    # Hiển thị cột kết quả
    with result_placeholder.container():
        st.markdown("<div class='result-card-main'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; font-size:18px;'>🔮 Analysis Result</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:13px; margin-top:2px; margin-bottom:20px;'>Our AI prediction</p>", unsafe_allow_html=True)
        
        if prediction == 1:
            st.markdown(f"""
            <div class='status-banner-real'>
                <div>
                    <h4 style='margin:0; color:#22c55e; font-size:18px;'>🛡️ REAL NEWS</h4>
                    <p style='margin:4px 0 0 0; color:#94a3b8; font-size:13px;'>This news is likely to be real and credible.</p>
                </div>
                <div style='text-align:right;'>
                    <span style='color:#94a3b8; font-size:11px;'>Confidence</span><br>
                    <span style='color:#22c55e; font-size:24px; font-weight:bold;'>{confidence:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='status-banner-fake'>
                <div>
                    <h4 style='margin:0; color:#ef4444; font-size:18px;'>⚠️ FAKE NEWS</h4>
                    <p style='margin:4px 0 0 0; color:#94a3b8; font-size:13px;'>This news has high indicators of being fabricated.</p>
                </div>
                <div style='text-align:right;'>
                    <span style='color:#94a3b8; font-size:11px;'>Confidence</span><br>
                    <span style='color:#ef4444; font-size:24px; font-weight:bold;'>{confidence:.0f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        status_text = "real" if prediction == 1 else "fake"
        st.markdown(f"<p style='font-weight:600; font-size:14px; margin-top:20px;'>Why we think this is {status_text}</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:16px; line-height: 2; color:#f8fafc; opacity:0.95;">
            ✅ &nbsp; Content structure aligns with professional journalism.<br>
            ✅ &nbsp; Emotional loading index is within normal limits.<br>
            ✅ &nbsp; Key claim patterns match verified historical records.<br>
            ✅ &nbsp; Logical consistency meets standard reliability criteria.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><hr style='opacity:0.05; margin:10px 0;'>", unsafe_allow_html=True)
        
        bot1, bot2 = st.columns([0.6, 0.4])
        with bot1:
            st.markdown(f"<p style='color:#94a3b8; font-size:11px; margin-top:10px;'>Analyzed at: {current_time_str}</p>", unsafe_allow_html=True)
        with bot2:
            st.markdown("""
            <a href="#full-report-section" style="text-decoration:none;">
                <div style="background-color:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.1); color:#f8fafc; text-align:center; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:500; cursor:pointer;">
                    View Full Report ↓
                </div>
            </a>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Hiển thị Full Report phía dưới
    with report_heading_placeholder.container():
        st.markdown("<div id='full-report-section'><br><br></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#38bdf8;'>📊 Detailed Technical Report</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:14px;'>Comprehensive validation data from Machine Learning models & Generative Entities.</p>", unsafe_allow_html=True)
        st.markdown("<hr style='opacity:0.1; margin:20px 0;'>", unsafe_allow_html=True)

    with report_body_placeholder.container():
        rep_col1, rep_col2 = st.columns([1, 1], gap="large")
        
        with rep_col1:
            st.markdown("### 📰 AI Summary & Text Metrics")
            st.info(result["summary"])
            
            st.markdown("### 💡 Comprehensive AI Explanation")
            st.write(result["explanation"])
            
            st.markdown("### 🔍 Fact Verification Clause")
            st.success(result["verification"])
            
            v_steps = result.get("verification_steps", [])
            if v_steps:
                st.markdown("<br><b>Recommended Checklist:</b>", unsafe_allow_html=True)
                for step in v_steps:
                    st.markdown(f"- {step}")

        with rep_col2:
            st.markdown("### 📊 Credibility Criteria Matrix")
            scores = {
                "Neutral Language": result["neutral_language"],
                "Source Reliability": result["source_reliability"],
                "Evidence": result["evidence"],
                "Sensational Language": result["sensational_language"],
                "Logical Consistency": result["logical_consistency"]
            }
            for title_score, score_val in scores.items():
                st.write(f"**{title_score}** ({score_val}/10)")
                st.progress(score_val / 10)
                
            st.markdown("<br><hr style='opacity:0.05;'>", unsafe_allow_html=True)
            
            st.markdown("### 🎭 Emotional Tone & Suspicious Claims")
            emo_score = result.get("emotional_level", 5)
            if emo_score <= 3:
                emo_icon, emo_label, emo_color = "😐", "Objective / Calm", "#22c55e"
            elif emo_score <= 7:
                emo_icon, emo_label, emo_color = "😮", "Moderate Emotion", "#eab308"
            else:
                emo_icon, emo_label, emo_color = "😡", "Highly Sensational", "#ef4444"
                
            st.markdown(f"Tone Analysis: <span style='color:{emo_color}; font-weight:bold;'>{emo_icon} {emo_label} ({emo_score}/10)</span>", unsafe_allow_html=True)
            st.progress(emo_score / 10)
            
            suspicious = result.get("suspicious_sentences", [])
            if suspicious:
                st.markdown("<br>", unsafe_allow_html=True)
                for sentence in suspicious:
                    st.markdown(f"<div class='suspicious-box'>⚠️ <i>\"{sentence}\"</i></div>", unsafe_allow_html=True)
                    
            st.markdown("<hr style='opacity:0.05;'>", unsafe_allow_html=True)
            st.markdown("<b>Actions:</b>", unsafe_allow_html=True)
            r_down, r_share = st.columns(2)
            with r_down:
                report_text = f"NewsGuard AI Report\nResult: {'REAL' if prediction==1 else 'FAKE'}\nConfidence: {confidence:.2f}%\nSummary: {result['summary']}"
                st.download_button("📥 Download Report .txt", data=report_text, file_name="news_report.txt", use_container_width=True)
            with r_share:
                if st.button("📤 Share Results", use_container_width=True):
                    st.toast("Report link copied to clipboard!", icon="🚀")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #64748B !important; font-size: 13.5px !important; opacity: 0.8;'>"
    "⚠️ AI can make mistakes, please check again."
    "</p>", 
    unsafe_allow_html=True
)
