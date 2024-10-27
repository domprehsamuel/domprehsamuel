import speech_recognition as sr 
import pyttsx3 
import pywhatkit
import googlesearch 
import pyautogui
import os
import requests
from bs4 import BeautifulSoup
import getpass
import nltk  # Import NLTK for NLP
import hashlib



# Initialize Speech Recognition
r = sr.Recognizer()

# Initialize Text-to-Speech
engine = pyttsx3.init()

# Login Password Authentication
def login():
    password = "61bffea9215f65164ad18b45aff1436c0c165d0d5dd2087ef61b4232ba6d2c1a"  # Replace with your actual password hash

    while True:
        engine.say("How would you like to enter your password? Say 'verbal' or 'manual'.")
        print("How would you like to enter your password? Say 'verbal' or 'manual'.")
        engine.runAndWait()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.42)  # Adjust duration as needed
            audio = r.listen(source)
            try:
                entry_method = r.recognize_google(audio).lower()

                if entry_method == "verbal":              
                    engine.say("Please say your login password.")
                    engine.runAndWait()

                    with sr.Microphone() as source:
                        audio = r.listen(source)
                        try:
                            recognized_password = r.recognize_google(audio).lower()
                            spoken_password = hashlib.sha256((recognized_password).encode()).hexdigest()
                            if spoken_password == password:
                                print("Login successful...")
                                engine.say("Login successful.")
                                return True
                            else:
                                print("Incorrect password.")
                                return False
                        except sr.UnknownValueError:
                            print("Sorry, didn't catch that.")
                            return False

                elif entry_method == "manual":
                    engine.say("Enter your login password.")
                    engine.runAndWait()
                    typed_password = getpass.getpass("Enter your login password: ").lower()
                    hashed_password = hashlib.sha256((typed_password).encode()).hexdigest()
                    if hashed_password == password:
                        engine.say("Login successful.")
                        print("Login successful.")
                        return True
                    else:
                        print("Incorrect password.")
                else:
                    print("Invalid entry method. Please try again.")
            except sr.UnknownValueError:
                print("Sorry, didn't catch that. Please try again.")

# Speech Recognition Enhancement
def listen_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Sorry, didn't catch that."

def open_program(program_name):
    program_paths = {
        'Notepad': r'C:\\Windows\\notepad.exe',
        'Chrome': r'C:\\Program Files\\Google\\Chrome\\chrome.exe',
        'Vlc': r'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe',
        'Winrar': r'C:\\Program Files\\WinRAR\\WinRAR.exe',
        'Vs Code': r'C:\\Users\\Dompreh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
    }
   
    try:
        os.system(f"start {program_paths[program_name.title()]}")
    except Exception as e:
        print(f"Error opening {program_name}: {e}")
        engine.say(f"Error opening {program_name}.")
        engine.runAndWait()

def search_chrome(query):
    url = f"https://google.com/search?q='{query}'"
    os.system(f"start chrome {url}")

def scrape_website(url, action):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
       
        if action == "scrape":
            print(soup.prettify())
        elif action == "fetch":
            print(soup.title.text)
            engine.say(f"The title is {soup.title.text}.")
            print([a.get("href") for a in soup.find_all("a", href=True)])
        elif action == "extract":
            import re
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.text)
            phone_numbers = re.findall(r"\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}", soup.text)
            print(emails)
            print(phone_numbers)
        elif action == "find":
            print(soup.find_all("img"))
       
        engine.say(f"{action.capitalize()}ing completed.")
        engine.runAndWait()
    except Exception as e:
        print(f"Error {action}ing {url}: {e}")
        engine.say(f"Error {action}ing website.")
        engine.runAndWait()

def handle_command(command):
    intents = {
        "open": ["open", "start", "launch", "run"],
        "search": ["search", "find", "look up"],
        "scrape": ["scrape", "extract", "fetch", "find"],
        "close": ["close", "exit", "quit"]

    }

    command = command.lower()
    tokens = nltk.word_tokenize(command)  # Tokenize the command

    # Use NLP to identify intent and entities
    intent = None
    entities = {}
    for intent_name, keywords in intents.items():
        for keyword in keywords:
            if keyword in command:
                intent = intent_name
                entities[keyword] = " ".join([token for token in tokens if token == keyword or token in keywords])
                break  # Stop iterating keywords once intent is found

    if intent == "open":
        program_name = entities.get("open")  # Use entity for program name
        if program_name:
            open_program(program_name.replace(keyword, "").strip())
        else:
            print("Couldn't understand the program name. Please rephrase.")
    elif intent == "search":
        query = entities.get("search")  # Use entity for search query
        if query:
            engine.say(f"Searching for '{query}' on Chrome.")
            search_chrome(query)
        else:
            engine.say("Couldn't understand the search query. Please rephrase.")
            print("Couldn't understand the search query. Please rephrase.")
    elif intent == "close":
        engine.say("Exiting program.")
        print("Exiting program.")
        engine.runAndWait()
        exit()

    else:
        engine.say("Sorry, I didn't understand your command. Please try again.")
        print("Sorry, I didn't understand your command. Please try again.")

def main():
    if login():
        while True:
            command = listen_command()
            print(f"Command: {command}")
            handle_command(command)

if __name__ == "__main__":
    main()
    engine.runAndWait()
    engine.stop()
