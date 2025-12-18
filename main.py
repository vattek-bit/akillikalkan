import streamlit as st
import base64
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(page_title="AKILLI KALKAN", page_icon="🛡️")

# Hata payını sıfırlamak için listeyi ve haritayı en sade hale getirdik
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
    'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252, 'I': 73, 'i': 105
}

def get_ascii(char):
    return KARAKTER_HARITASI.get(char, ord(char))

def anahtar_uret(isim):
    ad = isim.split()[0]
    return sum(get_ascii(h) * (i+1) for i, h in enumerate(ad)) % 256

def matris_olustur(anahtar):
    # Sabitleri [1, 2, 4, 3] olarak kullanıyoruz
    sabitler = [1, 2, 4, 3]
    hucreler = [(s + anahtar) % 10 for s in sabitler]
    return np.array(hucreler).reshape(2, 2)

# --- 2. ARAYÜZ ---
st.title("🛡️ AKILLI KALKAN")
st.markdown("### TÜBİTAK 2204-B Projesi\n#### Türkçe Karakter Destekli\n##### 2025 Adana\n---")

tab1, tab2 = st.tabs(["🔒 Şifrele", "🔓 Şifre Çöz"])

with tab1:
    st.subheader("Şifreleme Ekranı")
    secim = st.selectbox("Anahtar Öğrenci", sorted(list(set(SINIF_LISTESI))), key="s1")
    mesaj = st.text_input("Şifrelenecek Mesaj")
    
    if st.button("ŞİFRELE", type="primary"):
        if mesaj:
            anahtar = anahtar_uret(secim)
            matris = matris_olustur(anahtar)
            # XOR
            v = [get_ascii(c) for c in mesaj]
            s1 = [x ^ anahtar for x in v]
            if len(s1) % 2 != 0: s1.append(0)
            # Matris
            s2 = []
            for i in range(0, len(s1), 2):
                vek = np.array([[s1[i]], [s1[i+1]]])
                carpim = np.dot(matris, vek) % 256
                s2.extend(carpim.flatten().astype(int))
            # Bit Kaydırma
            s3 = [((x << 2) | (x >> 6)) & 0xFF for x in s2]
            sonuc = base64.b64encode(bytes(s3)).decode()
            st.success("Sonuç:")
            st.code(sonuc)

with tab2:
    st.subheader("Şifre Çözme Ekranı")
    secim_c = st.selectbox("Anahtar Öğrenci", sorted(list(set(SINIF_LISTESI))), key="c1")
    kod = st.text_input("Base64 Kodu")
    
    if st.button("ÇÖZ"):
        if kod:
            try:
                anahtar = anahtar_uret(secim_c)
                matris = matris_olustur(anahtar)
                # Ters Matris
                det = int(round(np.linalg.det(matris))) % 256
                det_inv = pow(det, -1, 256)
                adj = np.array([[matris[1,1], -matris[0,1]], [-matris[1,0], matris[0,0]]])
                t_mat = (det_inv * adj) % 256
                
                # İşlemler
                veri = list(base64.b64decode(kod))
                # Ters Bit
                t1 = [((x >> 2) | (x << 6)) & 0xFF for x in veri]
                # Ters Matris
                t2 = []
                for i in range(0, len(t1), 2):
                    vek = np.array([[t1[i]], [t1[i+1]]])
                    carpim = np.dot(t_mat, vek) % 256
                    t2.extend(carpim.flatten().astype(int))
                # Ters XOR
                t3 = [x ^ anahtar for x in t2]
                
                cozulen = "".join([next((k for k, v in KARAKTER_HARITASI.items() if v == val), chr(val)) for val in t3 if val != 0])
                st.success(f"Mesaj: {cozulen}")
            except:
                st.error("Hata! Bu isimle veya kodla çözülemiyor.")