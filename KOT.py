##KOT - THE KAPASIA BOT##

#Setup
#for speech-to-text
import speech_recognition as sr

#for text-to-speech
from gtts import gTTS

# for language model
import transformers

# for data
import os
import datetime
import numpy as np


#The AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("ME:  ", self.text)
        except:
            print("ME:   ERROR")

    @staticmethod
    def text_to_speech(text):
        print("ai --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        os.system("start res.mp3")
        os.remove("res.mp3")
    
    #To keep the model awake
    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')


#Running the AI
if __name__ == "__main__":
    ai = ChatBot(name="KOT")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    while True:
        ai.speech_to_text()
        #wake up
        if ai.wake_up(ai.text) is True:
            res = "Hello I am Kapasia-Bot, what can I do for you?"
        #keeping time
        elif "time" in ai.text:
            res = ai.action_time()
        
        #for responding politely
        elif any(i in ai.text for i in ["thank","thanks"]):
            res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","peace out!"])
        
        #conversation
        else:   
            chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
            res = str(chat)
            res = res[res.find("bot >> ")+6:].strip()

        ai.text_to_speech(res)