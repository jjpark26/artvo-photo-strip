from flask import Flask, render_template, request, send_file
from PIL import Image, ImageOps, ImageDraw, ImageFont
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
        
        message = request.form["message"]
        
        slots = {
            "photo1": (109, 90, 809, 516),
            "photo2": (109, 635, 448, 561),
            "photo3": (590, 635, 330, 492)
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

        draw = ImageDraw.Draw(template)

        try:
            font_date = ImageFont.truetype("arial.ttf", 32)
            font_message = ImageFont.truetype("arial.ttf", 28)
        except:
            font_date = ImageFont.load_default()
            font_message = ImageFont.load_default()

        date_text = datetime.now().strftime("%Y.%m.%d")

        draw.text(
            (760, 1180),
            date_text,
            fill="white",
            font=font_date
        )

        bbox = draw.textbbox((0, 0), message, font=font_message)
        text_width = bbox[2] - bbox[0]

        right_edge = 920
        x_position = right_edge - text_width

        draw.text(
            (x_position, 1240),
            message,
            fill="white",
            font=font_message
        )

        template.save(output_path)

        print("SAVED OUTPUT:", output_path)
        print("OUTPUT FILES:", os.listdir(OUTPUT_FOLDER))

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


@app.route("/debug")
def debug():
    return {
        "output_folder": OUTPUT_FOLDER,
        "output_exists": os.path.exists(OUTPUT_FOLDER),
        "files": os.listdir(OUTPUT_FOLDER)
    }


@app.route("/image/<filename>")
def image(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)