import PyInstaller.__main__
import customtkinter
import os
import shutil

# 1. CustomTkinter kütüphanesinin dosya yolunu buluyoruz
ctk_path = os.path.dirname(customtkinter.__file__)
print(f"CustomTkinter Yolu Bulundu: {ctk_path}")

# İkon dosyasının adı (Adım 1'de oluşturduğumuz)
icon_file = 'MyIcon.icns'

# İkon dosyası var mı kontrol edelim
if not os.path.exists(icon_file):
    print(f"HATA: '{icon_file}' bulunamadı! Lütfen önce ikonu dönüştürün.")
    exit(1)

# 2. PyInstaller komutlarını hazırlıyoruz
PyInstaller.__main__.run([
    'summerizer.py',                       # Senin ana dosyanın adı
    '--name=YouTubeAIApp',           # Uygulamanın adı (Türkçe karakter kullanmamaya çalış)
    '--windowed',                    # Konsol penceresi açılmasın
    '--onedir',                      # Klasör olarak çıkar
    '--clean',                       # Önbelleği temizle
    '--noconfirm',                   # Klasör varsa sormadan üzerine yaz
    f'--add-data={ctk_path}:customtkinter', # Tema dosyalarını ekle
    f'--icon={icon_file}',           # --- YENİ EKLENEN SATIR ---
])

print("\n✅ Derleme Tamamlandı!")
print(f"📂 Uygulaman '{icon_file}' ikonu ile birlikte 'dist/YouTubeAIApp' klasöründe seni bekliyor.")