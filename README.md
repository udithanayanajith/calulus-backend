# Calulus-backend

Dr. Calculus is an AI-powered educational mobile application designed to make mathematics engaging and accessible for grades 1-5 students. The app combines voice recognition, handwriting analysis, and gamified learning to deliver personalized math education.


# Backend for Handwritten Digit Recognition and Voice Transcription

This repository contains the backend implementation for a system that combines **handwritten digit recognition** and **voice transcription**. The backend is built using Python with Flask and integrates a pre-trained ResNet18 model for digit recognition and speech recognition for transcribing spoken numbers. It serves as the API for a mobile application where users can draw digits or speak numbers, and the system predicts or transcribes the input.

## Features

- **Handwritten Digit Recognition**:
  - Uses a pre-trained ResNet18 model fine-tuned for grayscale images to classify handwritten digits.
  - Accepts image uploads and returns the predicted digit with confidence percentage.
- **Voice Transcription**:
  - Converts audio files (MP3, M4A, WAV) to WAV format.
  - Transcribes spoken numbers from the audio using Google Speech Recognition.
  - Compares the transcribed numbers with expected numbers and returns the accuracy.
- **REST API**:
  - Provides two endpoints:
    - `/digit/predict`: For handwritten digit recognition.
    - `/transcribe`: For voice transcription and number comparison.
- **Image and Audio Preprocessing**:
  - Images are resized, converted to grayscale, and normalized.
  - Audio files are segmented, and silence is added between segments for better transcription.

## Technologies Used

- **Python**: The primary programming language.
- **Flask**: A lightweight web framework for building the REST API.
- **PyTorch**: Used for loading and running the pre-trained ResNet18 model.
- **Torchvision**: Provides utilities for image preprocessing and model loading.
- **Pydub**: For audio file conversion and manipulation.
- **SpeechRecognition**: For transcribing audio to text using Google Speech Recognition.
- **Flask-CORS**: Enables Cross-Origin Resource Sharing (CORS) for the API.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (for audio processing with Pydub)

### Installation

1.  **Clone the repository**:

        git clone https://github.com/your-username/your-repo-name.git
        cd your-repo-name

2.  **Create a virtual environment**:

        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate

3.  **Install dependencies**:

        pip install -r requirements.txt

4.  **Download the trained model**:
    - Place the trained model (`digits_model.pth`) in the `models` directory.
    - Ensure the model is compatible with the ResNet18 architecture modified for grayscale input.
5.  **Run the Flask server**:

        python app.py

    The server will start at `http://192.168.8.162:5000`.

### API Endpoints

- **POST `/digit/predict`**:

  - Accepts an image file (JPEG or PNG) as form data.
  - Returns a JSON response with the predicted digit and confidence percentage.

  **Example Request**:

      curl -X POST -F "image=@digit.jpg" http://192.168.8.162:5000/digit/predict

  **Example Response**:

      {
        "result": "5",
        "percentage": "95.23%"
      }

- **POST `/transcribe`**:

  - Accepts an audio file (MP3, M4A, WAV) and a list of expected numbers as form data.
  - Returns a JSON response with the transcribed numbers, expected numbers, and accuracy.

  **Example Request**:

      curl -X POST -F "file=@audio.m4a" -F "numbers=1,2,3" http://192.168.8.162:5000/transcribe

  **Example Response**:

      {
        "spoken_numbers": [1, 2, 3],
        "expected_numbers": [1, 2, 3],
        "correct_count": 3,
        "total_numbers": 3
      }

### Directory Structure

    your-repo-name/
    ├── app.py                  # Flask application
    ├── models/                 # Directory for trained models
    │   └── digits_model.pth    # Pre-trained model weights
    ├── Hand_Written.py         # Handwritten digit recognition module
    ├── convert_and_extract_voice.py  # Voice transcription module
    ├── requirements.txt        # Python dependencies
    ├── README.md               # Project documentation
    └── uploads/                # Temporary storage for uploaded files

### Model Training (Optional)

If you want to train the model yourself:

1.  Prepare a dataset of handwritten digit images (e.g., MNIST or custom dataset).
2.  Modify the ResNet18 model to accept grayscale input:

        model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

3.  Train the model using PyTorch and save the weights:

        torch.save(model.state_dict(), 'digits_model.pth')

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
