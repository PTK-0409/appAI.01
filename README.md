pip install streamlit google-generativeai pillow
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Cấu hình giao diện Web
st.set_page_config(page_title="PolyGlot AI Tutor", page_icon="🌐", layout="wide")

st.title("🌐 PolyGlot AI Tutor - Trợ lý Ngôn ngữ Đa năng")
st.caption("Chữa bài tập, giải thích chi tiết & tra cứu từ vựng thông minh")

# Thanh cấu hình bên trái (Sidebar)
st.sidebar.header("⚙️ Cấu hình")
api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")
target_language = st.sidebar.selectbox(
    "Ngôn ngữ đang học:",
    ["Tiếng Anh", "Tiếng Trung", "Tiếng Nhật", "Tiếng Hàn", "Tiếng Pháp", "Tiếng Đức", "Khác"]
)

if not api_key:
    st.warning("⚠️ Vui lòng nhập Gemini API Key ở thanh bên trái để bắt đầu!")
    st.stop()

# Khởi tạo mô hình AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Chia thành 2 tính năng chính bằng Tabs
tab1, tab2 = st.tabs(["📝 Giải & Phân tích Bài tập", "📚 Tra cứu Từ vựng"])

# TAB 1: GIẢI BÀI TẬP
with tab1:
    st.subheader("Tải ảnh hoặc nhập văn bản đề bài")
    input_text = st.text_area("Nhập văn bản bài tập (nếu có):", placeholder="Ví dụ: Fill in the blank: She _____ to school yesterday. (go/went/gone)")
    uploaded_file = st.file_uploader("Hoặc tải ảnh chụp bài tập:", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh bài tập đã tải lên", use_container_width=True)

    if st.button("🚀 Giải bài & Phân tích", key="btn_solve"):
        if not input_text and not uploaded_file:
            st.error("Vui lòng nhập chữ hoặc tải ảnh đề bài lên!")
        else:
            with st.spinner("AI đang phân tích và giải bài..."):
                prompt = f"""
                Bạn là một giáo viên dạy ngôn ngữ xuất sắc. Hãy hỗ trợ học sinh giải bài tập {target_language} sau.
                
                Yêu cầu cấu trúc phản hồi đúng theo 3 phần sau bằng tiếng Việt:
                1. **🎯 ĐÁP ÁN CHÍNH XÁC**: Đưa ra đáp án ngắn gọn, rõ ràng.
                2. **🔍 GIẢI THÍCH CHI TIẾT**: 
                   - Giải thích lý do chọn đáp án này.
                   - Phân tích cấu trúc ngữ pháp/quy tắc được áp dụng.
                   - Giải thích tại sao các phương án còn lại (nếu là trắc nghiệm) lại sai.
                3. **💡 TỪ VỰNG KÈM THEO**:
                   - Liệt kê 3-5 từ vựng/cụm từ quan trọng trong bài tập kèm phiên âm, nghĩa tiếng Việt và 1 ví dụ minh họa.
                """
                
                inputs = [prompt]
                if input_text:
                    inputs.append(f"Đề bài văn bản: {input_text}")
                if uploaded_file:
                    inputs.append(image)

                response = model.generate_content(inputs)
                st.markdown("---")
                st.markdown(response.text)

# TAB 2: TRA CỨU TỪ VỰNG
with tab2:
    st.subheader("Trợ lý từ vựng chuyên sâu")
    vocab_word = st.text_input("Nhập từ/cụm từ cần tra cứu:", placeholder="Ví dụ: ephemeral, 🔍, 努力...")
    
    if st.button("🔍 Tra cứu", key="btn_vocab"):
        if not vocab_word:
            st.error("Vui lòng nhập từ cần tra!")
        else:
            with st.spinner("AI đang tạo thẻ từ vựng..."):
                vocab_prompt = f"""
                Hãy đóng vai là một từ điển thông minh cho ngôn ngữ {target_language}.
                Hãy phân tích từ/cụm từ: '{vocab_word}'.
                
                Đưa ra kết quả trình bày dạng Markdown sạch đẹp gồm:
                - **Từ gốc & Từ loại**
                - **Phiên âm IPA / Pinyin / Romaji** (tùy ngôn ngữ)
                - **Nghĩa tiếng Việt**
                - **Ví dụ thực tế**: 2 câu ví dụ kèm dịch nghĩa tiếng Việt.
                - **Từ đồng nghĩa / Trái nghĩa**
                - **🧠 Mẹo ghi nhớ / Gốc từ (Etymology)**: Giải thích ngắn gọn giúp học sinh nhớ lâu.
                """
                response = model.generate_content(vocab_prompt)
                st.markdown("---")
                st.markdown(response.text)
