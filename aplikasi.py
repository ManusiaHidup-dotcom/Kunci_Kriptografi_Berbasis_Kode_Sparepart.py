import streamlit as st

# --- FUNGSI KRIPTOGRAFI ---
def encrypt_message(plaintext, k1, k2, k3):
    plaintext = plaintext.upper().replace(" ", "")
    result = []
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        ka = k1[i % len(k1)]
        kb = k2[i % len(k2)]
        
        # Vigenere Layer
        c2 = (p + ka + kb) % 26
        
        # Numerical Expansion (920)
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
            # Reduksi Numerik (Ambil salah satu hasil pengurangan)
            val = int(block[:2]) - k3[0]
            
            ka = k1[i % len(k1)]
            kb = k2[i % len(k2)]
            
            # Inverse Vigenere & Handling Negative
            p_val = (val - ka - kb) % 26
            decrypted_text += chr(p_val + ord('A'))
        return decrypted_text
    except:
        return "Format Error: Pastikan deret angka benar."

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Kripto Sparepart", page_icon="⚙️")

st.title("⚙️ Aplikasi Enkripsi Berbasis Kode Sparepart")
st.markdown("Aplikasi simulasi kriptografi menggunakan kunci **KODE SPAREPART KENDARAAN**")

# Tambahan Pesan Perhatian di Header Utama
st.warning("⚠️ **Perhatian!** Metode ini hanya bekerja pada kode sparepart yang memiliki 3 blok utama (Contoh: 31600-KG1-920).")

# Sidebar untuk Kunci (Default sesuai Makalah)
st.sidebar.header("Konfigurasi Kunci")
st.sidebar.info("Gunakan koma (,) untuk memisahkan angka kunci.")

k1_input = st.sidebar.text_input("Kunci A (Blok Pertama)", "3,1,6,0")
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
