# Darkroom — AI Photo Tools

Teen tools ek website mein:
- **Background Remover** — real AI model (rembg / U2-Net) server pe chalta hai, bilkul free & open-source, koi API key nahi chahiye
- **Compressor** — poori tarah browser mein chalta hai, kuch upload nahi hota
- **Upscaler** — image ko bara kar ke sharpen karta hai (server pe)

## Setup (apne computer ya server pe)

1. Python 3.9+ install hona chahiye.

2. Terminal mein project folder mein jayein:
   ```bash
   cd ai-tools-website
   ```

3. Virtual environment banayein (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

4. Packages install karein:
   ```bash
   pip install -r requirements.txt
   ```
   Pehli dafa `rembg` chalne par ye apna AI model (~176MB) download karega — internet chahiye hoga sirf ek dafa.

5. Server chalayein:
   ```bash
   python app.py
   ```

6. Browser mein kholein: **http://localhost:5000**

## Apni website pe deploy karna

- **Render / Railway / PythonAnywhere** — sab se aasan, free tier available hai, seedha yahi code upload kar dein.
- **VPS (DigitalOcean, Hostinger, etc.)** — Gunicorn + Nginx ke sath production mein chalayein:
  ```bash
  gunicorn -w 2 -b 0.0.0.0:8000 app:app
  ```
- Agar aap ki website WordPress ya kisi aur system pe hai, to ye Flask app ko subdomain (jaise `tools.aapkiwebsite.com`) pe alag se host kar dein aur main site se link kar dein.

## Aage kya badha saktay hain

- User accounts / usage limits
- Batch processing (multiple images ek sath)
- Zyada tools: image cropper, format converter, watermark remover
- `rembg` ke alternative models (u2netp — halka/tez version, chote servers ke liye behtar)

## Note

- Background remover aur upscaler ke liye server chalna zaroori hai (Python/Flask).
- Agar traffic zyada ho to server ki RAM kam se kam 2GB honi chahiye (AI model load karne ke liye).
