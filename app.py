import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện Web
st.set_page_config(page_title="DevTutor AI - Học Lập Trình", page_icon="💻", layout="centered")

st.title("💻 DevTutor AI - Trợ Lý Học Lập Trình")
st.caption("Hướng dẫn tư duy logic, tìm lỗi code & luyện tập từ Cơ bản đến Nâng cao")

# 1. TỰ ĐỘNG LẤY API KEY
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key (nếu chưa cài Secrets):", type="password")

if not api_key:
    st.info("💡 Vui lòng nhập Gemini API Key ở thanh bên trái để khởi chạy ứng dụng!")
    st.stop()

# Khởi tạo mô hình AI với model chuẩn tốc độ cao
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. CHỌN NGÔN NGỮ LẬP TRÌNH VÀ CẤP BẬC HỌC
col1, col2 = st.columns(2)

with col1:
    prog_lang = st.selectbox(
        "⚡ Ngôn ngữ lập trình:",
        ["Python", "C++", "SQL", "JavaScript / Web", "C# / Java"]
    )

with col2:
    dev_level = st.selectbox(
        "🎯 Trình độ hiện tại:",
        [
            "🌱 Cơ bản (Cú pháp, Vòng lặp, Câu lệnh điều kiện)",
            "📘 Trung cấp (Mảng, Cấu trúc dữ liệu, Hàm)",
            "🎓 Nâng cao (Thuật toán, Lập trình hướng đối tượng - OOP)",
            "🚀 Thực chiến (Tối ưu mã nguồn, Phân tích dữ liệu & AI)"
        ]
    )

st.write("---")

# 3. CHIA CHỨC NĂNG THÀNH 2 TABS
tab1, tab2 = st.tabs(["💬 Hỏi Đáp & Debug Code", "🧩 Bài Tập & Thử Thách Logic"])

# ================= TAB 1: HỎI ĐÁP & DEBUG CODE =================
with tab1:
    st.subheader("Hướng Dẫn & Phân Tích Lỗi Code")
    user_code = st.text_area(
        "✏️ Nhập thắc mắc hoặc dán đoạn code cần trợ giúp:",
        height=180,
        placeholder="Ví dụ: Làm sao để dùng vòng lặp for trong Python? Hoặc dán đoạn code C++ đang báo lỗi tại đây..."
    )

    if st.button("🚀 Phân Tích & Giải Thích", type="primary", use_container_width=True, key="btn_debug"):
        if not user_code:
            st.warning("⚠️ Vui lòng nhập nội dung thắc mắc hoặc dán đoạn code vào!")
        else:
            prompt = f"""
            Bạn là một Mentor dạy lập trình kiên nhẫn.
            Ngôn ngữ: **{prog_lang}**, Trình độ: **{dev_level}**.

            Hãy trả lời bằng Tiếng Việt theo 4 phần:
            1. 🔍 Phân Tích Vấn Đề / Lỗi Sai
            2. 💡 Ý Tưởng Giải Quyết (Pseudocode)
            3. 💻 Mã Nguồn Chuẩn (có comment giải thích)
            4. ⚡ Mẹo Tối Ưu Code
            """
            try:
                # Dùng streaming để chữ ra ngay lập tức
                response = model.generate_content([prompt, f"Nội dung học viên gửi:\n{user_code}"], stream=True)
                st.write_stream(chunk.text for chunk in response)
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {e}")

# ================= TAB 2: BÀI TẬP THỬ THÁCH =================
with tab2:
    st.subheader("Tự Tạo Bài Tập Luyện Tư Duy")
    topic = st.text_input(
        "Chủ đề muốn luyện tập (không bắt buộc):",
        placeholder="Ví dụ: Vòng lặp For, Mảng 2 chiều, Truy vấn SQL JOIN..."
    )

    if st.button("🎲 Tạo Thử Thách Mới", type="primary", use_container_width=True, key="btn_challenge"):
        test_prompt = f"""
        BẮT ĐẦU NGAY VÀO ĐỀ BÀI, KHÔNG CHÀO HỎI HAY VIẾT MỞ BÀI.
        Tạo 1 bài tập lập trình {prog_lang} cho trình độ {dev_level}.
        Chủ đề: {topic if topic else 'Tổng hợp kiến thức đúng trình độ'}.

        Trình bày theo dạng Markdown:
        ### 📝 Đề Bài: [Tên bài tập]
        - **Mô tả ngắn**:
        - **Input / Output mẫu**:

        ---
        ### 🔑 Hướng Dẫn & Đáp Án
        - **Gợi ý thuật toán**: 2 dòng ngắn gọn.
        - **Mã nguồn chuẩn**: Code đầy đủ kèm chú thích giải thích chi tiết.
        """
        
        try:
            # Tạo hiệu ứng chảy chữ siêu tốc
            response = model.generate_content(test_prompt, stream=True)
            st.write_stream(chunk.text for chunk in response)
        except Exception as e:
            st.error(f"❌ Có lỗi khi tạo bài test: {e}")
