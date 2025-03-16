from pydub import AudioSegment
import speech_recognition as sr
import re

class Extracted_Text_FROM_VOICE_Object:
    def convert_to_wav(file_path):
        try:
            sound = AudioSegment.from_file(file_path)
            wav_path = file_path.rsplit('.', 1)[0] + '.wav'
            sound.export(wav_path, format="wav")
            return wav_path
        except Exception as e:
            print(f"Error converting to WAV: {e}")
            return None

    def add_silence_between_segments(audio, segment_duration, silence_duration):
        """Add silence between audio segments."""
        combined_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment

        for i in range(0, len(audio), segment_duration):
            segment = audio[i:i + segment_duration]
            combined_audio += segment
            combined_audio += AudioSegment.silent(duration=silence_duration)  # Add silence

        return combined_audio

    def transcribe_audio(audio_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"Transcribed text: {text}")
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
                return None
            except sr.RequestError as e:
                print(f"Google Speech Recognition error: {e}")
                return None

    def extract_numbers_from_text(text):
        if not text:
            return None
        tokens = text.split()
        numbers = []
        
        for token in tokens:
            digit_sequences = re.findall(r'\d+', token)
            for seq in digit_sequences:
                if len(seq) > 2:
                    numbers.extend(list(seq))
                else:
                    numbers.append(seq)
        return numbers

    def compare_numbers(spoken_numbers, expected_numbers):
        correct_count = 0
        spoken_numbers = [int(num) for num in spoken_numbers] 
        for spoken, expected in zip(spoken_numbers, expected_numbers):
            if spoken == expected:
                correct_count += 1   
        return correct_count