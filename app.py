import streamlit as st
import io
import os
import docx
# Import trực tiếp các hàm xử lý từ 2 file .py của bạn
from texo_gov_standard import apply_nd30_standard
from texo_internal_standard import apply_texo_internal_standard

# Cấu hình giao diện và tiêu đề trang
st.set_page_config(page_title="TEXO Document Standardizer", page_icon="🏢")

st.title("🛡️ HỆ THỐNG CHUẨN HÓA VĂN BẢN TEXO")
st.info("💡 Hướng dẫn: Tải file Word lên -> Chọn loại giấy -> Nhấn nút xử lý -> Tải kết quả về.")

# --- PHẦN 1: CÀI ĐẶT TRÊN THANH BÊN (SIDEBAR) ---
st.sidebar.header("⚙️ CÀI ĐẶT CHUẨN HÓA")

# Đưa Nội bộ TEXO lên làm lựa chọn mặc định đầu tiên
mode = st.sidebar.selectbox(
    "1. Chọn chuẩn văn bản:", 
    ["Nội bộ TEXO", "Nghị định 30/2020 (Nhà nước)"]
)

is_letterhead = False
if mode == "Nội bộ TEXO":
    paper_choice = st.sidebar.radio(
        "2. Loại giấy in:", 
        ["Giấy thường (20/20/30/20)", "Giấy Letterhead (40/30/30/20)"]
    )
    is_letterhead = (paper_choice == "Giấy Letterhead (40/30/30/20)")

# --- PHẦN 2: TẢI FILE VÀ XỬ LÝ ---
uploaded_file = st.file_uploader("Kéo thả file .docx vào đây", type=["docx"])

if uploaded_file:
    # Sau khi có file, hiện nút bấm bắt đầu
    if st.button("🚀 BẮT ĐẦU CHUẨN HÓA"):
        with st.spinner("Đang xử lý văn bản chuyên sâu..."):
            try:
                # Tạo tên file tạm để xử lý (Streamlit Cloud cần thao tác file trên đĩa tạm)
                in_path = "temp_input.docx"
                out_path = "temp_output.docx"
                
                # Lưu dữ liệu upload vào file tạm
                with open(in_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Gọi hàm xử lý tương ứng dựa trên lựa chọn
                if mode == "Nội bộ TEXO":
                    apply_texo_internal_standard(in_path, out_path, is_letterhead=is_letterhead)
                else:
                    apply_nd30_standard(in_path, out_path)
                
                # Đọc kết quả đã xử lý xong
                if os.path.exists(out_path):
                    with open(out_path, "rb") as f:
                        processed_data = f.read()
                        
                    # Hiện nút tải xuống
                    st.success(f"✅ Đã chuẩn hóa xong theo chuẩn: {mode}")
                    st.download_button(
                        label="📥 TẢI VỀ FILE KẾT QUẢ",
                        data=processed_data,
                        file_name=f"Standardized_{uploaded_file.name}",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                else:
                    st.error("❌ Rất tiếc, quá trình tạo file kết quả thất bại.")
                    
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống: {e}")
                st.warning("Vui lòng kiểm tra lại cấu trúc file Word của bạn.")
            finally:
                # Dọn dẹp file tạm sau khi chạy xong để tiết kiệm tài nguyên
                if os.path.exists(in_path): os.remove(in_path)
                if os.path.exists(out_path): os.remove(out_path)

st.markdown("---")
st.caption("© 2026 TEXO - Trưởng phòng kỹ thuật - Hoàng Đức Vũ")
