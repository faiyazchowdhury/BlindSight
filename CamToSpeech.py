# Converts image to text

import io
import os
#from TextToSpeech import textToSpeech
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import texttospeech
from google.oauth2 import service_account
import os
import pygame
from pygame import mixer
import subprocess
import RPi.GPIO as GPIO
import time


# Instantiates a client
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
while True:
    if(GPIO.input(6) == 1):
        take_picture = subprocess.run('fswebcam -r 1280x720 --no-banner image1.jpg', shell=True);
        time.sleep(.003);
        credential_path = "/home/pi/MyfirstProject-820d22287a79.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        client = vision.ImageAnnotatorClient()
        # The name of the image file to annotate
        file_name = os.path.join(
            os.path.dirname(__file__),
            'image1.jpg')

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        # Performs label detection on the image file
        response = client.text_detection(image=image)
        texts = response.text_annotations

        #print('Texts: \n')
        #print(texts)
        inString = ""
        for i in range(1):
            inString += texts[i].description
        print(inString)
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=inString)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
            name='en-US-Wavenet-F')

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        with open('output.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            #print('Audio content written to file "output.mp3"')
        mixer.init()
        mixer.music.load("output.mp3")
        mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
GPIO.cleanup()
############################################################


