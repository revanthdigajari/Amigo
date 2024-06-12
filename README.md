Chat Bot Application

This Flask-based chatbot integrates image recognition, text-to-speech, and APIs for user interaction. Users can engage via text input, uploaded images, or speech recognition. The application leverages TensorFlow/Keras for image analysis, Unsplash API for image search, and YouTube API for video fetching. Additionally, it features a user-friendly web interface for seamless interaction.

Key Features:

Flask Framework: Utilizes Flask for building a lightweight web application.
Image Recognition: Incorporates InceptionV3 model for image classification.
Text-to-Speech: Converts text responses into speech using pyttsx3 library.
API Integration: Integrates Unsplash and YouTube APIs for image and video retrieval.
User Interaction: Allows users to interact via text, images, or speech input.
Web Interface: Provides a user-friendly web interface for seamless interaction.
Setup Instructions:

Clone the repository: git clone https://github.com/revanthdigajari/Amigo.git
Navigate to the project directory: cd chat-bot
Install dependencies: pip install -r requirements.txt
Set API keys:
Set GROQ_API_KEY environment variable to your Groq API key.
Set YOUTUBE_API_KEY environment variable to your YouTube API key.
Set UNSPLASH_API_KEY environment variable to your Unsplash API key.
Run the application: python app.py
Access the application in your web browser at http://localhost:5000
Usage:

Enter your message in the input field and click "SEND" or press Enter to send.
Optionally, upload an image using the "Upload" button.
Click the "Audio" button to enable speech recognition (Google Chrome only).
Click the "Speaker" button to hear the bot's response as speech.
Use the "mute" button to stop the speech playback.
Contributing:

Fork the repository.
Create a new branch: git checkout -b feature-branch
Make your changes and commit them: git commit -am 'Add new feature'
Push to the branch: git push origin feature-branch
Submit a pull request.
Credits:

Developed by Revanth Digajari
Inspired by OpenAI ChatGPT
Libraries used: Flask, TensorFlow, Keras, pyttsx3, requests, Pillow
License:This project is licensed under the MIT License.



