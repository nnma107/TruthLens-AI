import streamlit as st
import json


# SIDEBAR (Hiển thị danh mục & màu sắc đồng bộ y chang app.py)
# ==========================================

with st.sidebar:
    st.title("TruthLens AI")
    st.caption("AI Fake News Detection")
    st.divider()
    
    # Sử dụng st.page_link để điều hướng
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
# ==========================================
# 1. PAGE CONFIG (ĐẶT ĐẦU FILE)
# ==========================================
st.set_page_config(
    page_title="History - TruthLens AI",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. KHỞI TẠO SESSION STATE
# ==========================================
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.title("TruthLens AI")
    st.caption("AI Fake News Detection")
    st.divider()
    
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

# ==========================================
# 4. STYLING ĐẦY ĐỦ (HOÀN CHỈNH THẺ CSS)
# ==========================================
st.markdown("""
<style>
    /* 1. Nền toàn bộ trang */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        color: #f8fafc !important;
    }
    
    /* 2. Sidebar tối màu */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* 3. Input & Selectbox */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #1e293b !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
    }
    input[data-testid="stTextInput"] {
        color: #f8fafc !important;
    }

    /* 4. Badges */
    .badge-real {
        background-color: rgba(34, 197, 94, 0.15);
        color: #22c55e !important;
        border: 1px solid #22c55e;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }

    .badge-fake {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444 !important;
        border: 1px solid #ef4444;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        display: inline-block;
    }

    /* 5. Custom Table Row Box */
    .history-row-container {
        background-color: #1E293B;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        transition: border 0.2s;
    }
    .history-row-container:hover {
        border-color: rgba(56, 189, 248, 0.4);
    }

    /* 6. Text styling */
    h1, h2, h3, h4, p, span, label {
        color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. HEADER & FILTER BAR
# ==========================================
st.markdown("<h1 style='font-size:28px; font-weight:700;'>📜 Analysis History</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom: 25px;'>Manage and review all past news verification records.</p>", unsafe_allow_html=True)

# Thanh công cụ: Tìm kiếm + Lọc + Xóa
col_search, col_filter, col_clear = st.columns([0.5, 0.3, 0.2], gap="medium")

with col_search:
    search_query = st.text_input("Search Title / ID", placeholder="🔍 Enter keyword or ID...", label_visibility="collapsed")

with col_filter:
    filter_status = st.selectbox("Filter Status", ["All Results", "REAL ONLY", "FAKE ONLY"], label_visibility="collapsed")

with col_clear:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.analysis_history = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. HIỂN THỊ DẠNG BẢNG (TABLE LAYOUT)
# ==========================================
history_list = st.session_state.get("analysis_history", [])

# Lọc dữ liệu theo Search & Filter
filtered_history = []
for item in history_list:
    matches_search = (search_query.lower() in item["title"].lower()) or (search_query.lower() in item["id"].lower())
    matches_filter = True
    if filter_status == "REAL ONLY" and item["status"] != "REAL":
        matches_filter = False
    elif filter_status == "FAKE ONLY" and item["status"] != "FAKE":
        matches_filter = False
        
    if matches_search and matches_filter:
        filtered_history.append(item)

if not filtered_history:
    st.info("ℹ️ No matching analysis records found in history.")
else:
    # Header của Bảng
    h_col1, h_col2, h_col3, h_col4, h_col5, h_col6 = st.columns([0.15, 0.35, 0.12, 0.12, 0.14, 0.12])
    with h_col1: st.markdown("<b style='color:#94a3b8; font-size:12px;'>LOG ID</b>", unsafe_allow_html=True)
    with h_col2: st.markdown("<b style='color:#94a3b8; font-size:12px;'>ARTICLE TITLE</b>", unsafe_allow_html=True)
    with h_col3: st.markdown("<b style='color:#94a3b8; font-size:12px;'>RESULT</b>", unsafe_allow_html=True)
    with h_col4: st.markdown("<b style='color:#94a3b8; font-size:12px;'>CONFIDENCE</b>", unsafe_allow_html=True)
    with h_col5: st.markdown("<b style='color:#94a3b8; font-size:12px;'>DATE & TIME</b>", unsafe_allow_html=True)
    with h_col6: st.markdown("<b style='color:#94a3b8; font-size:12px;'>ACTION</b>", unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.1; margin: 8px 0 16px 0;'>", unsafe_allow_html=True)

    # Render từng dòng trong Bảng
    for idx, item in enumerate(filtered_history):
        c1, c2, c3, c4, c5, c6 = st.columns([0.15, 0.35, 0.12, 0.12, 0.14, 0.12])
        
        # ID
        with c1:
            st.markdown(f"<span style='font-family:monospace; color:#38bdf8; font-size:12px;'>{item['id'][:12]}...</span>", unsafe_allow_html=True)
        
        # Title
        with c2:
            st.markdown(f"<span style='font-weight:500; font-size:13.5px;'>{item['title']}</span>", unsafe_allow_html=True)
        
        # Status Badge
        with c3:
            badge_class = "badge-real" if item["status"] == "REAL" else "badge-fake"
            st.markdown(f"<span class='{badge_class}'>{item['status']}</span>", unsafe_allow_html=True)
        
        # Confidence
        with c4:
            color = "#22c55e" if item["status"] == "REAL" else "#ef4444"
            st.markdown(f"<b style='color:{color}; font-size:13.5px;'>{item['score']}</b>", unsafe_allow_html=True)
        
        # Date
        with c5:
            st.markdown(f"<span style='color:#94a3b8; font-size:12px;'>{item.get('date', 'N/A')}</span>", unsafe_allow_html=True)
        
        # Nút Action Xem Chi Tiết
        with c6:
            with st.expander("🔍 View"):
                st.markdown("#### 📰 Full Article Text")
                st.text_area("", value=item["full_text"], height=150, disabled=True, key=f"hist_txt_{item['id']}")
                
                st.markdown("#### 📝 AI Summary")
                st.info(item.get("summary", "No summary generated."))
                
                if "details" in item:
                    st.markdown("#### 📊 Fact-Check Details")
                    st.write(f"**Explanation:** {item['details'].get('explanation', 'N/A')}")
                    st.write(f"**Verification Step:** {item['details'].get('verification', 'N/A')}")
        
        st.markdown("<hr style='opacity:0.05; margin:10px 0;'>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 13px;'>TruthLens AI • Audit History Log</p>", unsafe_allow_html=True)

