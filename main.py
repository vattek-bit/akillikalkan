import streamlit as st
import base64
import numpy as np
import math

# --- 1. AYARLAR VE VERİLER ---
st.set_page_config(page_title="Akıllı Kalkan", page_icon="🛡️")

# LİSTEYİ TÜRKÇE KARAKTERLERLE GÜNCELLEDİM
VARSAYILAN_LISTE = [
    "ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI",
    "YASİN ERDOĞAN", "MUSTAFA EFE BAYSAL", "NASIF EMRE GÖZÜKÜÇÜK", "ALTAN ÖZTÜRK",
    "ZEYNEP BEREKETLİ", "ONUR KAAN ÖZYURT", "ECE SU KAYA", "EGEHAN KUDDAR",
    "ELA YILDIRIM", "ELİSA BAL", "FADİME HİRANUR AYKÜL", "HATİCE KARAKAŞ",
    "HAVVA SİZGEN", "MAHMUD SAMİ SIÇRAMAZ", "İSA ALPEREN DURUKAN", "BAYRAM DEMİRKESER",
    "MELİSANUR TELEK", "MİNE DURU UZUN", "MİRAÇ CAN TARAÇ", "MUHAMMED ALİ KILINÇ",
    "FEDYE ÖMERİ", "ŞADİYE GÜL KUŞDEMİR", "TUANA SUNA YALÇIN", "YAĞMUR ÇETİN",
    "YAHYA NEBİ ERDOĞAN", "ZELİHA ŞİFA KILIÇ", "SIDIKA SILA DAĞ", "ALİ BATIN ÇETİN",
    "PERİHAN CİVELEK", "ELİF ÜLKÜ AKDENİZ", "DİLANUR SARIKAYA", "EMİR ŞAHİN",
    "SÜLEYMAN KUŞCU", "BERKAY ALP SİVRİDAĞ"
]

# Türkçe karakterlerin matematiksel değerleri (Proje Raporuna Uygun)
KARAKTER_HARITASI = {
    'Ç': 199, 'Ğ': 208, 'İ': 221, 'Ö': 214, 'Ş': 222, 'Ü': 220,
    'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252,
    'I': 73, 'i': 105
}
MATRIS_SABITLERI = [1, 2, 4, 3]

# --- 2. FONKSİYONLAR ---
def get_ascii(char):
    # Eğer harf haritada varsa özel değerini al, yoksa standart değerini al
    return KARAKTER_HARITASI.get(char, ord(char))

def anahtar_uret(isim):
    sadece_isim = isim.split()[0]
    # Harfleri tek tek matematiksel değere çevirip konumuyla çarpıyoruz
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
st.title("🛡️ Akıllı Kalkan")
st.markdown("**TÜBİTAK 2204-B Projesi - Türkçe Karakter Destekli**")

# Sekmeler (Tablar)
tab1, tab2 = st.tabs(["🔒 Şifrele", "🔓 Şifre Çöz"])

# -- SEKME 1: ŞİFRELEME --
with tab1:
    st.header("Mesaj Şifreleme")
    
    # 1. Adım: Öğrenci Seçimi
    secilen_ogrenci = st.selectbox("1. Anahtar Öğrenciyi Seçin", VARSAYILAN_LISTE, key="sifrele_secim")
    
    # 2. Adım: Mesaj Girişi
    mesaj = st.text_area("2. Mesajınızı Girin", height=100, placeholder="Örn: MERHABA DÜNYA")
    
    if st.button("ŞİFRELE", type="primary"):
        if not mesaj:
            st.error("Lütfen bir mesaj yazın!")
        else:
            # Algoritma
            anahtar = anahtar_uret(secilen_ogrenci)
            matris = matris_olustur(anahtar)
            
            # İşlemler
            v = [get_ascii(c) for c in mesaj]
            s1 = [x ^ anahtar for x in v]
            if len(s1) % 2 != 0: s1.append(0) # Padding
            
            s2 = []
            for i in range(0, len(s1), 2):
                vek = np.array([[s1[i]], [s1[i+1]]])
                s2.extend((np.dot(matris, vek) % 256).flatten().astype(int))
            
            s3 = [((x << 2) | (x >> 6)) & 0xFF for x in s2]
            cikti = base64.b64encode(bytes(s3)).decode('utf-8')
            
            st.success("Şifreleme Başarılı!")
            st.code(cikti, language="text")
            st.info(f"Anahtar (Tuz): {anahtar} | Seçilen: {secilen_ogrenci}")

# -- SEKME 2: ŞİFRE ÇÖZME --
with tab2:
    st.header("Tersine Mühendislik")
    
    # 1. Adım: Öğrenci Seçimi
    coz_ogrenci = st.selectbox("1. Anahtar Öğrenciyi Seçin", VARSAYILAN_LISTE, key="coz_secim")
    
    # 2. Adım: Şifreli Kod Girişi
    sifreli_kod = st.text_area("2. Base64 Kodunu Yapıştırın", height=100)
    
    if st.button("ŞİFREYİ ÇÖZ", type="secondary"):
        if not sifreli_kod:
            st.error("Lütfen şifreli kodu yapıştırın!")
        else:
            try:
                anahtar = anahtar_uret(coz_ogrenci)
                matris = matris_olustur(anahtar)
                t_mat = ters_matris_moduler(matris)
                
                if t_mat is None:
                    st.error("HATA: Bu öğrenci ismiyle matrisin tersi alınamıyor (Determinant sorunu).")
                else:
                    # Çözme Algoritması
                    ham_veri = list(base64.b64decode(sifreli_kod))
                    t1 = [((x >> 2) | (x << 6)) & 0xFF for x in ham_veri]
                    
                    t2 = []
                    for i in range(0, len(t1), 2):
                        vek = np.array([[t1[i]], [t1[i+1]]])
                        t2.extend((np.dot(t_mat, vek) % 256).flatten().astype(int))
                    
                    t3 = [x ^ anahtar for x in t2]
                    
                    # ASCII'den Karaktere (Ters Harita)
                    cozulen = ""
                    for val in t3:
                        if val != 0:
                            bulundu = False
                            for k, v in KARAKTER_HARITASI.items():
                                if v == val:
                                    cozulen += k
                                    bulundu = True
                                    break
                            if not bulundu: cozulen += chr(val)
                    
                    st.success("Mesaj Çözüldü!")
                    st.markdown(f"### {cozulen}")
            except Exception as e:
                st.error(f"Hata oluştu: Kod hatalı olabilir. ({e})")