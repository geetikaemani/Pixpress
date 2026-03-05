from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import os
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Paths
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load BLIP model
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")


@app.route('/caption', methods=['POST'])
def generate_caption():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(image_file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    # Open and preprocess image
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            output = model.generate(**inputs, max_length=50)

        caption = processor.decode(output[0], skip_special_tokens=True)
        return jsonify({'caption': caption})
    
    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
