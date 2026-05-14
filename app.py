from flask import Flask, render_template, request, send_file
from PIL import Image, ImageOps
from datetime import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        template = Image.open("template.jpg").convert("RGB")

        slots = {
            "photo1": (60, 60, 880, 520),
            "photo2": (60, 610, 520, 520),
            "photo3": (610, 610, 330, 330),
        }

        for name, slot in slots.items():
            photo = request.files[name]

            if photo.filename == "":
                return f"{name} empty"

            filepath = os.path.join(UPLOAD_FOLDER, photo.filename)
            photo.save(filepath)

            img = Image.open(filepath).convert("RGB")
            x, y, w, h = slot

            img = ImageOps.fit(img, (w, h))
            template.paste(img, (x, y))

        filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        template.save(output_path)

        return render_template("submitted.html")

    return render_template("index.html")


@app.route("/admin")
def admin():
    files = []

    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            files.append(filename)

    files.sort(reverse=True)

    return render_template("admin.html", files=files)


@app.route("/image/<filename>")
def image(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)