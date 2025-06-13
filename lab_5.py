import streamlit as st
import re

# Tiền xử lý dữ liệu từ file tần suất
def preprocess_data():
    st.write("Vui lòng tải lên tệp `giao-duc-f.txt` với định dạng: từ : số_lần")

    uploaded_file = st.file_uploader("Chọn tệp giao-duc-f.txt", type="txt", key="file_f")

    if uploaded_file is not None:
        tan_suat = {}
        error_lines = []

        for i, line in enumerate(uploaded_file):
            line = line.decode("utf-8").strip()
            spls = line.split(" : ")

            if len(spls) == 2:
                tu = spls[0]
                try:
                    so_lan = int(spls[1])
                    tan_suat[tu] = so_lan
                except ValueError:
                    error_lines.append((i + 1, line))
            else:
                error_lines.append((i + 1, line))

        if tan_suat:
            st.subheader("Kết quả tiền xử lý:")
            st.write(tan_suat)

        if error_lines:
            st.warning("Một số dòng bị sai định dạng:")
            for dong, noi_dung in error_lines:
                st.text(f"Dòng {dong}: {noi_dung}")

# Xử lý văn bản và loại bỏ stopwords
def process_text():
    st.write("Tải lên 2 tệp: `giao-duc.txt` (văn bản) và `stopwords.txt` (từ cần loại bỏ)")

    file_tho = st.file_uploader("Tải tệp giao-duc.txt", type="txt", key="file_tho")
    file_stop = st.file_uploader("Tải tệp stopwords.txt", type="txt", key="file_stop")

    if file_tho is not None and file_stop is not None:
        noi_dung = file_tho.read().decode("utf-8").lower()
        noi_dung = re.sub(r"[.,\-?:@#$%^&*()+=_`~!{}\[\]]", "", noi_dung)

        stop_words = [line.decode("utf-8").strip() for line in file_stop.readlines()]
        for word in stop_words:
            noi_dung = noi_dung.replace(f' {word} ', ' ')

        ds_tu = noi_dung.split()
        tan_suat = {}
        for tu in ds_tu:
            if tu:
                tan_suat[tu] = tan_suat.get(tu, 0) + 1

        st.subheader("Tần suất từ (đã loại bỏ stopwords):")
        st.write(tan_suat)

# Giao diện chính
def main():
    st.title("Ứng dụng Xử lý Văn Bản")

    st.sidebar.header("Chọn chức năng")
    choice = st.sidebar.selectbox("Chức năng", ["Tiền xử lý dữ liệu", "Xử lý văn bản"])

    if choice == "Tiền xử lý dữ liệu":
        st.subheader("Tiền Xử Lý Dữ Liệu")
        preprocess_data()
    elif choice == "Xử lý văn bản":
        st.subheader("Xử Lý Văn Bản")
        process_text()

# Chạy ứng dụng
if __name__ == "__main__":
    main()
