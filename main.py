import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv # you must have this 
import datetime
import os
import random
import pywhatkit as kit
import cv2
import smtplib
import webbrowser
import wikipedia
import time
import pyjokes
import pyowm
import json
import requests
import openai
import geocoder

load_dotenv()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Jarvis. Please tell me how may I help you?")

def sendEmail(to, content):
    server =smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(os.getenv("base_email_id"), os.getenv("email_id_pass"))
    server.sendmail(os.getenv("base_email_id"), to, content)
    server.close()

def get_weather(city):
    api_key = os.getenv("weather_api_key")  # Replace 'YOUR_API_KEY' with your actual API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city_name = city
    complete_url = base_url + 'q=' + city_name + '&APPID=' + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main_info = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = int(temperature_kelvin - 273.15)
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {main_info} ({description}). The temperature is {temperature_celsius}°C with {humidity}% humidity."
    else:
        return "City not found."
        
openai.api_key = os.getenv("chat_gpt_api_key")

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

def get_user_location():
    g = geocoder.ip('me')
    location = g.city
    return location



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I didn't get that. Can you please say that again?")
        return "None"
    return query

if __name__ == "__main__":
    # speak("Hello ma'am")
    wishme()

    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    
    while True:
        query = takeCommand().lower()

        if "open notepad" in query:
            npath = "C:\\WINDOWS\\System32\\notepad.exe"
            os.startfile(npath)
            speak("Opening Notepad")

        elif "open command prompt" in query:
            os.system("start cmd")
            speak("opening command prompt")

        elif "open camera" in query:
            capture = cv2.VideoCapture(0) 
            while True:
                ret, frame = capture.read()
                cv2.imshow("Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            capture.release()
            cv2.destroyAllWindows()
            speak("Closing Camera")

        elif "play music" in query:
            music_dir = "C:\\Users\\ANKIT JODHANI\\Music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))
            speak("Playing Music")

        elif "wikipedia" in query:
            speak("searching wikipedia....")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query,sentences=2)
            speak("according to wikipedia...")
            print(result)

        elif "open youtube" in query:
            speak("What would you like to search on YouTube?")
            search_query = takeCommand().lower()
            if search_query != "none":
                speak(f"Searching YouTube for {search_query}")
                webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
                webbrowser.get('brave').open(f"https://www.youtube.com/results?search_query={search_query}")
                speak("Here are the search results on YouTube.")

        elif "open google" in query:
            speak("What would you like to search on Google?")
            search_query = takeCommand().lower()
            if search_query != "none":
                speak(f"Searching Google for {search_query}")
                webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
                webbrowser.get('brave').open(f"https://www.google.com/search?q={search_query}")
                speak("Here are the search results on Google.")

        elif "open stackoverflow" in query:
            webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
            webbrowser.get('brave').open("stackoverflow.com")

        elif "open linkedin" in query or "open LinkedIn" in query:
            webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
            webbrowser.get('brave').open("linkedin.com")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)     
            speak(f"sir, the time is {strTime}")

        elif "open vs code" in query:
            code_path = "C:\\Users\\ANKIT JODHANI\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
            speak("opening vs code")


        elif "play songs on youtube" in query:
            speak("Which song would you like to listen to?")
            song_name = takeCommand().lower()
            if song_name != "none":
                kit.playonyt(song_name)
                speak(f"Playing {song_name} on YouTube.")
            else:
                speak("Sorry, I didn't catch the song name. Please try again.")
        
        elif "send email to devanshi" in query:
            try:
                speak("what should i say?")
                content = takeCommand().lower()
                to = "..."      # The id of the person to whom you want to send the mail
                sendEmail(to, content)
                speak("Email has been sent to Devanshi")
            except Exception as e:
                print(e)
                speak("sorry , i'm not able to sent Email to Devanshi")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "weather in" in query:
            city = query.split("in", 1)[1].strip()
            result = get_weather(city)
            speak(result)

        elif "chat with gpt" in query:
            speak("Sure! What would you like to chat about?")
            prompt = takeCommand().lower()
            if prompt != "none":
                response = chat_with_gpt(prompt)
                speak(response)
            else:
                speak("Sorry, I didn't catch your prompt. Please try again.")

        elif "where am I" in query or "my location" in query:
            location = get_user_location()
            speak(f"You are currently in {location}.")


        if "close notepad" in query:
            speak("Okay, closing Notepad")
            os.system("taskkill /f /im notepad.exe")
        elif "close command prompt" in query:
            speak("Okay, closing Command Prompt")
            os.system("taskkill /f /im cmd.exe")
        elif "close vs code" in query:
            speak("Okay, closing vs Code")
            os.system("taskkill /f /im code.exe")

        elif "no thanks" in query:
            speak("ok...Thank you for yousing me, have a good day.... ")
            break

        speak("do you have any other work.... ")

