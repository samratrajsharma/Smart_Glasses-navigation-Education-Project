import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from googlesearch import search

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")
        return ""

def get_battery_status():
    battery_percent = 99
    battery_plugged = True
    speak(f"The battery is at {battery_percent} percent and is currently {'charging' if battery_plugged else 'not charging'}.")

def perform_google_search(query):
    try:
        results = search(query, num_results=1, pause=2.0)
        if results:
            top_result = results[0]
            speak(f"The top result for {query} is: {top_result}")
        else:
            speak("Sorry, I couldn't find any results.")
    except Exception as e:
        speak(f"An error occurred while performing the search: {e}")

def handle_command(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")
    elif 'battery' in command:
        get_battery_status()
    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        speak("Opening YouTube")
    elif 'open google' in command:
        webbrowser.open('https://www.google.com')
        speak("Opening Google")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I can search that for you.")
        perform_google_search(command)

def main():
    speak("Hello, how can I assist you?")
    while True:
        command = listen()
        if command:
            handle_command(command)

if __name__ == "__main__":
    main()
