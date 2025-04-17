from pydub import AudioSegment
import speech_recognition as sr
import re

class Extracted_Text_FROM_VOICE_Object:
    def convert_to_wav(self, file_path):
        try:
            sound = AudioSegment.from_file(file_path)
            wav_path = file_path.rsplit('.', 1)[0] + '.wav'
            sound.export(wav_path, format="wav")
            return wav_path
        except Exception as e:
            print(f"Error converting to WAV: {e}")
            return None

    def add_silence_between_segments(self, audio, segment_duration, silence_duration):
        """Add silence between audio segments."""
        combined_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment

        for i in range(0, len(audio), segment_duration):
            segment = audio[i:i + segment_duration]
            combined_audio += segment
            combined_audio += AudioSegment.silent(duration=silence_duration)  # Add silence

        return combined_audio

    def transcribe_audio(self, audio_path):
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

    def extract_numbers_from_text(self, text):
        if not text:
            return []
            
        # Define mappings for word-to-number conversion
        word_to_number = {
            "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
            "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
            "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13", 
            "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
            "eighteen": "18", "nineteen": "19", "twenty": "20", 
            "thirty": "30", "forty": "40", "fifty": "50"
        }
        
        # Define special two-word cases
        compound_numbers = {
            "twenty one": "21", "twenty two": "22", "twenty three": "23", 
            "twenty four": "24", "twenty five": "25", "twenty six": "26",
            "twenty seven": "27", "twenty eight": "28", "twenty nine": "29",
            "thirty one": "31", "thirty two": "32", "thirty three": "33",
            "thirty four": "34", "thirty five": "35", "thirty six": "36",
            "thirty seven": "37", "thirty eight": "38", "thirty nine": "39",
            "forty one": "41", "forty two": "42", "forty three": "43",
            "forty four": "44", "forty five": "45", "forty six": "46",
            "forty seven": "47", "forty eight": "48", "forty nine": "49"
        }
        
        # First process compound numbers (like "twenty one")
        text_lower = text.lower()
        for compound, value in compound_numbers.items():
            text_lower = text_lower.replace(compound, value)
        
        # Split the processed text into tokens
        tokens = text_lower.split()
        numbers = []
        
        for token in tokens:
            # Check if the token is a word-form number
            if token in word_to_number:
                numbers.append(word_to_number[token])
            else:
                # Check if the token contains digits
                digit_match = re.findall(r'\d+', token)
                if digit_match:
                    for num in digit_match:
                        # Keep numbers in the range 0-50 as is
                        num_val = int(num)
                        if 0 <= num_val <= 50:
                            numbers.append(num)
                        else:
                            # Split larger numbers into individual digits
                            for digit in num:
                                numbers.append(digit)
        
        return numbers

    def compare_numbers(self, spoken_numbers, expected_numbers):
        correct_count = 0
        
        # Convert all expected numbers to strings for comparison
        expected_numbers_str = [str(num) for num in expected_numbers]
        
        print("Processing - Spoken numbers before processing:", spoken_numbers)
        print("Expected numbers:", expected_numbers_str)
        
        # Match element by element with position sensitivity
        min_len = min(len(spoken_numbers), len(expected_numbers_str))
        for i in range(min_len):
            if spoken_numbers[i] == expected_numbers_str[i]:
                correct_count += 1
        
        return correct_count