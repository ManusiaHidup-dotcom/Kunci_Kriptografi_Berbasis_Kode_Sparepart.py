import streamlit as st

# --- FUNGSI KRIPTOGRAFI ---
def char_to_num(text):
    """Mengubah huruf menjadi angka A=0, B=1, dst. Angka tetap angka."""
    text = text.upper().replace("-", "")
    result = []
    for char in text:
        if char.isalpha():
            result.append(str(ord(char) - ord('A')))
        elif char.isdigit():
            result.append(char)
    return ",".join(result)

def encrypt_message(plaintext, k1, k2, k3):
    plaintext = plaintext.upper().replace(" ", "")
    result = []
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        ka = k1[i % len(k1)]
        kb = k2[i % len(k2)]
        
        c2 = (p + ka + kb) % 26
        
        n1 = str(c2 + k3[0]).zfill(2)
        n2 = str(c2 + k3[1]).zfill(2)
        n3 = str(c2 + k3[2]).zfill(2)
        result.append(f"{n1}{n2}{n3}")
    return " ".join(result)

def decrypt_message(ciphertext, k1, k2, k3):
    try:
        blocks = ciphertext.split()
        decrypted_text = ""
        for i, block in enumerate(blocks):
            val = int(block[:2]) - k3[0]
            ka = k1[i % len(k1)]
            kb = k2[i % len(k2)]
            p_val = (val - ka - kb) % 26
            decrypted_text += chr(p_val + ord('A'))
        return decrypted_text
    except:
        return "Format Error: Pastikan deret angka dan kunci benar."

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Kripto Sparepart", page_icon="⚙️")

st.title("⚙️ Aplikasi Enkripsi Berbasis Kode Sparepart")
st.markdown("Simulasi kriptografi menggunakan kunci **KODE SPAREPART KENDARAAN**")

st.warning("⚠️ **Perhatian!** Metode ini hanya bekerja pada kode sparepart yang memiliki 3 blok utama (Contoh: 31600-KG1-920).")

# --- FITUR BARU: AUTO CONVERTER ---
with st.expander("🔍 Tool: Konversi Kode ke Angka (Gunakan ini untuk mengisi kunci)"):
    st.write("Masukkan kode sparepart per blok untuk mendapatkan deret angkanya.")
    input_kode = st.text_input("Contoh: Ketik 'KG1' atau '31600'", "")
    if input_kode:
        hasil_konversi = char_to_num(input_kode)
        st.info(f"Deret Angka: **{hasil_konversi}**")
        st.caption("Copy angka di atas dan tempelkan ke konfigurasi kunci di samping.")

# Sidebar untuk Kunci
st.sidebar.header("Konfigurasi Kunci")
st.sidebar.info("Gunakan koma (,) untuk memisahkan angka kunci.")

k1_input = st.sidebar.text_input("Kunci A (Blok Pertama)", "3,1,6,0,0")
k2_input = st.sidebar.text_input("Kunci B (Blok Kedua)", "10,6,1")
k3_input = st.sidebar.text_input("Kunci C (Blok Ketiga)", "9,2,0")

# Parsing Kunci
try:
    k1 = [int(x) for x in k1_input.split(",")]
    k2 = [int(x) for x in k2_input.split(",")]
    k3 = [int(x) for x in k3_input.split(",")]
except:
    st.sidebar.error("Input kunci harus berupa angka dan dipisahkan koma!")

tab1, tab2 = st.tabs(["Enkripsi", "Dekripsi"])

with tab1:
    msg = st.text_input("Masukkan Pesan (Plaintext):", "HALO")
    if st.button("Enkripsi Sekarang"):
        hasil = encrypt_message(msg, k1, k2, k3)
        st.success(f"Hasil Enkripsi: {hasil}")
        st.code(hasil)

with tab2:
    code = st.text_area("Masukkan Deret Angka (Ciphertext):")
    if st.button("Dekripsi Sekarang"):
        asli = decrypt_message(code, k1, k2, k3)
        st.info(f"Pesan Asli: {asli}")

st.divider()
st.caption("Dibuat oleh Yudhistira Baskoro Adi Admojo 24.83.1094")
