import streamlit as st
import base64
import numpy as np
import math

# --- 1. AYARLAR VE VERİLER ---
st.set_page_config(page_title="AKILLI KALKAN", page_icon="🛡️")

# Sınıf Listesi (7B ve 7D Birleşik)
SINIF_LISTESI = [
    "ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI", "YASIN ERDOĞAN",
    "MUSTAFA EFE BAYSAL", "NASIF EMRE GÖZÜKÜÇÜK", "ALTAN ÖZTÜRK", "YİCIT ALI MERT",
    "ZEYNEP BEREKETLİ", "ONUR KAAN ÖZYURT", "ECE SU KAYA", "EGEHAN KUDDAR", "ELA YILDIRIM",
    "ELISA BAL", "FADİME HİRANUR AYKÜL", "HATİCE KARAKAŞ", "HAVVA SİZGEN", "MAHMUD SAMİ SİÇRAMAZ",
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
    'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252,
    'I': 73, 'i': 105
}
MATRIS_SABITLERI = [1, 2, 4, 3]

# --- 2. FONKSİYONLAR ---
def get_ascii(char):
    return KARAKTER_HARITASI.get(char, ord(char))

def anahtar_uret(isim):
    sadece_isim = isim.split()[0]
    toplam = sum(get_ascii(h) * (i+1) for i, h in enumerate(sadece_isim))
    return toplam % 256

def matris_olustur(anahtar):
    hucreler = [(s + anahtar) % 10 for s in MATRIS_SABITLERI]
    return np.array(hucreler).reshape(2, 2)

def ters_matris_moduler(matris, mod=256):
    det = int(round(np.linalg.det(matris))) % mod
    try:
        det_inv = pow(det, -1, mod)
        a, b, c, d = matris[0,0], matris[0,1], matris[1,0], matris[1,1]
        adj = np.array([[d, -b], [-c, a]])
        return (det_inv * adj) % mod
    except: return None

# --- 3. ARAYÜZ TASARIMI ---
st.title("🛡️ AKILLI KALKAN")

# BAŞLIĞI SATIRLARA BÖLDÜK
st.markdown("""
### TÜBİTAK 2204-B Projesi
#### Türkçe Karakter Destekli
##### 2025 Adana
---
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔒 Şifrele", "🔓 Şifre Çöz"])

with tab1:
    st.header("Mesaj Şifreleme")
    secilen_ogrenci = st.selectbox("1. Anahtar Öğrenciyi Seçin", sorted(list(set(SINIF_LISTESI))), key="sifrele_secim")
    mesaj = st.text_area("2. Mesajınızı Girin", height=100)
    
    if st.button("ŞİFRELE", type="primary"):
        if mesaj:
            anahtar = anahtar_uret(secilen_ogrenci)
            matris = matris_olustur(anahtar)
            v = [get_ascii(c) for c in mesaj]
            s1 = [x ^ anahtar for x in v]
            if len(s1) % 2 != 0: s1.append(0)
            s2 = []
            for i in range(0, len(s1), 2):
                vek = np.array([[s1[i]], [s1[i+1]]])
                s2.extend((np.dot(matris, vek) % 256).flatten().astype(int))
            s3 = [((x << 2) | (x >> 6)) & 0xFF for x in s2]
            cikti = base64.b64encode(bytes(s3)).decode('utf-8')
            st.success("Şifreleme Başarılı!")
            st.code(cikti)
        else:
            st.error("Mesaj girmediniz!")

with tab2:
    st.header("Tersine Mühendislik")
    coz_ogrenci = st.selectbox("1. Anahtar Öğrenciyi Seçin", sorted(list(set(SINIF_LISTESI))), key="coz_secim")
    sifreli_kod = st.text_area("2. Base64 Kodunu Yapıştırın")
    
    if st.button("ŞİFREYİ ÇÖZ", type="secondary"):
        if sifreli_kod:
            try:
                anahtar = anahtar_uret(coz_ogrenci)
                matris = matris_olustur(anahtar)
                t_mat = ters_matris_moduler(matris)
                if t_mat is not None:
                    ham_veri = list(base64.b64decode(sifreli_kod))
                    t1 = [((x >> 2) | (x << 6)) & 0xFF for x in ham_veri]
                    t2 = []
                    for i in range(0, len(t1), 2):
                        vek = np.array([[t1[i]], [t1[i+1]]])
                        t2.extend((np.dot(t_mat, vek) % 256).flatten().astype(int))
                    t3 = [x ^ anahtar for x in t2]
                    cozulen = ""
                    for val in t3:
                        if val != 0:
                            found = False
                            for k, v in KARAKTER_HARITASI.items():
                                if v == val:
                                    cozulen += k
                                    found = True
                                    break
                            if not found: cozulen += chr(val)
                    st.success("Mesaj Çözüldü!")
                    st.markdown(f"### {cozulen}")
                else:
                    st.error("Bu isimle şifre çözülemez (Matris hatası).")
            except:
                st.error("Kod geçersiz!")