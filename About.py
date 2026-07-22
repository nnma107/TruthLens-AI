
from pathlib import Path
import streamlit as st


# Cấu hình trang đồng bộ
st.set_page_config(
    page_title="About - TruthLens AI",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================
# SIDEBAR (Hiển thị danh mục & màu sắc đồng bộ y chang app.py)
# ==========================================
with st.sidebar:
    st.title("TruthLens AI")
    st.caption("AI Fake News Detection")
    st.divider()
    
    # Sử dụng st.page_link để điều hướng mượt mà
    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/History.py", label="📜 History")
    st.page_link("pages/Performance.py", label="📊 Model Performance")
    st.page_link("pages/About.py", label="ℹ️ About")
    
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
    /* 1. Ép màu nền tối toàn bộ trang */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        color: #f8fafc !important;
    }
    
    /* 2. Ép màu nền Sidebar (#111827) */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* 3. FIX TRIỆT ĐỂ MÀU CHỮ TRONG SIDEBAR & PAGE_LINK */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] div {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* Ép màu xám phụ cho caption/subtext trong Sidebar */
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    [data-testid="stSidebar"] caption {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* Đổi màu khi di chuột vào nút liên kết trang trong Sidebar */
    [data-testid="stSidebar"] a:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #111827; padding: 12px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); margin: -5rem -5rem 2rem -5rem;">
    <div style="display: flex; align-items: center; gap: 14px;">
        <img src="assets/logo.png" style="width: 38px; height: 38px; object-fit: contain;">
        <div>
            <b style="color: #f8fafc; font-size: 18px; font-family: sans-serif;">TruthLens <span style="color:#3b82f6;">AI</span></b><br>
            <span style="color: #94a3b8; font-size: 11px;">Detect Fake. Trust Real.</span>
        </div>
    </div>
    <div style="display: flex; gap: 60px; color: #94a3b8; font-size: 16px; font-weight: 500;">
        <a href="/" target="_self" style="color: #94a3b8; text-decoration: none;">Home</a>
        <a href="/" target="_self" style="color: #94a3b8; text-decoration: none;">Detect</a>
        <a href="/About" target="_self" style="color: #38bdf8; border-bottom: 2px solid #3b82f6; padding-bottom: 4px; text-decoration: none;">About</a>
        <a href="/History" target="_self" style="color: #94a3b8; text-decoration: none;">History</a>
    </div>
    <div style="display: flex; align-items: center; gap: 20px;">
        <span style="color: #94a3b8; font-size: 16px; cursor: pointer;"> &nbsp; </span>
        <div style="background-color: #3b82f6; color: #f8fafc; padding: 6px 16px; border-radius: 6px; font-size: 13px; font-weight: bold; cursor: pointer;">Login</div>
    </div>
</div>
""", unsafe_allow_html=True)
import streamlit as st

# 1. Khởi tạo trạng thái Theme trong session_state nếu chưa có
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark" # Mặc định là Dark Mode

# 2. Hàm áp dụng CSS theo chủ đề
def apply_theme():
    if st.session_state.theme_mode == "dark":
        # CSS Dành cho DARK MODE
        theme_css = """
        <style>
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #0B0F19 !important;
                color: #F8FAFC !important;
            }
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #0F172A !important;
                border-right: 1px solid rgba(255,255,255,0.05) !important;
            }
            /* Thẻ Card */
            .custom-card {
                background-color: #111827 !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                color: #F8FAFC !important;
            }
            /* Tiêu đề Ombre Dark */
            .ombre-title {
                background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }
        </style>
        """
    else:
        # CSS Dành cho LIGHT MODE
        theme_css = """
        <style>
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #F8FAFC !important;
                color: #0F172A !important;
            }
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #FFFFFF !important;
                border-right: 1px solid #E2E8F0 !important;
            }
            /* Thẻ Card Light */
            .custom-card {
                background-color: #FFFFFF !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
                color: #0F172A !important;
            }
            /* Tiêu đề Ombre Light */
            .ombre-title {
                background: linear-gradient(135deg, #0F172A 30%, #0284C7 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }
            /* Đảm bảo chữ trong card và label dễ đọc ở Light Mode */
            p, span, label {
                color: #334155 !important;
            }
        </style>
        """
    st.markdown(theme_css, unsafe_allow_html=True)

# Gọi hàm áp dụng CSS ngay đầu trang
apply_theme()
# ==========================================
# INJECT CSS PHONG CÁCH DARK MODE & GRADIENT OMBRE TRONG ẢNH MẪU
# ==========================================
st.markdown("""
<style>
    /* 1. Ép toàn bộ màu nền tối sâu thẳm như ảnh mẫu */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0B0F19 !important;
        color: #F8FAFC !important;
    }

    /* Đảm bảo sidebar đồng bộ */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* 2. HIỆU ỨNG TIÊU ĐỀ OMBRE SIÊU CẤP ĐÈ MỌI THÀNH PHẦN MẶC ĐỊNH */
    .ombre-title {
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 52px !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px !important;
        background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        color: transparent !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
        line-height: 1.2 !important;
        display: inline-block !important;
    }
    
    .ombre-subtitle {
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 38px !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(135deg, #FFFFFF 40%, #60A5FA 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        color: transparent !important;
        margin-top: 40px !important;
        margin-bottom: 25px !important;
        line-height: 1.3 !important;
        display: inline-block !important;
    }

    /* 3. THIẾT KẾ CARD NỀN TỐI CAO CẤP (Bọc các khối thông tin như ảnh mẫu) */
    .about-card {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .about-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    /* Định dạng chữ nhỏ bên trong Card */
    .card-title {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .card-text {
        color: #94A3B8 !important;
        font-size: 14.5px !important;
        line-height: 1.6 !important;
        margin-bottom: 0px !important;
    }

    /* Thiết kế riêng bảng thông tin kĩ thuật số mượt mà */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .custom-table td {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #94A3B8;
        font-size: 14.5px;
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    .custom-table td strong {
        color: #FFFFFF;
    }
    .metric-badge {
        background: rgba(56, 189, 248, 0.1);
        color: #38BDF8 !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
    }

    /* Quy trình Pipeline ngang */
    .pipeline-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        background: #111827;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .pipeline-step {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        color: #F8FAFC;
    }
    .pipeline-arrow {
        color: #38BDF8;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)



# ==========================================
# HEADER BANNER (Tiêu đề chính Ombre giống ảnh)
# ==========================================
st.markdown('<div class="ombre-title">What we do</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color: #94A3B8; font-size: 18px; margin-top: 5px; margin-bottom: 40px; max-width: 800px;'>"
    "TruthLens AI is an intelligent web application designed to help users identify fake news and evaluate the credibility of online information. "
    "By combining Machine Learning, Natural Language Processing (NLP), and Google Gemini AI, the platform delivers transparent, explainable results."
    "</p>", 
    unsafe_allow_html=True
)


# ==========================================
# GRID 1: OVERVIEW & OBJECTIVES (Layout 2 cột song song)
# ==========================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
    <div class="about-card">
        <div class="card-title">🎯 Project Overview</div>
        <p class="card-text">
            The rapid growth of social media and digital news platforms has made misinformation spread faster than ever. 
            Fake news can influence public opinion, create confusion, and even cause serious social consequences. <br><br>
            <b>TruthLens AI</b> was developed as an educational and practical solution to address this problem. 
            Instead of simply classifying news articles, the system explains its reasoning and encourages users to verify information through reliable sources.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="about-card">
        <div class="card-title">🚀 Project Objectives</div>
        <p class="card-text" style="line-height: 1.8;">
            ✅ Detect fake news using Machine Learning.<br>
            ✅ Help users evaluate the credibility of news articles.<br>
            ✅ Explain prediction results using Generative AI.<br>
            ✅ Encourage critical thinking and fact-checking.<br>
            ✅ Demonstrate the practical application of Artificial Intelligence in combating misinformation.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# HEADER 2: THE PROCESS (Tiêu đề Ombre tiếp theo)
# ==========================================
st.markdown('<div class="ombre-subtitle">The process</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='color: #94A3B8; font-size: 15px; margin-top: 5px; margin-bottom: 20px;'>"
    "Every news article follows a complete automated AI pipeline data sequence:"
    "</p>", 
    unsafe_allow_html=True
)

# Hiển thị luồng Pipeline trực quan
st.markdown("""
<div class="pipeline-container">
    <div class="pipeline-step">📄 News Article</div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-step">⚙️ Text Cleaning (NLP)</div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-step">📊 TF-IDF Extraction</div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-step">🧠 Logistic Regression</div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-step">🤖 Gemini AI Analysis</div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-step">✨ Final Result</div>
</div>
<br>
<p style='color: #94A3B8; font-size: 14.5px; line-height: 1.6;'>
    The article is first cleaned using Natural Language Processing techniques to remove unnecessary characters, URLs, and formatting. 
    The cleaned text is then converted into numerical features using the TF-IDF algorithm. A Logistic Regression model predicts whether the article is Real or Fake. 
    Finally, Google Gemini AI analyzes the content, explains the prediction, evaluates credibility, and provides recommendations for verification.
</p>
""", unsafe_allow_html=True)

# ==========================================
# GRID 2: CORE ARCHITECTURE (3 Cột giống khối dưới của ảnh mẫu)
# ==========================================
st.markdown('<div class="ombre-subtitle">AI & Machine Learning</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">🔮 Natural Language Processing</div>
        <p class="card-text">
            Before training and prediction, every article is preprocessed by converting text to lowercase, removing URLs, punctuation, special characters, and extra spaces. 
            This improves data quality and helps the model focus on meaningful information.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">📊 TF-IDF Extraction</div>
        <p class="card-text">
            TF-IDF (Term Frequency–Inverse Document Frequency) converts text into numerical vectors by measuring the importance of words within a document while reducing the influence of common words.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">🧠 Logistic Regression</div>
        <p class="card-text">
            The classification model used in this project is Logistic Regression, a supervised Machine Learning algorithm widely used for text classification. Based on TF-IDF features, the model predicts the news category.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# GRID 3: GEMINI AI & KEY FEATURES
# ==========================================
st.markdown('<br>', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown(f"""
    <div class="about-card">
        <div class="card-title">🤖 Google Gemini AI Integration</div>
        <p class="card-text" style="line-height: 1.7;">
            After the Machine Learning model generates a prediction, Google Gemini AI performs an additional analysis to improve user understanding. Gemini generates:
            <br><br>
            • A concise summary of the article<br>
            • AI explanation of the prediction<br>
            • Credibility analysis & trust score indicators<br>
            • Factual verification recommendations
            <br><br>
            This hybrid combination makes the system more transparent and easier to understand than a traditional black-box classifier.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div class="about-card">
        <div class="card-title">✨ Key Platform Features</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 5px;">
            <span class="pipeline-step">🛡️ Fake News Detection</span>
            <span class="pipeline-step">⚙️ NLP Text Cleaning</span>
            <span class="pipeline-step">📊 TF-IDF Vectors</span>
            <span class="pipeline-step">📝 AI Article Summary</span>
            <span class="pipeline-step">📈 Trust Score Evaluation</span>
            <span class="pipeline-step">🔍 Credibility Analysis</span>
            <span class="pipeline-step">🤖 Gemini 2.5 Explanations</span>
            <span class="pipeline-step">📜 Analysis History Log</span>
            <span class="pipeline-step">💻 Interactive Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# GRID 4: TECHNICAL PERFORMANCE TABLE & GUIDES
# ==========================================
st.markdown('<div class="ombre-subtitle">System Specifications</div>', unsafe_allow_html=True)

t_col1, t_col2 = st.columns([1.1, 0.9], gap="large")

with t_col1:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">📊 Model Performance Matrix</div>
        <table class="custom-table">
            <tr><td><strong>Classification Model</strong></td><td>Logistic Regression</td></tr>
            <tr><td><strong>Feature Extraction</strong></td><td>TF-IDF Vectorizer</td></tr>
            <tr><td><strong>Natural Language Processing</strong></td><td>Custom Text Cleaning</td></tr>
            <tr><td><strong>AI Assistant Engine</strong></td><td>Google Gemini 2.5 Flash</td></tr>
            <tr><td><strong>Train Accuracy</strong></td><td><span class="metric-badge">99.41%</span></td></tr>
            <tr><td><strong>Test Accuracy</strong></td><td><span class="metric-badge">98.77%</span></td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with t_col2:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">📖 User Guide</div>
        <p class="card-text" style="line-height: 1.75;">
            1. <b>Paste Article</b>: Paste a news article into the dashboard input area.<br>
            2. <b>Analyze</b>: Click the <i>Analyze News</i> button.<br>
            3. <b>Prediction</b>: The Machine Learning model evaluates if the article is Real/Fake.<br>
            4. <b>AI Generation</b>: Gemini AI generates a summary, detailed analysis, and score.<br>
            5. <b>Fact-Check</b>: Review the verification roadmap before sharing online.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# GRID 5: WHY US & FUTURE
# ==========================================
st.markdown('<br>', unsafe_allow_html=True)
b_col1, b_col2 = st.columns(2, gap="large")

with b_col1:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">⭐ Why TruthLens AI?</div>
        <p class="card-text">
            Unlike conventional fake news detectors that only provide a binary prediction, TruthLens AI focuses on <b>Explainable Artificial Intelligence (XAI)</b>. 
            Users not only receive a classification result but also understand <i>why</i> the prediction was made through detailed explanations. 
            This helps users cultivate critical thinking rather than relying solely on an AI label.
        </p>
    </div>
    """, unsafe_allow_html=True)

with b_col2:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">🚀 Future Improvements</div>
        <p class="card-text">
            • Supporting multi-language articles.<br>
            • Integrating OCR for extracting and analyzing text inside images.<br>
            • Live connecting with professional database fact-checking networks.<br>
            • Upgrading core models to transformer-based architectures like BERT.<br>
            • Expanding support for official mobile applications.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER: DEVELOPER INFO & DISCLAIMER
# ==========================================
st.markdown('<div class="ombre-subtitle">Administration</div>', unsafe_allow_html=True)

f_col1, f_col2 = st.columns([0.8, 1.2], gap="large")

with f_col1:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">👨‍💻 Developer Profile</div>
        <table class="custom-table">
            <tr><td><strong>Project Name</strong></td><td>TruthLens AI</td></tr>
            <tr><td><strong>Project Type</strong></td><td>Fake News Detection Platform</td></tr>
            <tr><td><strong>Developer</strong></td><td>Nguyen Ngoc Minh Anh</td></tr>
            <tr><td><strong>Core Tech</strong></td><td>Python, Streamlit, Scikit-learn, Gemini API</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
    <div class="about-card">
        <div class="card-title">📄 Legal Disclaimer</div>
        <p class="card-text" style="font-style: italic; font-size: 13.5px;">
            TruthLens AI is designed as an educational and decision-support tool. 
            The predictions and AI-generated explanations are intended to assist users in evaluating news credibility but should not be considered absolute, faultless facts. 
            Users are strongly encouraged to cross-verify critical information using trusted news organizations and official primary sources before making real-world decisions or sharing content on social media.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Thêm khoảng trống chân trang
st.markdown("<br><br><br>", unsafe_allow_html=True)