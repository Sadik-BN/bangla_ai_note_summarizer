from google import genai
from dotenv import load_dotenv
import os,io
from gtts import gTTS

load_dotenv()

apiKey= os.getenv("GEMINI_KEY")


client= genai.Client(api_key=apiKey)


#Note generation function

def note_generator(images):

    prompt="""Analyze the images if they are academic study materials generate summarized notes in a well structure at max 200 words for each image (as much as possible in Bangla Language) . 
    Else directly state that particular images are not any study material in Bangla Language and don't generate any note.
    Make sure to add necessary markdown to differentiate different sections.Also if images are related do not split the summary by image."""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[images,prompt]
    )
    return response.text


def audio_transcript_generator(text):
    speech = gTTS(text,lang='bn',slow=False)

    audio_buffer = io.BytesIO()

    speech.write_to_fp(audio_buffer)

    return audio_buffer



def quiz_generator(images,difficulty):
    prompt = f"Analyze the images if they are strictly academic study materials generate quizes at max 5 quizes (if appropriate for contexts of the images) with the difficulty:{difficulty} based on the images and make sure using proper markdown.Give the correct answers separately at the end of the all quiz questions. Else Directly state that quiz can't be generated."

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[images,prompt]
    )
    return response.text