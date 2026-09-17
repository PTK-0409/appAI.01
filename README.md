import streamlit as st
import google.generativeai as genai
from PIL import Image

# Cấu hình giao diện Web
st.set_page_config(page_title="PolyGlot AI - Hỗ Trợ & Đánh Giá Trình Độ", page_icon="🎓", layout="centered")

st.title("🎓 PolyGlot AI - Trợ Lý & Kiểm Tra Ngôn Ngữ Đa Năng")
st.caption("Hỗ trợ giải bài tập, tra cứu & tự động tạo bài test đánh giá trình độ chuẩn quốc tế")

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

# 2. KHUNG TRÌNH ĐỘ CHUẨN THEO TỪNG NGÔN NGỮ
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
        "🟢 JLPT N5 (Sơ cấp 1)",
        "🟢 JLPT N4 (Sơ cấp 2)",
        "🟡 JLPT N3 (Trung cấp)",
        "🔴 JLPT N2 (Trung Cao cấp)",
        "🟣 JLPT N1 (Cao cấp)"
    ],
    "Tiếng Hàn": [
        "🟢 TOPIK 1 - Cấp 1 (Sơ cấp)",
        "🟢 TOPIK 1 - Cấp 2 (Sơ cấp)",
        "🟡 TOPIK 2 - Cấp 3 (Trung cấp 1)",
        "🟡 TOPIK 2 - Cấp 4 (Trung cấp 2)",
        "🔴 TOPIK 2 - Cấp 5 & 6 (Cao cấp)"
    ],
    "Tiếng Pháp": [
        "🇫🇷 DELF A1 (Nhập môn)",
        "🇫🇷 DELF A2 (Sơ cấp)",
        "🇫🇷 DELF B1 (Trung cấp)",
        "🇫🇷 DELF B2 (Nâng cao)"
    ],
    "Tiếng Đức": [
        "🇩🇪 Goethe A1 (Sơ cấp 1)",
        "🇩🇪 Goethe A2 (Sơ cấp 2)",
        "🇩🇪 Goethe B1 (Trung cấp 1)",
        "🇩🇪 Goethe B2 (Trung cấp 2)"
    ]
}

# 3. THANH CHỌN NGÔN NGỮ VÀ TRÌNH ĐỘ
col1, col2 = st.columns(2)
with col1:
    target_lang = st.selectbox("🌐 Chọn Ngôn ngữ:", list(LEVELS_BY_LANGUAGE.keys()))
with col2:
    selected_level = st.selectbox("🎯 Trình độ mục tiêu:", LEVELS_BY_LANGUAGE[target_lang])

st.write("---")

# 4. CHIA TÍNH NĂNG THÀNH 2 TABS
tab1, tab2 = st.tabs(["📝 Hướng Dẫn & Giải Bài", "🎯 Bài Test Đánh Giá Trình Độ"])

# ================= TAB 1: HƯỚNG DẪN & GIẢI BÀI =================
with tab1:
    st.subheader("Trợ lý Giải bài & Tra cứu")
    user_text = st.text_area(
        "✏️ Nhập đề bài tập, từ vựng hoặc đoạn văn:",
        placeholder=f"Ví dụ: Giải thích ngữ pháp câu này, Dịch thuật, Tra từ vựng trình độ {selected_level}..."
    )
    uploaded_img = st.file_uploader("📷 Tải ảnh bài tập (nếu có):", type=["png", "jpg", "jpeg"])

    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, caption="Ảnh đề bài đã chọn", use_container_width=True)

    if st.button("✨ Hướng dẫn bài tập", type="primary", use_container_width=True, key="btn_explain"):
        if not user_text and not uploaded_img:
            st.warning("⚠️ Bạn hãy nhập nội dung hoặc tải ảnh bài tập lên nhé!")
        else:
            with st.spinner("🤖 AI đang phân tích bài học..."):
                prompt = f"""
                Bạn là một chuyên gia dạy {target_lang}. Học sinh đang học ở trình độ **{selected_level}**.
                Hãy giải thích bài tập/yêu cầu sau bằng Tiếng Việt phù hợp chính xác với trình độ này.
                
                Đưa ra câu trả lời gồm:
                1. **🎯 Đáp án / Bản dịch chuẩn**
                2. **🔍 Giải thích chi tiết**
                3. **💡 Từ vựng & Ngữ pháp quan trọng**
                4. **🌟 Mẹo ghi nhớ**
                """
                contents = [prompt]
                if user_text: contents.append(f"Nội dung: {user_text}")
                if uploaded_img: contents.append(img)
                
                res = model.generate_content(contents)
                st.markdown(res.text)

# ================= TAB 2: BÀI TEST ĐÁNH GIÁ TRÌNH ĐỘ =================
with tab2:
    st.subheader(f"Tạo đề kiểm tra trình độ: {selected_level}")
    st.write("AI sẽ tự động tạo bộ câu hỏi kiểm tra gồm trắc nghiệm và điền từ để kiểm tra xem bạn đã đạt trình độ này chưa!")

    num_questions = st.slider("Số lượng câu hỏi:", min_value=3, max_value=5, value=3)

    if st.button("🎲 Bắt đầu làm bài test", type="primary", use_container_width=True, key="btn_test"):
        with st.spinner(f"🎲 AI đang soạn {num_questions} câu hỏi kiểm tra trình độ {selected_level}..."):
            test_prompt = f"""
            Hãy đóng vai là một Giám khảo kiểm tra ngôn ngữ {target_lang}.
            Tạo một bài kiểm tra đánh giá năng lực gồm {num_questions} câu hỏi thuộc chuẩn trình độ **{selected_level}**.

            **Yêu cầu đề thi:**
            - Bao gồm các dạng: Trắc nghiệm tìm đáp án đúng, Chọn từ điền vào chỗ trống, Tìm lỗi sai.
            - Trình bày đề bài rõ ràng, dễ nhìn.
            - Đặt phần **ĐÁP ÁN & ĐÁNH GIÁ NĂNG LỰC** ở phía dưới cùng, trình bày ngắn gọn kèm giải thích.

            Trình bày theo định dạng Markdown đẹp mắt:
            ---
            ### 📝 ĐỀ KIỂM TRA TRÌNH ĐỘ: {selected_level} ({target_lang})
            (Các câu hỏi từ Câu 1 đến Câu {num_questions})
            
            ---
            ### 🔑 ĐÁP ÁN & GIẢI THÍCH CHI TIẾT
            (Liệt kê đáp án từng câu và giải thích ngắn gọn lý do)
            
            ### 📊 THUẬT TOÁN ĐÁNH GIÁ TRÌNH ĐỘ:
            - **Đạt {num_questions}/{num_questions} câu**: Bạn đã hoàn toàn vững vàng trình độ {selected_level}! Có thể thử sức lên cấp độ cao hơn.
            - **Đạt 1-{num_questions-1} câu**: Bạn cần ôn tập thêm phần từ vựng/ngữ pháp còn hổng.
            """
            
            test_res = model.generate_content(test_prompt)
            st.markdown(test_res.text)
