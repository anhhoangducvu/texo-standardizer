import streamlit as st
import io
import docx
from texo_gov_standard import apply_nd30_standard
from texo_internal_standard import apply_texo_internal_standard

# Cấu hình giao diện
st.set_page_config(page_title="TEXO Standardizer", page_icon="📄", layout="centered")

st.title("🛡️ HỆ THỐNG CHUẨN HÓA VĂN BẢN TEXO")
st.markdown("---")

# 1. Tải file Word lên
uploaded_file = st.file_uploader("Kéo thả file Word (.docx) của bạn vào đây", type=["docx"])

# 2. Thanh bên (Sidebar) để chọn chuẩn
st.sidebar.header("Cài đặt chuẩn hóa")
mode = st.sidebar.selectbox("Chọn chuẩn văn bản:", ["Nghị định 30/2020", "Nội bộ TEXO"])

is_letterhead = False
if mode == "Nội bộ TEXO":
    paper_choice = st.sidebar.radio("Sử dụng loại giấy:", ["Giấy thường", "Giấy Letterhead (có logo chìm)"])
    is_letterhead = (paper_choice == "Giấy Letterhead (có logo chìm)")

# 3. Nút bấm bắt đầu chuẩn hóa
if uploaded_file:
    if st.button("🚀 Bắt đầu chuẩn hóa ngay"):
        with st.spinner("Đang xử lý văn bản..."):
            try:
                # Đọc dữ liệu từ file upload
                input_stream = io.BytesIO(uploaded_file.getvalue())
                output_stream = io.BytesIO()

                # Gọi hàm xử lý tương ứng
                if mode == "Nghị định 30/2020":
                    # Lưu ý: Cần chỉnh một chút trong 2 file .py để nhận stream thay vì path, hoặc dùng file tạm
                    # Để đơn giản nhất, ta dùng file tạm trên cloud:
                    with open("temp_input.docx", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    if mode == "Nghị định 30/2020":
                        apply_nd30_standard("temp_input.docx", "temp_output.docx")
                    else:
                        apply_texo_internal_standard("temp_input.docx", "temp_output.docx", is_letterhead=is_letterhead)

                    # Đọc kết quả từ file tạm trả về cho người dùng
                    with open("temp_output.docx", "rb") as f:
                        st.download_button(
                            label="📥 Tải Văn bản đã chuẩn hóa (.docx)",
                            data=f,
                            file_name=f"Standardized_{uploaded_file.name}",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    st.success("✅ Chuẩn hóa thành công! Hãy tải file của bạn bên trên.")
            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {e}")
else:
    st.info("💡 Bạn hãy tải file lên để bắt đầu.")
