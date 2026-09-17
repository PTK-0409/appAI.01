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

# Khởi tạo mô hình AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

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
            with st.spinner("🤖 AI đang phân tích logic code..."):
                prompt = f"""
                Bạn là một Chuyên gia Lập trình và Mentor dạy code cực kỳ kiên nhẫn.
                Học viên đang học ngôn ngữ: **{prog_lang}** ở trình độ: **{dev_level}**.

                Hãy xử lý yêu cầu sau đây và trả lời bằng Tiếng Việt theo cấu trúc:
                1. **🔍 Phân Tích Vấn Đề / Lỗi Sai**: Chỉ rõ nguyên nhân hoặc bản chất thuật toán bằng ngôn từ dễ hiểu.
                2. **💡 Ý Tưởng Giải Quyết (Pseudocode)**: Giải thích tư duy các bước xử lý trước khi viết code.
                3. **💻 Mã Nguồn Chuẩn**: Đưa ra đoạn code hoàn chỉnh, sạch sẽ, có chú thích (comment) chi tiết ở từng dòng quan trọng.
                4. **⚡ Mẹo Tối Ưu Code**: 1 lời khuyên ngắn giúp code chạy nhanh hơn hoặc tránh lỗi logic phổ biến.
                """
                
                res = model.generate_content([prompt, f"Nội dung học viên gửi:\n{user_code}"])
                st.markdown(res.text)

# ================= TAB 2: BÀI TẬP THỬ THÁCH =================
with tab2:
    st.subheader("Tự Tạo Bài Tập Luyện Tư Duy")
    topic = st.text_input(
        "Chủ đề muốn luyện tập (không bắt buộc):",
        placeholder="Ví dụ: Vòng lặp For, Mảng 2 chiều, Truy vấn SQL JOIN, Con trỏ C++..."
    )

    if st.button("🎲 Tạo Thử Thách Mới", type="primary", use_container_width=True, key="btn_challenge"):
        with st.spinner(f"🎲 AI đang soạn bài tập {prog_lang} phù hợp với [{dev_level}]..."):
            test_prompt = f"""
            Tạo 1 bài tập lập trình ngôn ngữ **{prog_lang}** cho trình độ **{dev_level}**.
            Chủ đề ưu tiên: **{topic if topic else 'Tổng hợp kiến thức đúng trình độ'}**.

            Trình bày theo cấu trúc Markdown sau:
            ### 📝 Đề Bài: [Tên bài tập]
            - **Mô tả bài toán**:
            - **Đầu vào (Input)** & **Đầu ra (Output)**:
            - **Ví dụ mẫu (Test case)**:

            ---
            ### 🔑 Hướng Dẫn & Đáp Án Mẫu
            - **Gợi ý thuật toán**: 
            - **Mã nguồn chuẩn**: Code đầy đủ kèm chú thích giải thích chi tiết từng dòng.
            """
            
            res_test = model.generate_content(test_prompt)
            st.markdown(res_test.text)
