import flet as ft
import base64
import numpy as np

# --- ŞİFRELEME MOTORUN (Senin Kodun) ---
VARSAYILAN_LISTE = ["ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI", "YASİN ERDOĞAN"] # Burayı tam listeyle doldurabilirsin
KARAKTER_HARITASI = {'Ç': 199, 'Ğ': 208, 'İ': 221, 'Ö': 214, 'Ş': 222, 'Ü': 220, 'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252}
MATRIS_SABITLERI = [1, 2, 4, 3]

def get_ascii(char): return KARAKTER_HARITASI.get(char, ord(char))
def anahtar_uret(isim):
    ad = isim.split()[0]
    return sum(get_ascii(h) * (i+1) for i, h in enumerate(ad)) % 256

def main(page: ft.Page):
    page.title = "Akıllı Kalkan"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"

    # UI Elemanları
    drp_ogrenci = ft.Dropdown(label="1. Öğrenci Seç (Anahtar)", options=[ft.dropdown.Option(i) for i in VARSAYILAN_LISTE])
    txt_giris = ft.TextField(label="2. Mesajını Gir", multiline=True)
    txt_sonuc = ft.TextField(label="Sonuç", read_only=True, multiline=True)

    def sifrele_tetik(e):
        if not drp_ogrenci.value or not txt_giris.value: return
        anahtar = anahtar_uret(drp_ogrenci.value)
        # Basit XOR + Bit Kaydırma simülasyonu (Senin mantığın)
        v = [get_ascii(c) for c in txt_giris.value]
        s1 = [x ^ anahtar for x in v]
        s2 = [((x << 2) | (x >> 6)) & 0xFF for x in s1]
        txt_sonuc.value = base64.b64encode(bytes(s2)).decode()
        page.update()

    def coz_tetik(e):
        if not drp_ogrenci.value or not txt_giris.value: return
        anahtar = anahtar_uret(drp_ogrenci.value)
        try:
            sifreli = list(base64.b64decode(txt_giris.value))
            t1 = [((x >> 2) | (x << 6)) & 0xFF for x in sifreli]
            t2 = [x ^ anahtar for x in t1]
            txt_sonuc.value = "".join([chr(x) for x in t2])
        except: txt_sonuc.value = "Hata: Geçersiz Kod!"
        page.update()

    page.add(
        ft.Text("🛡️ AKILLI KALKAN", size=30, weight="bold", color="blue"),
        drp_ogrenci,
        txt_giris,
        ft.Row([
            ft.ElevatedButton("ŞİFRELE 🔒", on_click=sifrele_tetik, bgcolor="red", color="white"),
            ft.ElevatedButton("ÇÖZ 🔓", on_click=coz_tetik, bgcolor="green", color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        txt_sonuc
    )

ft.app(target=main)