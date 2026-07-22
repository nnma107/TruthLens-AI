import requests

# Đăng ký lấy API Key miễn phí tại: https://www.newscatcherapi.com/
NEWSCATCHER_API_KEY = "YOUR_NEWSCATCHER_API_KEY"

def fetch_latest_news(query=None, minutes_ago=30, country="VN", page_size=5):
    """
    Quét tin tức cập nhật cực nhanh từ NewsCatcher API.
    - query: Từ khóa tìm kiếm (ví dụ: 'thời sự', 'AI', 'kinh tế' hoặc tên sự kiện)
    - minutes_ago: Tìm tin xuất bản trong X phút vừa qua (mặc định 30 phút)
    - country: VN (Việt Nam) hoặc US, GB...
    """
    if not NEWSCATCHER_API_KEY or NEWSCATCHER_API_KEY == "YOUR_NEWSCATCHER_API_KEY":
        return []

    url = "https://v3-api.newscatcherapi.com/api/search"
    headers = {
        "x-api-token": NEWSCATCHER_API_KEY
    }
    
    # Cấu hình tham số quét real-time
    params = {
        "q": query if query else "*",        # Nếu không truyền từ khóa thì lấy tất cả tin mới
        "sort_by": "date",                   # Lấy tin mới nhất lên đầu
        "page_size": page_size,
        "from_": f"{minutes_ago} minutes ago", # Lấy tin xuất bản trong vòng vài phút qua
        "countries": country
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        else:
            print(f"NewsCatcher API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Lỗi khi kết nối NewsCatcher API: {e}")
        return []