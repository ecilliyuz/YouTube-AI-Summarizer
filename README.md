# YouTube AI Summarizer

A beautiful desktop application that uses Google Gemini AI to summarize YouTube videos. Simply paste a YouTube link and get an AI-powered summary or key moments extraction in Turkish.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- 🎥 **YouTube Video Summarization** - Paste any YouTube link and get an AI-generated summary
- 🔑 **Key Moments Extraction** - Extract the most important moments from videos
- 🌊 **Real-time Streaming** - Watch the AI response appear in real-time
- 🎨 **Modern Glass UI** - Beautiful dark theme with glassmorphism design
- 📱 **Responsive Design** - Window resizes gracefully
- 🇹🇷 **Turkish Output** - Summaries are generated in Turkish

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/youtube-ai-summarizer.git
   cd youtube-ai-summarizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python summerizer.py
   ```

## 📦 Dependencies

```
customtkinter
youtube-transcript-api
google-genai
python-dotenv
```

## 🔧 Building a Standalone App (macOS)

You can compile this application into a standalone `.app` bundle using PyInstaller.

### Step 1: Create an Application Icon

First, prepare a 1024x1024 PNG image named `app_icon.png`, then run these commands to create a macOS icon:

```bash
# Create a temporary icon folder
mkdir MyIcon.iconset

# Generate required icon sizes
sips -z 16 16     app_icon.png --out MyIcon.iconset/icon_16x16.png
sips -z 32 32     app_icon.png --out MyIcon.iconset/icon_16x16@2x.png
sips -z 32 32     app_icon.png --out MyIcon.iconset/icon_32x32.png
sips -z 64 64     app_icon.png --out MyIcon.iconset/icon_32x32@2x.png
sips -z 128 128   app_icon.png --out MyIcon.iconset/icon_128x128.png
sips -z 256 256   app_icon.png --out MyIcon.iconset/icon_128x128@2x.png
sips -z 256 256   app_icon.png --out MyIcon.iconset/icon_256x256.png
sips -z 512 512   app_icon.png --out MyIcon.iconset/icon_256x256@2x.png
sips -z 512 512   app_icon.png --out MyIcon.iconset/icon_512x512.png
sips -z 1024 1024 app_icon.png --out MyIcon.iconset/icon_512x512@2x.png

# Convert to .icns format
iconutil -c icns MyIcon.iconset

# Clean up temporary folder
rm -R MyIcon.iconset
```

This will create `MyIcon.icns` in your project directory.

### Step 2: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 3: Run the Build Script

```bash
python derle.py
```

The `derle.py` script handles:
- Locating CustomTkinter theme files and bundling them
- Setting the application icon
- Creating a windowed (no console) application
- Outputting to `dist/YouTubeAIApp`

### Step 4: Run Your App

After building, you'll find your application at:
```
dist/YouTubeAIApp/YouTubeAIApp.app
```

Double-click to run, or drag it to your Applications folder!

## 📁 Project Structure

```
youtube-ai-summarizer/
├── summerizer.py      # Main application
├── derle.py           # PyInstaller build script
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
├── .env               # Your API key (not in git)
├── .gitignore         # Git ignore rules
├── app_icon.png       # Source icon (1024x1024)
├── MyIcon.icns        # Compiled macOS icon
└── README.md          # This file
```

## 🎮 Usage

1. Launch the application
2. Paste a YouTube video URL into the input field
3. Select mode: **Özet** (Summary) or **Önemli Anlar** (Key Moments)
4. Press **Enter** or click the 🚀 button
5. Watch as the AI-generated content streams in real-time

## ⚠️ Notes

- Videos must have subtitles/transcripts available (auto-generated or manual)
- The AI output is in Turkish by default
- Long videos may take more time to process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) and [Google Gemini](https://ai.google.dev/)
# YouTube-AI-Summarizer
# YouTube-AI-Summarizer
# YouTube-AI-Summarizer
