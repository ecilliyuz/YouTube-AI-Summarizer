import customtkinter as ctk
import threading
import re
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# --- AYARLAR ---
# .env dosyasından API Key okuma
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class GlassApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("YouTube AI Summary App")
        self.geometry("900x700")
        self.resizable(True, True)
        self.configure(fg_color="#0f0c29")  # Uzay teması arka plan

        # Gemini İstemcisi Başlatma
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            print(f"API Key Hatası: {e}")

        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # --- ANA ÇERÇEVE (Glass Effect) ---
        self.glass_frame = ctk.CTkFrame(
            self, corner_radius=30, fg_color="#1a1a2e", border_width=2, border_color="#4e4e75", bg_color="transparent"
        )
        self.glass_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        self.glass_frame.grid_columnconfigure(0, weight=1)
        self.glass_frame.grid_rowconfigure(2, weight=1) # Sadece alt kısım büyüsün (row 0:search, 1:segmented, 2:box)

        # --- ÜST KISIM: ARAMA ---
        search_container = ctk.CTkFrame(self.glass_frame, fg_color="transparent", height=80)
        search_container.grid(row=0, column=0, sticky="ew", padx=30, pady=(40, 10))

        # Giriş Kutusu (Uzun Input)
        self.link_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="YouTube linkini buraya yapıştır ve Enter'a bas...",
            height=60,
            corner_radius=20,
            font=("Arial", 16),
            fg_color="#252540",
            border_color="#5b5b8f",
            border_width=1,
            text_color="white",
        )
        self.link_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        # "Enter" tuşuna basınca işlemi başlatma (Normal ve Numpad Enter)
        self.link_entry.bind("<Return>", lambda event: self.start_thread())
        self.link_entry.bind("<KP_Enter>", lambda event: self.start_thread())

        # Buton
        search_button = ctk.CTkButton(
            search_container,
            text="🚀",
            width=60,
            height=60,
            corner_radius=20,
            font=("Arial", 24),
            fg_color="#303050",
            hover_color="#404060",
            border_color="#5b5b8f",
            border_width=1,
            command=self.start_thread,
        )
        search_button.pack(side="right")

        # --- SEÇENEKLER ---
        self.mode_var = ctk.StringVar(value="Özet")
        self.segmented_button = ctk.CTkSegmentedButton(
            self.glass_frame,
            values=["Özet", "Önemli Anlar"],
            variable=self.mode_var,
            font=("Arial", 14, "bold"),
            selected_color="#6c6cff",
            unselected_color="#252540",
            height=40
        )
        self.segmented_button.grid(row=1, column=0, pady=(0, 20))

        # --- ALT KISIM: SONUÇ KUTUSU ---
        self.summary_box = ctk.CTkFrame(self.glass_frame, corner_radius=20, fg_color="#252540", border_color="#5b5b8f", border_width=1)
        # Başlangıçta gizli
        
        # Textbox (Scroll edilebilir metin alanı)
        self.summary_textbox = ctk.CTkTextbox(self.summary_box, font=("Arial", 16), text_color="#e0e0e0", fg_color="transparent", wrap="word")
        self.summary_textbox.pack(fill="both", expand=True, padx=15, pady=15)
        self.summary_textbox.configure(state="disabled")
        
        # Bold/Header tag konfigürasyonu (Siyah yazı, beyaz arka plan - Okunabilirlik için)
        self.summary_textbox._textbox.tag_config("bold", font=("Arial", 16, "bold"), foreground="black", background="white")

    # --- ARKA PLAN İŞLEMLERİ (Thread) ---
    def start_thread(self):
        """Arayüz donmasın diye işlemi ayrı kanalda başlatır"""
        link = self.link_entry.get()
        if not link:
            return

        # Alt kısmı göster
        self.summary_box.grid(row=2, column=0, sticky="nsew", padx=30, pady=(10, 40))

        # UI Güncelleme: Yükleniyor durumu
        self.write_to_box("Video analiz ediliyor...")

        # İşlemi başlat
        threading.Thread(target=self.process_video, args=(link,), daemon=True).start()

    def process_video(self, url):
        try:
            # 1. Video ID Çek
            video_id = self.get_video_id(url)
            if not video_id:
                self.update_ui_error("Geçersiz YouTube Linki!")
                return

            # 2. Transkript İndir (Dokümana uygun yeni yöntem)
            transcript_text = self.fetch_transcript(video_id)
            if not transcript_text:
                return

            # 3. Gemini ile Özetle (Streaming)
            self.write_to_box("") # İçeriği temizle
            self.summarize_and_stream(transcript_text)

        except Exception as e:
            self.update_ui_error(f"Beklenmeyen hata: {str(e)}")

    def get_video_id(self, url):
        patterns = [r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def fetch_transcript(self, video_id):
        try:
            # --- DÜZELTME BURADA ---
            # Dokümanına göre önce sınıfı örnekliyoruz:
            ytt_api = YouTubeTranscriptApi()

            # Sonra .fetch() metodunu çağırıyoruz:
            fetched_transcript = ytt_api.fetch(video_id, languages=["tr", "en"])

            # Dönen nesne iterable (döngüye sokulabilir) olduğu için snippet.text'leri topluyoruz
            full_text = " ".join([snippet.text for snippet in fetched_transcript])

            return full_text

        except Exception as e:
            self.update_ui_error(f"Altyazı hatası: {e}\n(Video altyazıya kapalı olabilir.)")
            return None

    def summarize_and_stream(self, text):
        try:
            mode = self.mode_var.get()
            
            if mode == "Özet":
                prompt = f"""
                Aşağıdaki YouTube videosunun transkriptini Türkçe olarak, maddeler halinde ve akıcı bir dille özetle.
                Videonun ana fikrini ve en önemli çıkarımlarını belirt.
                Başlıkları **BAŞLIK İSMİ** şeklinde kalın yap. 
                Her başlıktan sonra mutlaka bir alt satıra geç ve açıklamayı altından devam ettir.

                Transkript:
                {text[:30000]} 
                """
            else: # Önemli Anlar
                prompt = f"""
                Aşağıdaki YouTube videosunun transkriptini incele ve videodaki en önemli anları (key moments) belirle.
                Her bir önemli anı başlık ve kısa bir açıklama ile Türkçe olarak listele.
                Madde işaretleri kullan.
                Başlıkları **BAŞLIK İSMİ** şeklinde kalın yap.
                Her başlıktan sonra mutlaka bir alt satıra geç ve açıklamayı altından devam ettir.

                Transkript:
                {text[:30000]} 
                """
            
            # Textbox'ı temizle ve aktif et
            self.summary_textbox.configure(state="normal")
            self.summary_textbox.delete("0.0", "end")
            
            # Stream başlat
            stream = self.client.models.generate_content_stream(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            
            # Stream ve Parslama (**markdown bold** formatı)
            full_text_buffer = ""
            is_bold = False
            
            for chunk in stream:
                if chunk.text:
                    full_text_buffer += chunk.text
                    
                    # Markdown ** parslama ve anlık yazdırma
                    while "**" in full_text_buffer:
                        parts = full_text_buffer.split("**", 1)
                        if is_bold:
                            # Bold kısım bitti
                            self.summary_textbox.insert("end", parts[0], "bold")
                            is_bold = False
                        else:
                            # Normal metin, bold başlıyor
                            self.summary_textbox.insert("end", parts[0])
                            is_bold = True
                        full_text_buffer = parts[1]
                    
                    # Eğer tag yoksa ve bold modunda değilsek buffer'ı boşalt
                    if not is_bold:
                        self.summary_textbox.insert("end", full_text_buffer)
                        full_text_buffer = ""
                    
                    self.update_idletasks()
            
            # Kalan buffer'ı yazdır
            if full_text_buffer:
                tag = "bold" if is_bold else None
                self.summary_textbox.insert("end", full_text_buffer, tag)

            self.summary_textbox.configure(state="disabled")

        except Exception as e:
            self.update_ui_error(f"Gemini Hatası: {str(e)}")

    # --- UI GÜNCELLEME YARDIMCILARI ---
    def write_to_box(self, text):
        self.summary_textbox.configure(state="normal")
        self.summary_textbox.delete("0.0", "end")
        self.summary_textbox.insert("0.0", text)
        self.summary_textbox.configure(state="disabled")

    def update_ui_success(self, text):
        self.write_to_box(text)

    def update_ui_error(self, error_msg):
        self.write_to_box(f"HATA: {error_msg}")


if __name__ == "__main__":
    app = GlassApp()
    app.mainloop()
