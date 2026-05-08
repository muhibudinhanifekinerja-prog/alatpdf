import streamlit as st
from pypdf import PdfReader, PdfWriter
import img2pdf
import io

st.set_page_config(page_title="PDF Engineer Tool", layout="wide")

st.title("🛠️ PDF Engineering App")
st.markdown("Aplikasi manajemen PDF mandiri - Akses di mana saja.")

# Sidebar Menu
menu = ["Merge PDF", "Split PDF", "Gambar ke PDF", "Kompresi PDF (Basic)"]
choice = st.sidebar.selectbox("Pilih Fungsi", menu)

# --- FUNGSI MERGE PDF ---
if choice == "Merge PDF":
    st.header("🔗 Gabungkan PDF")
    files = st.file_uploader("Pilih beberapa file PDF", type="pdf", accept_multiple_files=True)
    if st.button("Proses Gabung"):
        if files:
            writer = PdfWriter()
            for f in files:
                writer.append(f)
            
            output = io.BytesIO()
            writer.write(output)
            st.download_button("📥 Download Hasil Gabungan", output.getvalue(), "merged_file.pdf")
        else:
            st.error("Silakan upload file terlebih dahulu.")

# --- FUNGSI SPLIT PDF ---
elif choice == "Split PDF":
    st.header("✂️ Pisah PDF")
    file = st.file_uploader("Pilih satu file PDF", type="pdf")
    if file:
        reader = PdfReader(file)
        page_count = len(reader.pages)
        st.write(f"Total Halaman: {page_count}")
        
        start, end = st.slider("Pilih rentang halaman", 1, page_count, (1, page_count))
        
        if st.button("Proses Pisah"):
            writer = PdfWriter()
            for i in range(start-1, end):
                writer.add_page(reader.pages[i])
            
            output = io.BytesIO()
            writer.write(output)
            st.download_button("📥 Download Halaman Terpilih", output.getvalue(), "split_file.pdf")

# --- FUNGSI GAMBAR KE PDF ---
elif choice == "Gambar ke PDF":
    st.header("🖼️ Gambar ke PDF")
    images = st.file_uploader("Pilih gambar (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if st.button("Konversi ke PDF"):
        if images:
            pdf_bytes = img2pdf.convert([img.read() for img in images])
            st.download_button("📥 Download PDF", pdf_bytes, "image_converted.pdf")

# --- FUNGSI KOMPRESI ---
elif choice == "Kompresi PDF (Basic)":
    st.header("📉 Kompresi PDF")
    file = st.file_uploader("Upload PDF untuk dikompres", type="pdf")
    if st.button("Kompres Sekarang"):
        if file:
            reader = PdfReader(file)
            writer = PdfWriter()
            for page in reader.pages:
                page.compress_content_streams()  # Kompresi konten internal
                writer.add_page(page)
            
            output = io.BytesIO()
            writer.write(output)
            st.download_button("📥 Download PDF Terkompres", output.getvalue(), "compressed.pdf")
