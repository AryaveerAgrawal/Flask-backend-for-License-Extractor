# Install required packages
!pip install flask flask-cors pyngrok google-generativeai

# Setup and run the server
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import threading
import google.generativeai as genai
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key="AIzaSyBKiOv_8sSmGyNUOyrBrXbdswsrr331q54")

@app.route('/process', methods=['GET', 'POST'])
def process_license():
    if request.method == 'GET':
        return jsonify({"status": "Server is alive and ready to process POST requests with base64 images."})
    try:
        data = request.json
        base64_image = data.get('image')

        # Convert base64 to image
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))

        # Process with Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([
            "Extract all information from this driving license image and return it in JSON format with fields like name, license number, expiry date, etc.",
            image
        ])

        return jsonify({"drivingLicense": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

def run_flask():
    app.run(host='0.0.0.0', port=8083)

# Start Flask in background
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Start ngrok tunnel
public_url = ngrok.connect(8083)
print(f"Your public URL: {public_url}")
print("Copy this URL and paste it in your React app!")
