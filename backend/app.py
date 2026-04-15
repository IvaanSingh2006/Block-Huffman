from flask import Flask, request, send_file
from flask_cors import CORS
import os
from compress import compress_file
from decompress import decompress_file

app = Flask(__name__)
CORS(app, origins=["https://ivaansingh2006.github.io"])

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/compress", methods=["POST"])
def compress():
    try:
        file = request.files.get("file")
        block_size = int(request.form.get("block_size", 1))

        if not file:
            return {"error": "No file uploaded"}, 400

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "compressed.bin")

        file.save(input_path)
        compress_file(input_path, output_path, block_size)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}, 500


@app.route("/decompress", methods=["POST"])
def decompress():
    file = request.files.get("file")

    if not file:
        return {"error": "No file uploaded"}, 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "decompressed_output")

    file.save(input_path)
    decompress_file(input_path, output_path, "outputs/metadata.json")

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)