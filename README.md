import streamlit as st
import google.generativeai as genai
import requests

# 1. CẤU HÌNH GIAO DIỆN RỘNG (WIDE LAYOUT) CHUẨN OJ
st.set_page_config(
    page_title="CPPro OJ - Hệ Thống Chấm Bài & AI Tutor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS TẠO GIAO DIỆN CHUẨN HYDROOJ / CPPRO
st.markdown("""
<style>
    /* CSS Styling giống giao diện oj.cppro.vn */
    .stApp { background-color: #0e1117; }
    .oj-title { font-size: 26px; font-weight: 700; color: #40a9ff; margin-bottom: 5px; }
    .oj-badge {
        display: inline-block; padding: 3px 10px; border-radius: 12px;
        font-size: 13px; font-weight: 600; margin-right: 8px; margin-bottom: 15px;
    }
    .badge-time { background-color: #1f293d; color: #7928ca; border: 1px solid #7928ca; }
    .badge-mem { background-color: #1f293d; color: #0070f3; border: 1px solid #0070f3; }
    .badge-easy { background-color: #1c3329; color: #50e3c2; border: 1px solid #50e3c2; }
    
    .sample-box {
        background-color: #161b22; border: 1px solid #30363d;
        border-radius: 6px; padding: 10px; font-family: monospace; font-size: 14px;
    }
    .status-ac { color: #52c41a; font-weight: bold; font-size: 20px; }
    .status-wa { color: #ff4d4f; font-weight: bold; font-size: 20px; }
</style>
""", unsafe_allow_html=True)

# 3. TỰ ĐỘNG LẤY API KEY GEMINI
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key:", type="password")

if not api_key:
    st.info("💡 Vui lòng nhập Gemini API Key ở thanh bên trái để khởi chạy OJ!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. KHO BÀI TẬP DẠNG HYDROOJ
PROBLEMS = {
    "P101": {
        "title": "P101 - Tính tổng hai số A + B",
        "time_limit": "1.0s",
        "memory_limit": "256MB",
        "difficulty": "Dễ",
        "description": "Cho hai số nguyên $A$ và $B$. Hãy tính và in ra tổng $A + B$.",
        "input_format": "Một dòng duy nhất chứa hai số nguyên $A$ và $B$ cách nhau bởi dấu cách ($-10^9 \le A, B \le 10^9$).",
        "output_format": "In ra một số nguyên duy nhất là kết quả của phép tính $A + B$.",
        "sample_input": "5 7",
        "sample_output": "12",
        "expected_output_test": "12\n"
    },
    "P102": {
        "title": "P102 - Kiểm tra số chẵn lẻ",
        "time_limit": "1.0s",
        "memory_limit": "256MB",
        "difficulty": "Dễ",
        "description": "Cho số nguyên $N$. Hãy kiểm tra xem $N$ là số chẵn hay số lẻ.",
        "input_format": "Gồm một số nguyên $N$ ($1 \le N \le 10^6$).",
        "output_format": "In ra `CHAN` nếu $N$ là số chẵn, ngược lại in ra `LE`.",
        "sample_input": "4",
        "sample_output": "CHAN",
        "expected_output_test": "CHAN\n"
    },
    "P103": {
        "title": "P103 - Tìm số lớn nhất (Max 3 số)",
        "time_limit": "1.0s",
        "memory_limit": "256MB",
        "difficulty": "Trung bình",
        "description": "Cho 3 số nguyên $A, B, C$. Hãy tìm và in ra giá trị lớn nhất trong 3 số đó.",
        "input_format": "Một dòng chứa 3 số nguyên $A, B, C$ cách nhau bởi dấu cách.",
        "output_format": "In ra giá trị lớn nhất.",
        "sample_input": "10 25 15",
        "sample_output": "25",
        "expected_output_test": "25\n"
    }
}

# 5. SIDEBAR NAVIGATION
st.sidebar.title("⚡ CPPro Online Judge")
menu = st.sidebar.radio("Điều hướng:", ["📚 Kho bài tập (Problemset)", "💬 Hỏi đáp AI Tutor"])

if menu == "📚 Kho bài tập (Problemset)":
    selected_p_code = st.sidebar.selectbox("📌 Chọn bài tập:", list(PROBLEMS.keys()), format_func=lambda x: PROBLEMS[x]["title"])
    p = PROBLEMS[selected_p_code]

    # GIAO DIỆN CHIA 2 CỘT CHUẨN ONLINE JUDGE
    col_problem, col_submit = st.columns([1, 1], gap="medium")

    # ================= CỘT TRÁI: ĐỀ BÀI (PROBLEM STATEMENT) =================
    with col_problem:
        st.markdown(f"<div class='oj-title'>{p['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <span class='oj-badge badge-time'>⏱️ Thời gian: {p['time_limit']}</span>
            <span class='oj-badge badge-mem'>💾 Bộ nhớ: {p['memory_limit']}</span>
            <span class='oj-badge badge-easy'>🎯 Độ khó: {p['difficulty']}</span>
        """, unsafe_allow_html=True)

        st.subheader("📄 Mô tả bài toán")
        st.write(p["description"])

        st.subheader("📥 Định dạng Đầu vào (Input)")
        st.write(p["input_format"])

        st.subheader("📤 Định dạng Đầu ra (Output)")
        st.write(p["output_format"])

        # Ví dụ mẫu (Sample Testcase)
        col_in, col_out = st.columns(2)
        with col_in:
            st.caption("Ví dụ Đầu vào (Sample Input):")
            st.code(p["sample_input"], language="text")
        with col_out:
            st.caption("Ví dụ Đầu ra (Sample Output):")
            st.code(p["sample_output"], language="text")

    # ================= CỘT PHẢI: TRÌNH SOẠN THẢO & NỘP BÀI =================
    with col_submit:
        st.subheader("💻 Trình nộp bài (Submit Code)")
        
        col_lang, col_theme = st.columns([2, 1])
        with col_lang:
            lang = st.selectbox("Ngôn ngữ:", ["C++ (GCC 9.2.0)", "Python (3.8.1)"])
            
        default_code = "#include <iostream>\nusing namespace std;\n\nint main() {\n    // Viết code của bạn ở đây\n    return 0;\n}" if "C++" in lang else "# Viết code Python của bạn ở đây\n"

        user_code = st.text_area("Mã nguồn:", value=default_code, height=280)

        if st.button("🚀 NỘP BÀI (SUBMIT)", type="primary", use_container_width=True):
            if not user_code:
                st.warning("⚠️ Vui lòng nhập mã nguồn!")
            else:
                with st.spinner("⚙️ Máy chấm (Judger) đang biên dịch và thực thi code..."):
                    lang_id = 71 if "Python" in lang else 54
                    url = "https://judge0-ce.p.rapidapi.com/submissions?wait=true"
                    payload = {
                        "source_code": user_code,
                        "language_id": lang_id,
                        "stdin": p["sample_input"],
                        "expected_output": p["expected_output_test"]
                    }
                    headers = {
                        "content-type": "application/json",
                        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
                        "X-RapidAPI-Key": "7f0980164fmshd1e59bf40fb2b75p16a3a9jsn972236a297b5"
                    }
                    
                    try:
                        res = requests.post(url, json=payload, headers=headers).json()
                        status = res.get("status", {}).get("description", "Unknown Error")
                        stdout = res.get("stdout", "")
                        stderr = res.get("compile_output", "") or res.get("stderr", "")

                        # KHU VỰC TRẢ KẾT QUẢ CHẤM (JUDGE RESULT)
                        st.subheader("📊 Kết quả chấm bài")
                        if status == "Accepted":
                            st.balloons()
                            st.markdown("<div class='status-ac'>🟢 ACCEPTED (100/100 pts)</div>", unsafe_allow_html=True)
                            st.success("Chúc mừng! Đã vượt qua tất cả các bộ testcase.")
                        else:
                            st.markdown(f"<div class='status-wa'>🔴 {status.upper()}</div>", unsafe_allow_html=True)
                            if stdout:
                                st.text(f"Đầu ra của bạn: {stdout.strip()}")
                                st.text(f"Đầu ra chuẩn:   {p['sample_output']}")
                            if stderr:
                                st.code(stderr, language="bash")

                            # TỰ ĐỘNG GỌI AI MENTOR GIẢI THÍCH LỖI
                            st.write("---")
                            st.subheader("🤖 AI Mentor Phân Tích Lỗi:")
                            ai_prompt = f"""
                            Học sinh làm bài: {p['title']}
                            Code ({lang}):
                            ```
                            {user_code}
                            ```
                            Lỗi từ máy chấm: {status}
                            Chi tiết lỗi: {stderr if stderr else stdout}
                            
                            Giải thích ngắn gọn lý do sai và chỉ hướng khắc phục (không cho code hoàn chỉnh).
                            """
                            response = model.generate_content(ai_prompt)
                            st.markdown(response.text)

                    except Exception as e:
                        st.error(f"⚠️ Lỗi kết nối máy chấm: {e}")

else:
    # TAB HỎI ĐÁP AI TỰ DO
    st.title("💬 Trợ Lý AI Mentor Lập Trình")
    user_query = st.text_area("Nhập thắc mắc hoặc dán đoạn code cần debug:", height=200)
    if st.button("🚀 Hỏi AI", type="primary"):
        if user_query:
            response = model.generate_content(user_query, stream=True)
            st.write_stream(chunk.text for chunk in response)
