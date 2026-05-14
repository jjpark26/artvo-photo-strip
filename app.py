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
            "photo1": (150, 60, 800, 500),
            "photo2": (150, 610, 520, 520),
            "photo3": (610, 610, 330, 330),
        }

        for name, slot in slots.items():

            if name not in request.files:
                return f"{name} missing"

            photo = request.files[name]

            if photo.filename == "":
                return f"{name} empty"

            filepath = os.path.join(UPLOAD_FOLDER, photo.filename)
            photo.save(filepath)

            img = Image.open(filepath).convert("RGB")

            x, y, w, h = slot

            img = ImageOps.fit(img, (w, h))

            template.paste(img, (x, y))

        output_path = os.path.join(
            OUTPUT_FOLDER,
            f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        template.save(output_path)

        return send_file(output_path, mimetype="image/jpeg")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)