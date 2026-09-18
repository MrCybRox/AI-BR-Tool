"""
Darkroom — AI Photo Tools backend.

Endpoints:
  POST /api/remove-bg   -> real AI background removal (rembg / U2-Net)
  POST /api/upscale     -> resampled + sharpened upscale

Run:
  pip install -r requirements.txt
  python app.py
Then open http://localhost:5000
"""

import os
import tempfile

# Windows Store Python installs live in a sandboxed folder that numba
# (used internally by rembg) can't write its JIT cache into. Point it
# somewhere writable before rembg is imported.
os.environ.setdefault("NUMBA_CACHE_DIR", os.path.join(tempfile.gettempdir(), "numba_cache"))
os.makedirs(os.environ["NUMBA_CACHE_DIR"], exist_ok=True)

from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image, ImageFilter
from rembg import remove
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    input_bytes = file.read()

    if len(input_bytes) > MAX_FILE_SIZE:
        return jsonify({"error": "File too large (max 10MB)"}), 400

    try:
        output_bytes = remove(input_bytes)
    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500

    return send_file(
        io.BytesIO(output_bytes),
        mimetype="image/png",
        as_attachment=False,
        download_name="background-removed.png",
    )


@app.route("/api/upscale", methods=["POST"])
def upscale():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    factor = request.form.get("factor", "2")

    try:
        factor = int(factor)
        if factor not in (2, 3, 4):
            factor = 2
    except ValueError:
        factor = 2

    try:
        img = Image.open(file.stream).convert("RGB")
    except Exception:
        return jsonify({"error": "Could not read image"}), 400

    # Cap output size so requests stay reasonable
    max_dim = 4000
    new_w = min(img.width * factor, max_dim)
    new_h = min(img.height * factor, max_dim)

    upscaled = img.resize((new_w, new_h), Image.LANCZOS)
    upscaled = upscaled.filter(
        ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2)
    )

    buf = io.BytesIO()
    upscaled.save(buf, format="PNG")
    buf.seek(0)

    return send_file(
        buf, mimetype="image/png", as_attachment=False, download_name="upscaled.png"
    )


if __name__ == "__main__":
    expected_template = os.path.join(BASE_DIR, "templates", "index.html")
    print(f"Looking for template at: {expected_template}")
    if not os.path.isfile(expected_template):
        print("!! NOT FOUND. Make sure index.html is inside a 'templates' folder")
        print(f"!! sitting right next to app.py, i.e. at exactly the path above.")
        print(f"!! Files currently in that folder: {os.listdir(os.path.join(BASE_DIR, 'templates')) if os.path.isdir(os.path.join(BASE_DIR, 'templates')) else 'templates folder does not exist!'}")
    else:
        print("Found it. Starting server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
