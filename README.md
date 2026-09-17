import streamlit as st
import google.generativeai as genai
from PIL import Image

# Cấu hình giao diện Web
st.set_page_config(page_title="PolyGlot AI - Chuẩn Trình Độ Quốc Tế", page_icon="🌐", layout="centered")

st.title("🌐 PolyGlot AI - Học Ngôn Ngữ Theo Khung Chuẩn Quốc Tế")
st.caption("Tự động điều chỉnh bài giảng theo khung năng lực chuẩn: IELTS, HSK, JLPT, TOPIK, DELF...")

# 1. TỰ ĐỘNG LẤY API KEY
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key (nếu chưa cài Secrets):", type="password")

if not api_key:
    st.info("💡 Vui lòng nhập Gemini API Key ở thanh bên trái (hoặc cấu hình Secrets) để bắt đầu!")
    st.stop()

# Khởi tạo AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. ĐỊNH NGHĨA BẬC TRÌNH ĐỘ CHO TỪNG NGÔN NGỮ
LEVELS_BY_LANGUAGE = {
    "Tiếng Anh": [
        "🌱 Sơ cấp (Mới bắt đầu / Lớp 1-5)",
        "📘 Trung cấp (CEFR A1 - A2 / THCS)",
        "🎓 Nâng cao (CEFR B1 - B2 / THPT)",
        "🏆 Luyện thi IELTS 4.0 - 5.5",
        "🔥 Luyện thi IELTS 6.0 - 7.5+",
        "💼 Giao tiếp công sở / Thương mại"
    ],
    "Tiếng Trung": [
        "🔴 HSK 1 (Sơ cấp - Nhập môn)",
        "🔴 HSK 2 (Sơ cấp - Giao tiếp cơ bản)",
        "🟡 HSK 3 (Trung cấp 1 - Đã có nền tảng)",
        "🟡 HSK 4 (Trung cấp 2 - Thi du học/việc làm)",
        "🔵 HSK 5 (Cao cấp 1 - Thành thạo)",
        "🔵 HSK 6 (Cao cấp 2 - Chuyên gia)"
    ],
    "Tiếng Nhật": [
        "🟢 JLPT N5 (Sơ cấp 1 - Bảng chữ cái & Bảng câu ngắn)",
        "🟢 JLPT N4 (Sơ cấp 2 - Kanji cơ bản & Mẫu câu thông dụng)",
        "🟡 JLPT N3 (Trung cấp - Giao tiếp hàng ngày)",
        "🔴 JLPT N2 (Trung Cao cấp - Làm việc tại công ty Nhật)",
        "🟣 JLPT N1 (Cao cấp - Đọc báo chí, tài liệu chuyên ngành)"
    ],
    "Tiếng Hàn": [
        "🟢 TOPIK 1 - Cấp 1 (Sơ cấp - Bảng chữ cái Hangeul)",
        "🟢 TOPIK 1 - Cấp 2 (Sơ cấp - Giao tiếp hàng ngày)",
        "🟡 TOPIK 2 - Cấp 3 (Trung cấp 1)",
        "🟡 TOPIK 2 - Cấp 4 (Trung cấp 2 - Thi du học)",
        "🔴 TOPIK 2 - Cấp 5 & 6 (Cao cấp - Dịch thuật / Chuyên nghiệp)"
    ],
    "Tiếng Pháp": [
        "🇫🇷 DELF A1 (Nhập môn)",
        "🇫🇷 DELF A2 (Sơ cấp)",
        "🇫🇷 DELF B1 (Trung cấp)",
        "🇫🇷 DELF B2 (Độc lập / Nâng cao)",
        "🇫🇷 DALF C1 / C2 (Cao cấp / Thành thạo)"
    ],
    "Tiếng Đức": [
        "🇩🇪 Goethe A1 (Sơ cấp 1)",
        "🇩🇪 Goethe A2 (Sơ cấp 2)",
        "🇩🇪 Goethe B1 (Trung cấp 1 - Thi du học nghề)",
        "🇩🇪 Goethe B2 (Trung cấp 2)",
        "🇩🇪 Goethe C1 / C2 (Cao cấp)"
    ]
}

# 3. GIAO DIỆN CHỌN NGÔN NGỮ VÀ TRÌNH ĐỘ TƯƠNG ỨNG
col1, col2 = st.columns(2)

with col1:
    target_lang = st.selectbox("🌐 Chọn Ngôn ngữ:", list(LEVELS_BY_LANGUAGE.keys()))

with col2:
    # Danh sách cấp bậc sẽ TỰ ĐỘNG THAY ĐỔI khi đổi Ngôn ngữ ở col1
    selected_level = st.selectbox("🎯 Trình độ / Cấp bậc:", LEVELS_BY_LANGUAGE[target_lang])

st.write("---")

# 4. NHẬP NỘI DUNG DẠY / GIẢI BÀI
user_text = st.text_area(
    "✏️ Nhập đề bài tập, từ vựng hoặc đoạn văn cần trợ giúp:",
    placeholder=f"Ví dụ: Dịch câu này, Phân tích ngữ pháp, Tra từ vựng chuẩn trình độ {selected_level}..."
)

uploaded_img = st.file_uploader("📷 Tải ảnh bài tập (nếu có):", type=["png", "jpg", "jpeg"])

if uploaded_img:
    img = Image.open(uploaded_img)
    st.image(img, caption="Ảnh đề bài đã chọn", use_container_width=True)

# 5. XỬ LÝ VÀ PHÂN TÍCH THEO TRÌNH ĐỘ CHUẨN
if st.button("✨ Hướng dẫn theo trình độ chuẩn của tôi", type="primary", use_container_width=True):
    if not user_text and not uploaded_img:
        st.warning("⚠️ Bạn hãy nhập nội dung câu hỏi hoặc tải ảnh bài tập lên nhé!")
    else:
        with st.spinner(f"🤖 AI đang soạn bài giảng chuẩn trình độ [{target_lang} - {selected_level}]..."):
            
            prompt = f"""
            Bạn là một chuyên gia đào tạo ngôn ngữ {target_lang} chuẩn quốc tế.
            Học sinh đang học ở trình độ: **{selected_level}**.

            Hãy xử lý bài tập/yêu cầu dưới đây và trả lời bằng Tiếng Việt sao cho PHÙ HỢP CHÍNH XÁC với trình độ **{selected_level}**:

            **Yêu cầu chuyên môn:**
            1. **Nếu là Sơ cấp (A1/A2, HSK 1-2, N5-N4, TOPIK 1)**: 
               - Giải thích bằng từ ngữ đơn giản, có phiên âm chi tiết (Pinyin, Romaji, Hangeul...).
               - Tránh dùng các cấu trúc ngữ pháp quá phức tạp ngoài phạm vi trình độ này.
            2. **Nếu là Trung cấp (B1/B2, HSK 3-4, N3-N2, TOPIK 3-4)**: 
               - Phân tích rõ các ngữ pháp nền tảng, bẫy trắc nghiệm, các từ đồng nghĩa/trái nghĩa hay gặp trong đề thi chuẩn.
            3. **Nếu là Cao cấp / Luyện thi (IELTS 6.5+, HSK 5-6, N1, TOPIK 5-6)**: 
               - Phân tích sắc thái từ (Nuance), Collocations, cấu trúc nâng cao, ngữ cảnh trang trọng/văn viết.

            **Cấu trúc câu trả lời:**
            1. **🎯 ĐÁP ÁN / BẢN DỊCH CHUẨN**: Đáp án ngắn gọn, chính xác.
            2. **🔍 GIẢI THÍCH CHI TIẾT (Phù hợp trình độ {selected_level})**: Phân tích vì sao chọn đáp án này, cấu trúc được sử dụng.
            3. **💡 TỪ VỰNG CHUẨN TRÌNH ĐỘ**: 3-5 từ vựng/cụm từ thuộc đúng khung năng lực {selected_level} kèm phiên âm và nghĩa.
            4. **🌟 MẸO LÀM BÀI / ĐIỂM CẦN LƯU Ý**: 1 lời khuyên giúp học sinh ăn điểm ở cấp độ này.
            """
            
            contents = [prompt]
            if user_text:
                contents.append(f"Nội dung học sinh gửi: {user_text}")
            if uploaded_img:
                contents.append(img)
                
            response = model.generate_content(contents)
            
            st.success(f"🎉 Đã hoàn thành bài giảng chuẩn trình độ {selected_level}!")
            st.markdown(response.text)
