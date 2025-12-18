import streamlit as st
import base64
import numpy as np

# --- 1. AYARLAR VE VERİLER ---
st.set_page_config(page_title="AKILLI KALKAN", page_icon="🛡️")

SINIF_LISTESI = [
    "ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI", "YASIN ERDOĞAN",
    "MUSTAFA EFE BAYSAL", "NASIF EMRE GÖZÜKÜÇÜK", "ALTAN ÖZTÜRK", "YİCIT ALI MERT",
    "ZEYNEP BEREKETLİ", "ONUR KAAN ÖZYURT", "ECE SU KAYA", "EGEHAN KUDDAR", "ELA YILDIRIM",
    "ELİSA BAL", "FADİME HİRANUR AYKÜL", "HATİCE KARAKAŞ", "HAVVA SİZGEN", "MAHMUD SAMİ SİÇRAMAZ",
    "İSA ALPEREN DURUKAN", "İBRAHİM DA", "BAYRAM DEMİRESER", "MELİSANUR TELEK", "MİNE DURU UZUN",
    "MİRAÇ CAN TARAÇ", "MUHAMMED ALI KILINÇ", "FEDYE ÖMERİ", "ŞADİYE GÜL KUŞDEMİR",
    "TUANA SUNA YALÇIN", "YAĞMUR ÇETİN", "YAHYA NEBİ ERDOĞAN", "ZELİHA ŞİFA KILIÇ", "SİDRA KATBİ",
    "SIDIKA SILA DAĞ", "ALI BATIN ÇETİN", "PERİHAN CİVELEK", "ELİF ÜLKÜ AKDENİZ", "DİLANUR SARIKAYA",
    "EMİR ŞAHİN", "SÜLEYMAN KUŞCU", "BERKAY ALP SİVRİDAĞ", "SILA TOPAL", "AHMED HAYRI KUŞÇUTOPAL",
    "MEHMET ÇAĞLAYAN HARPUT", "BERKİN ERVA GÜLDEN", "TAHA ERDOĞAN", "ŞEHED MUSTAFA", "ESMA SAKMEN",
    "HANİFE NİSA KARIOĞLU", "NESLİHAN SU ATLI", "POYRAZ ERGE", "BERAT BOZROĞA", "BERAT YAŞAR",
    "EYLÜL KAYA", "EYLÜL AŞNAS", "GÖZDE YASDIBAŞ", "HAYDAR SALAMA", "HAYRUNNİSA GÜLTEPE",
    "YAHYA YUSUF GÖKALP", "NURMİNA ERDOĞAN", "ÖZKAN KAAN DORUK", "YUSUF EFE CAN", "RAVAN AŞUR", "SÜLEYMAN ARES DEMİREL"
]

KARAKTER_HARITASI = {
    'Ç': 199, 'Ğ': 208, 'İ': 221, 'Ö': 214, 'Ş': 222, 'Ü': 220,
    'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252, 'I': 73, 'i': 105
}

# --- 2. YARDIMCI FONKSİYONLAR ---
def get_ascii(char):
    return KARAKTER_HARITASI.get(char, ord(char))

def anahtar_uret(isim):
    ad = isim.split()[0]
    toplam = sum(get_ascii(h) * (i+1) for i, h in enumerate(ad))
    return toplam % 256

def matris_olustur(anahtar):
    sabitler = [1, 2, 4, 3] # [tek, çift, çift, tek]
    hucreler = [(s + anahtar) % 10 for s in sabitler]
    return np.array(hucreler).reshape(2, 2)

def ters_matris_hesapla(matris, mod=256):
    try:
        a, b, c, d = int(matris[0,0]), int(matris[0,1]), int(matris[1,0]), int(matris[1,1])
        det = (a * d - b * c) % mod
        det_inv = pow(det, -1, mod)
        adj = np.array([[d, -b], [-c, a]])
        return (det_inv * adj) % mod
    except:
        return None

# --- 3. ARAYÜZ (UI) ---
st.title("🛡️ AKILLI KALKAN")
st.markdown("""
### TÜBİTAK 2204-B Projesi
#### Türkçe Karakter Destekli
##### 2025 Adana
---
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔒 Şifrele", "🔓 Şifre Çöz"])

with tab1:
    st.subheader("Mesaj Şifreleme")
    ogrenci = st.selectbox("Anahtar Öğrenci Seçin", sorted(list(set(SINIF_LISTESI))), key="enc_student")
    mesaj = st.text_input("Şifrelenecek Mesajı Girin", key="enc_msg")
    
    if st.button("ŞİFRELE", type="primary"):
        if mesaj:
            anahtar = anahtar_uret(ogrenci)
            matris = matris_olustur(anahtar)
            
            # 1. XOR
            ascii_vals = [get_ascii(c) for c in mesaj]
            xor_vals = [x ^ anahtar for x in ascii_vals]
            if len(xor_vals) % 2 != 0: xor_vals.append(0)
            
            # 2. Matris Şifreleme
            matris_vals = []
            for i in range(0, len(xor_vals), 2):
                v = np.array([[xor_vals[i]], [xor_vals[i+1]]])
                res = np.dot(matris, v) % 256
                matris_vals.extend(res.flatten().astype(int))
            
            # 3. Bit Kaydırma (Sola 2)
            final_vals = [((x << 2) | (x >> 6)) & 0xFF for x in matris_vals]
            b64_sonuc = base64.b64encode(bytes(final_vals)).decode()
            
            st.success("Şifreleme Başarılı!")
            st.code(b64_sonuc)
        else:
            st.warning("Lütfen bir mesaj girin.")

with tab2:
    st.subheader("Şifre Çözme")
    ogrenci_c = st.selectbox("Anahtar Öğrenci Seçin", sorted(list(set(SINIF_LISTESI))), key="dec_student")
    kod = st.text_input("Base64 Kodunu Yapıştırın", key="dec_msg")
    
    if st.button("ŞİFREYİ ÇÖZ"):
        if kod:
            try:
                anahtar = anahtar_uret(ogrenci_c)
                matris = matris_olustur(anahtar)
                t_mat = ters_matris_hesapla(matris)
                
                if t_mat is None:
                    st.error("HATA: Seçilen isimle matris tersi alınamıyor. Başka isim deneyin.")
                else:
                    raw_data = list(base64.b64decode(kod))
                    # 1. Ters Bit Kaydırma (Sağa 2)
                    t1 = [((x >> 2) | (x << 6)) & 0xFF for x in raw_data]
                    
                    # 2. Ters Matris
                    t2 = []
                    for i in range(0, len(t1), 2):
                        v = np.array([[t1[i]], [t1[i+1]]])
                        res = np.dot(t_mat, v) % 256
                        t2.extend(res.flatten().astype(int))
                    
                    # 3. Ters XOR
                    t3 = [x ^ anahtar for x in t2]
                    
                    # ASCII -> Metin
                    cozulen_metin = ""
                    for val in t3:
                        if val != 0:
                            found = False
                            for k, v in KARAKTER_HARITASI.items():
                                if v == val:
                                    cozulen_metin += k
                                    found = True
                                    break
                            if not found: cozulen_metin += chr(val)
                    
                    st.success("Mesaj Başarıyla Çözüldü:")
                    st.header(cozulen_metin)
            except Exception as e:
                st.error("Hata: Kod geçersiz veya eksik.")
        else:
            st.warning("Lütfen şifreli kodu yapıştırın.")