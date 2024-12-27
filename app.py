from flask import Flask, request, render_template, send_file
import os
from translation import ExcelTranslator

# Initialize model
model_path = "local_model"
translator = ExcelTranslator(model_path)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Render the file upload form."""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Handle file upload and translation."""
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        input_path = os.path.join("uploads", file.filename)
        output_path = os.path.join("uploads", f"translated_{file.filename}")

        # Save uploaded file
        os.makedirs("uploads", exist_ok=True)
        file.save(input_path)

        # Translate the file using the function from translation.py
        translator.translate_excel(input_path, output_path)

        # Serve the translated file for download
        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
