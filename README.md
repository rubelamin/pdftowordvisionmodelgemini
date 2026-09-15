# 📝 Gemini Vision - High-Quality PDF to Word Converter

An advanced, high-speed Python web application that utilizes the **Gemini 3.8 Flash Vision Model** to accurately transcribe text from scanned, low-quality, or dusty PDFs and export them directly into editable Microsoft Word (`.docx`) files.

Unlike traditional PyMuPDF or open-source OCR tools (like Tesseract), this project leverages the contextual intelligence of Gemini AI to understand full-sentence structures, preserving absolute text layout, formatting, and spelling accuracy.

---

## ✨ Features

- **Vision-Based OCR Approach:** Converts PDF pages to high-resolution images before extraction.
- **🌍 Multi-Language Support:** Automatically detects and transcribes multiple languages flawlessly (English, Bengali, Arabic, Spanish, Hindi, etc.) without translating them.
- **Paid Speed Mode (No Rate Limits):** Zero delay, optimized for fast and bulk extraction.
- **Contextual Correction:** Understands low-quality or dusty text and contextually transcribes it like a human.
- **One-Click Word Export:** Creates and downloads structured `.docx` files directly from memory.
- **Secure Environment:** Keeps your Gemini API keys safe using `.env` configurations.

---

## 🛠️ Prerequisites & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rubelamin/pdftowordvisionmodelgemini.git
cd YOUR_REPOSITORY_NAME
```

### 2. Set Up a Virtual Environment

**For Windows:**

```bash
python -m venv .venv
source .venv\Scripts\activate
```

**For Mac / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Install Poppler (Required for `pdf2image`)

This application requires **Poppler** to convert PDF pages into images.

- **Windows:**
  1. Download the latest binary zip from [here](https://github.com/oschwartz10612/poppler-windows/releases).
  2. Extract it and move the folder to `C:\poppler`.
  3. Ensure the binary path `C:\poppler\Library\bin` matches the path in `server.py`.
- **Mac (Using Homebrew):**
  ```bash
  brew install poppler
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get install poppler-utils
  ```

---

## 🔑 Getting Your Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/)** and log in with your Google account.
2. Click on **"Get API key"** and select **"Create API Key"**.
3. _Optional for Paid Speed Mode:_ Click on **"Set up billing"** / **"Upgrade to Paid Tier"** and link your credit card to activate the high-speed tier.
4. Copy your API Key.
5. Create a file named `.env` in the root directory of this project and add your key:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```

---

## 🚀 How to Run the Application

Execute the following command in your terminal:

```bash
python server.py
```

_Note: For Mac/Linux, you might need to use `python3 server.py`._

Once running, open your web browser and go to:
👉 **`http://127.0.0.1:5000`**

Upload your English PDF file, wait for the lightning-fast conversion, and click **Download Word (.docx) File**.

---

## 📦 Project Structure

```text
├── templates/
│   └── index.html      # Frontend Interface
├── server.py           # Backend Flask Server & Gemini Implementation
├── .env                # API Keys (Local Only - Hidden from GitHub)
├── .gitignore          # Tells Git what files to ignore
├── requirements.txt    # List of dependencies
└── README.md           # Documentation
```

---

## ❤️ Support My Work

If this project saved your time or helped you with your workflows, feel free to buy me a coffee! ☕

<br>

<a href="https://www.buymeacoffee.com/baghavai10G" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" style="height: 60px !important; width: 217px !important;">
</a>

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
