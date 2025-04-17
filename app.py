import io
from PIL import Image
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from pydub import AudioSegment
import speech_recognition as sr
import re
import torch
from Hand_Written import H_digit_Object
from Voice import Extracted_Text_FROM_VOICE_Object

app = Flask(__name__)
CORS(app)  

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav'}  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

hand_writter_digit_obj= H_digit_Object() 
voice_objects=Extracted_Text_FROM_VOICE_Object()
CONFIDENCE_THRESHOLD = 0.7

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    numbers = request.form.get('numbers')
    print("Numbers received:", numbers)

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            print(file_path)
            wav_path = voice_objects.convert_to_wav(file_path)
            if not wav_path:
                return jsonify({"error": "Unsupported or corrupted audio file"}), 400

            audio = AudioSegment.from_file(wav_path)
            print(f"Total audio duration: {len(audio) / 1000} seconds")

            # Add silence between segments
            segment_duration = 2000  # 2 seconds 
            silence_duration = 1000  # 1 second 
            combined_audio = voice_objects.add_silence_between_segments(audio, segment_duration, silence_duration)
            combined_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], "combined_audio.wav")
            combined_audio.export(combined_audio_path, format="wav")
            transcribed_text = voice_objects.transcribe_audio(combined_audio_path)
            spoken_numbers = voice_objects.extract_numbers_from_text(transcribed_text)

            # Compare spoken numbers with expected numbers
            expected_numbers = list(map(int, numbers.split(',')))
            correct_count = voice_objects.compare_numbers(spoken_numbers, expected_numbers)
            print("Spoken numbers:", spoken_numbers)
            print("Expected numbers:", expected_numbers)
            print("Correct count:", correct_count)

            os.remove(file_path)
            os.remove(wav_path)
            os.remove(combined_audio_path)

            return jsonify({
                "spoken_numbers": spoken_numbers,
                "expected_numbers": expected_numbers,
                "correct_count": correct_count,
                "total_numbers": len(expected_numbers)
            })
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400
    

@app.route('/digit/predict', methods=['POST'])
def digit_predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    # try:
    # Read the image file
    img_bytes = file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert('L')  # Convert to grayscale
    
    # Preprocess the image
    image = hand_writter_digit_obj.transform(image).unsqueeze(0)  # Add batch dimension

    # Make prediction
    with torch.no_grad():
        outputs = hand_writter_digit_obj.digits_model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)  # Calculate probabilities

        # Get the top prediction
        top_prob, top_pred_idx = torch.max(probabilities, 1)
        top_prob = top_prob.item()
        top_class = hand_writter_digit_obj.digits_class_names[top_pred_idx.item()]

        # If the confidence is above the threshold, return the result
        if top_prob >= CONFIDENCE_THRESHOLD:
            return jsonify({
                'result': top_class,
                'percentage': f"{top_prob * 100:.2f}%"
            }), 200
        else:
            return jsonify({
                'result': "This is not making the confident limit"
            }), 200

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='192.168.8.100', port=5000)