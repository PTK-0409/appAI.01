import streamlit as st
import google.generativeai as genai
import requests

# Cấu hình giao diện Web
st.set_page_config(page_title="DevTutor & Code Judge", page_icon="💻", layout="centered")

st.title("💻 DevTutor AI - Luyện Lập Trình & Chấm Bài")
st.caption("Trợ lý học tập cá nhân & Nhóm bạn - Tích hợp máy chấm bài tự động")

# 1. TỰ ĐỘNG LẤY API KEY GEMINI
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key:", type="password")

if not api_key:
    st.info("💡 Vui lòng nhập Gemini API Key ở thanh bên trái để khởi chạy!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. KHO BÀI TẬP CƠ BẢN DÀNH CHO NHÓM BẠN (Bạn có thể tự thêm bài mới vào đây)
PROBLEMS = {
    "Bài 1: Tính tổng 2 số (A + B)": {
        "description": "Nhập vào 2 số nguyên A và B trên 1 dòng (cách nhau bởi dấu cách). In ra tổng của 2 số.",
        "input_test": "5 7",
        "expected_output": "12\n"
    },
    "Bài 2: Kiểm tra số chẵn lẻ": {
        "description": "Nhập vào 1 số nguyên N. Nếu N là số chẵn in ra 'CHAN', ngược lại in ra 'LE'.",
        "input_test": "4",
        "expected_output": "CHAN\n"
    },
    "Bài 3: Tìm số lớn nhất trong 3 số": {
        "description": "Nhập vào 3 số nguyên A, B, C trên 1 dòng. In ra số lớn nhất.",
        "input_test": "10 25 15",
        "expected_output": "25\n"
    }
}

# 3. CHIA GIAO DIỆN THÀNH 2 TABS
tab1, tab2 = st.tabs(["🧪 Chấm Bài Tự Động (Judge)", "💬 Hỏi Đáp & AI Debug"])

# ================= TAB 1: MÁY CHẤM BÀI TỰ ĐỘNG =================
with tab1:
    st.subheader("🎯 Kho Bài Tập & Máy Chấm Bài")
    
    # Chọn bài tập
    selected_prob_title = st.selectbox("📌 Chọn bài tập cần làm:", list(PROBLEMS.keys()))
    prob = PROBLEMS[selected_prob_title]
    
    st.info(f"**Mô tả đề bài:** {prob['description']}")
    
    col_lang, col_space = st.columns([1, 1])
    with col_lang:
        lang = st.selectbox("⚡ Ngôn ngữ nộp bài:", ["Python (3.8.1)", "C++ (GCC 9.2.0)"])
    
    # Ô nhập code
    user_code = st.text_area(
        "📝 Dán đoạn code của bạn vào đây:",
        height=200,
        placeholder="Viết mã nguồn của bạn tại đây..."
    )
    
    if st.button("🚀 Nộp Bài & Chấm Điểm", type="primary", use_container_width=True):
        if not user_code:
            st.warning("⚠️ Vui lòng dán code trước khi nộp bài!")
        else:
            with st.spinner("⚙️ Máy chấm (Judger) đang biên dịch và chạy thử testcase..."):
                # Mã định danh ngôn ngữ trên Judge0 API
                lang_id = 71 if "Python" in lang else 54  # 71 = Python, 54 = C++
                
                # Gửi request đến máy chấm công cộng Judge0 (Free API)
                url = "https://judge0-ce.p.rapidapi.com/submissions?wait=true"
                payload = {
                    "source_code": user_code,
                    "language_id": lang_id,
                    "stdin": prob["input_test"],
                    "expected_output": prob["expected_output"]
                }
                headers = {
                    "content-type": "application/json",
                    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
                    "X-RapidAPI-Key": "7f0980164fmshd1e59bf40fb2b75p16a3a9jsn972236a297b5" # Key dùng chung
                }
                
                try:
                    res = requests.post(url, json=payload, headers=headers).json()
                    status = res.get("status", {}).get("description", "Lỗi không xác định")
                    stdout = res.get("stdout", "")
                    compile_output = res.get("compile_output", "") or res.get("stderr", "")
                    
                    # Hiển thị kết quả chấm
                    if status == "Accepted":
                        st.balloons()
                        st.success("🎉 ACCEPTED (Chính Xác)! Bạn đã vượt qua testcase.")
                    else:
                        st.error(f"❌ Kết quả: **{status}**")
                        if stdout:
                            st.write(f"**Kết quả chạy ra của bạn:** `{stdout.strip()}`")
                            st.write(f"**Kết quả đúng yêu cầu:** `{prob['expected_output'].strip()}`")
                        if compile_output:
                            st.code(compile_output, language="bash")
                            
                        # Tự động nhờ AI phân tích lỗi nếu làm sai
                        st.write("---")
                        st.subheader("🤖 AI Mentor Phân Tích Lỗi:")
                        ai_prompt = f"""
                        Học sinh làm bài tập: {prob['description']}
                        Code của học sinh ({lang}):
                        ```
                        {user_code}
                        ```
                        Máy chấm báo lỗi: {status}
                        Chi tiết lỗi/Kết quả ra: {compile_output if compile_output else stdout}
                        
                        Hãy giải thích ngắn gọn tại sao code bị sai và hướng dẫn cách sửa logic cho học sinh (không cho đáp án trực tiếp).
                        """
                        ai_res = model.generate_content(ai_prompt)
                        st.markdown(ai_res.text)
                        
                except Exception as e:
                    st.error(f"⚠️ Không thể kết nối đến máy chấm: {e}")

# ================= TAB 2: HỎI ĐÁP & DEBUG TỰ DO =================
with tab2:
    st.subheader("💬 Trợ Lý AI Giải Đáp & Debug Code")
    user_query = st.text_area("Nhập câu hỏi hoặc dán code cần giải thích:", height=150)
    
    if st.button("🚀 Hỏi AI", key="btn_ask"):
        if user_query:
            response = model.generate_content(user_query, stream=True)
            st.write_stream(chunk.text for chunk in response)
