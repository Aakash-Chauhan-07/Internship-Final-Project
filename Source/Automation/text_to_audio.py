import pyttsx3
import os

def text_to_audio(text, filename):
  """Converts text to speech, saves it as an MP3 audio file, and plays it.

  Args:
    text: The text to be converted to speech.
    filename: The desired filename for the saved audio file (without extension).
  """

  engine = pyttsx3.init()

  # Save the audio to file
  engine.save_to_file(text, rf"{filename}.mp3")
  engine.runAndWait()

  # Play the saved audio file
  # (Make sure an audio player is associated with the .mp3 extension)
  os.startfile(rf"{filename}.mp3")

