from flask import Flask, render_template, request, jsonify, send_file
import os
import pyttsx3
import requests
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS
from groq import Groq

app = Flask(__name__, static_folder='static')
os.environ['GROQ_API_KEY'] = "GROQ-API-KEY"
YOUTUBE_API_KEY = "YOUTUBE-API-KEY"
UNSPLASH_API_KEY = "UNSPLASH-API-KEY"
model = InceptionV3(weights='imagenet', include_top=True)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

class ChatBot:
    def __init__(self):
        self.client = Groq()
    def send_message(self, message):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: Unable to get response from Groq API. {e}"

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict_image_class(img_path):
    img_array = load_and_preprocess_image(img_path)
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    return decoded_predictions

def get_image_metadata(img_path):
    img = Image.open(img_path)
    exif_data = img._getexif()
    metadata = {}
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata[tag_name] = value
    return metadata

def search_images(query, api_key):
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}"
        response = requests.get(url)
        data = response.json()
        return [item['urls']['regular'] for item in data.get('results', [])]
    except Exception as e:
        print("An error occurred:", str(e))
        return []

def download_image(url, filename):
    try:
        os.makedirs("static/images", exist_ok=True)
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join("static/images", filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully.")
        else:
            print("Failed to download image. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def search_youtube_videos(query, api_key):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        return [f"https://www.youtube.com/embed/{item['id']['videoId']}" for item in data.get('items', [])]
    except Exception as e:
        print("An error occurred:", str(e))
        return []
chat_bot = ChatBot()

@app.route('/')
def index():
    return render_template('YOUR_HTML_FILE_NAME')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message', None)
    predicted_label = request.json.get('predicted_label', None)
    if predicted_label:
        bot_response = chat_bot.send_message(predicted_label)
    else:
        bot_response = chat_bot.send_message(user_input)
    query = predicted_label if predicted_label else user_input
    images = search_images(query, UNSPLASH_API_KEY)
    image_location = None
    if images:
        print("Found image.")
        download_image(images[0], "IMAGE-LOCATION")
        image_location = os.path.join("static", "images", "IMAGE-LOCATION")
    videos = search_youtube_videos(query, YOUTUBE_API_KEY)
    video_location = videos[0] if videos else None
    if video_location:
        print(f"YouTube video link: {video_location}")
    return jsonify({'response': bot_response, 'image': image_location, 'video': video_location})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']
        file_path = os.path.join("static/images", file.filename)
        file.save(file_path)
        predicted_data = predict_image_class(file_path)
        predicted_label = predicted_data[0][1]
        metadata = get_image_metadata(file_path)
        response = chat_bot.send_message(predicted_label)
        images = search_images(predicted_label, UNSPLASH_API_KEY)
        image_location = None
        if images:
            print("Found image.")
            download_image(images[0], "image1.jpg")
            image_location = os.path.join("static", "images", "image1.jpg")
        videos = search_youtube_videos(predicted_label, YOUTUBE_API_KEY)
        video_location = videos[0] if videos else None
        if video_location:
            print(f"YouTube video link: {video_location}")
        return jsonify({
            'success': True,
            'predicted_label': predicted_label,
            'response': response,
            'image': image_location,
            'video': video_location,
            'metadata': metadata
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text', None)
    if text:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) 
        engine.setProperty('volume', 0.9)  
        engine.save_to_file(text, 'AUDIO-FILE')
        engine.runAndWait()
        audio_file_path = "AUDIO-FILE"
        return send_file(audio_file_path, mimetype='audio/mpeg')
    else:
        return jsonify({'error': 'No text provided'}), 400
if __name__ == "__main__":
    app.run(debug=True)
