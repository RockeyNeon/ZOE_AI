import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import openai
import urllib
import datetime
import subprocess
# import py
# import playsound
import AppOpener
import time
import requests
import json
# import openweathermap
import wikipedia
from ecapture import ecapture as ec
import wolframalpha
import tkinter as tk
from tkinter import messagebox
import pyjokes
import google.generativeai as genai
import re

api_key = 'XXXXXXXXX'

def initiate_genai(api_key):
    api_key = api_key
    genai.configure(api_key = api_key)
    return "model initiated"


def get_response(prompt) :
    config = genai.types.GenerationConfig(max_output_tokens=100)
    model = genai.GenerativeModel('gemini-1.0-pro')
    response = model.generate_content(contents=prompt)#, generation_config=config)
    respond = response.text
    clean_response =  re.sub(r'[^A-Za-z0-9\s]', '', respond)

    print(response.text)
    return clean_response

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"Pawan said:{query}\n")

        except Exception as e:
            say("Pardon me, please say that again")
            return "None"
        return query




print('Loading your A. I. personal assistant - Zoe')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

# api_key = "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"
# openai.api_key = api_key

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        say("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        say("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        say("Hello,Good Evening")
        

def say(text):
    engine.say(text)
    engine.runAndWait()

def browse():
    if "open" in query.lower() and " browser" in query.lower():
        words = query.split()
        for word in words:
            if len(word) > 4:
                url = word.lower()
                site = "http://" + url + ".com"
                webbrowser.open(site)
                engine.say("Opening " + url)
                engine.runAndWait()
                break
        else:
            engine.say("Sorry, I didn't understand the website you want to open.")
            engine.runAndWait()

    elif "open" in query.lower() and ".com" in query.lower():
        words = query.split()
        for word in words:
            if len(word) > 4:
                url = word.lower()
                site = "http://" + url
                webbrowser.open(site)
                engine.say("Opening " + url)
                engine.runAndWait()
                break

        else:
            engine.say("Sorry, I didn't understand the website you want to open.")
            engine.runAndWait()

    elif "search" in query.lower() and any(s in query.lower() for s in ["browser", "google"]):
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "play" in query.lower() and "on youtube" in query.lower():
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
        temperature=0.5,
        max_tokens=100,
    )
    return response.choices[0].message.content

def application(app_name):
    try:
        AppOpener.open(app_name, match_closest=True)
    except Exception as e:
        print(f"Error: {e}")

say("Loading your A.I. personal assistant - ZOE")
print(initiate_genai(api_key))
wishMe()

# def main():
if __name__ == '__main__':
    while True:
        
        say("Tell me how can I help you now?")
        query = listen().lower()
        if query == 0:
            continue

        


        if "good bye" in query or "ok bye" in query or "stop" in query:
            say('your personal assistant ZOE is shutting down,Good bye')
            print('your personal assistant ZOE is shutting down,Good bye')
            break

        if 'wikipedia' in query:
            say('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            say("According to Wikipedia")
            print(results)
            say(results)

        if any(s in query.lower() for s in ["open", "search"]) and any(
            s in query.lower() for s in ["google", "browser", ".com"]):
            browse()

        if any(s in query.lower() for s in ["open", ]) and any(s in query.lower() for s in ["in windows"]):
            app_name = query.lower().split("open ")[-1]
            application(app_name)

        if "play" in query.lower() and "on youtube" in query.lower():
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

        if 'search' in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)

        if "weather" in query:
            api_key = "XXXXXXX"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            say("whats the city name")
            city_name = listen()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                current_temperature_celsius = round(current_temperature - 273.15, 1)

                say(" Temperature in celsius unit is " +
                    str(current_temperature_celsius) +
                    "\n humidity in percentage is " +
                    str(current_humidiy) +
                    "\n description  " +
                    str(weather_description))

                print(" Temperature in celsius unit = " +
                      str(current_temperature_celsius) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                say(" City Not Found ")


        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"the time is {strTime}")
            print("The time is " + strTime)

        if 'who are you' in query or 'what is your name' in query:
            say('I am ZOE version 1 point O your personal assistant.')
            print('I am ZOE version 1 point O your personal assistant.')


        if 'news' in query:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            say('Here are some headlines from the Times of India,Happy reading')

        if "take a photo" in query:
            ec.capture(0, "robo camera", "img.jpg")


        if 'ask' in query:
            say('I can answer to computational and geographical questions and what question do you want to ask now')
            question = listen()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            say(answer)
            print(answer)

        if 'open word' in query:
            subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
        if 'open powerpoint' in query:
            subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE')
        if 'open excel' in query:
            subprocess.Popen(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
        if 'open notepad' in query:
            subprocess.Popen(r'C:\Windows\System32\notepad.exe')
        if 'open chrome' in query:
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        if 'who made you' in query or 'who created you' in query or 'who discovered you' in query:
            say("I was built by Tech Titans")
        # if 'make a note' in query:
        #     note(text)
        # if 'note this' in query:
        #     note(text)
        if 'tell me a joke' in query:
            say(pyjokes.get_joke())


        if "log off" in query or "sign out" in query:
            say("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        if "good bye" in query or "ok bye" in query or "stop zoe" in query:
            say('Your personal assistant ZOE is shutting down. Goodbye!')
            print('Your personal assistant ZOE is shutting down. Goodbye!')
            sys.exit()  
        
        else :
            print(query)
            say(get_response(query + " Answer in 50 words"))
            
# This will terminate the program

# # Initialize the GUI
# root = tk.Tk()
# root.title("Voice Assistant")
# root.geometry("400x200")
#
# # Create a label and a button
# label_text = tk.StringVar()
# label_text.set("Click the button to start the voice assistant.")
# label = tk.Label(root, textvariable=label_text)
# button = tk.Button(root, text="Start", command=main)
#
# # Pack the label and the button
# label.pack()
# button.pack()
#
# # Start the GUI
# root.mainloop()