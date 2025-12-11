import pyttsx3  # type: ignore # Text-to-speech engine
import speech_recognition as sr # type: ignore
import os
import cv2 #----> for camera
import random 
from requests import get #----->to find ip address
import wikipedia
import webbrowser
import pywhatkit as kit #------>to send message via whatsapp(can do a lot)
import sys
import time
from datetime import datetime
import threading
import pyjokes
import pyautogui #----->control mouse keyboard
import requests
import instaloader #--->instagram
from bs4 import BeautifulSoup #----->to get the weather forcast
import psutil #------>to get battery
import speedtest #----->to get internet speed
from twilio.rest import Client #----->To make call (twillio)
from PyQt5 import QtWidgets, QtCore, QtGui  #----->for GUI
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie #-----> to move
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from NEOui import Ui_MainWindow #-----> class in NEOui

engine = pyttsx3.init('sapi5')  # Use SAPI5 engine 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Male voice (use voices[2] for female)

def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") # Get available system voices
        voice_to_use = voices[0].id if len(voices) > 0 else voices[1].id #Prefer voice[0] if available, else fallback to voice[1]
        engine.setProperty("voice", voice_to_use)
        engine.setProperty("rate", 175) #Set speaking speed (default is too slow on some PCs)

        engine.say(text) #Queue the text to be spoken
        engine.runAndWait() # Run the speech engine until finished
        engine.stop() # Properly stop engine to prevent memory lock

class MainThread(QThread):  #---->class inherit
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    #to convert voice to text
    def takecommand(self):
        r = sr.Recognizer()
    
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)  # FIXES MIC ISSUES

            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
            except:
                print("Mic timeout")
                return "none"

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")
            return query.lower()
        except:
            return "none"


    #alarm
    def set_alarm(alarm_time_str):
        try:
            # Convert time input to a proper format
            alarm_time_str = alarm_time_str.replace("a.m.", "AM").replace("p.m.", "PM")
            alarm_time = datetime.strptime(alarm_time_str, "%I:%M %p").time()

            # Speak the set alarm time
            speak(f"Alarm is set for {alarm_time.strftime('%I:%M %p')}")

            # Wait for the alarm time to match the current time
            while True:
                now = datetime.now().time()
                if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                    speak("Time to wake up, sir!")
                    break
                time.sleep(10)  # Check the time every 10 seconds
        except ValueError:
            speak("Sorry, I didn't understand the time format. Please say it like '6:30 AM'.")

    # Function to set alarm when requested
    def handle_alarm_query(self, query):
        if "set alarm" in query:
            speak("Please tell me the time to set the alarm. Say like 6:30 AM or 7:45 PM")
            alarm_input = self.takecommand().lower()

            try:
                alarm_input = alarm_input.replace("a.m.", "AM").replace("p.m.", "PM")
                t = threading.Thread(target=self.set_alarm, args=(alarm_input.strip(),))
                t.start()  # Start the alarm thread
            except Exception as e:
                speak(f"Error: {str(e)}. Try again.")

    #weather
    def get_weather(self, city="delhi"):
        try:
            url = f"https://wttr.in/{city}?format=3"  # Simple weather format
            res = requests.get(url)

            if res.status_code == 200:
                weather_info = res.text.strip()
                speak(f"The weather in {city} is: {weather_info}")
            else:
                speak("Sorry, I couldn't fetch the weather information right now.")
        except Exception as e:
            speak("There was an error fetching the weather.")
            print("Error:", e)

    #to wish
    def wish(self):
        hour = int(datetime.now().hour) #---->to get the correct time
        tt = time.strftime("%I:%M %p")
        
        if hour >= 0 and hour <= 12:
            speak(f"good morning, its {tt}")
        elif hour >= 12 and hour <= 18:
            speak(f"good afternoon, its {tt}")
        else:
            speak(f"good evening, its {tt}")
        speak("i am Neo . please tell me how may i help you")

    def TaskExecution(self):
        self.wish()
        while True:
            query = self.takecommand().lower()

            #logic build for tasks
            if "open notepad" in query:
                npath = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2501.31.0_x64__8wekyb3d8bbwe\\Notepad\\notepad.exe" #----->\\double backslash to get to directory
                os.startfile(npath)
                
            elif query == "none":
                continue   # keep listening



            

            elif "open camera" in query:
                cam = cv2.VideoCapture(0)
                cv2.namedWindow("webcam")  # Create a named window to monitor

                while True:
                    ret, img = cam.read()
                    if not ret:
                        speak("Failed to grab frame")
                        break
                    cv2.imshow("webcam", img)

                    key = cv2.waitKey(1)

                    # Exit if ESC is pressed
                    if key == 27:
                        speak("Closing camera.")
                        break

                    # Check if the window was closed manually
                    if cv2.getWindowProperty("webcam", cv2.WND_PROP_VISIBLE) < 1:
                        speak("Camera window closed.")
                        break

                cam.release()
                cv2.destroyAllWindows()

            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in query:
                speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("according to wikipedia")
                print(results)
                speak(results)

            elif "youtube" in query:
                webbrowser.open("www.youtube.com")

            elif "facebook" in query:
                webbrowser.open("www.facebook.com")

            elif "stack overflow" in query:
                webbrowser.open("www.stackoverflow.com")

            elif "search" in query and "on google" in query:
                search_query = query.replace("search", "").replace("on google", "").strip()
                if search_query:
                    speak(f"Searching for {search_query} on Google.")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                else:
                    speak("What should I search on Google?")
                    search_query = self.takecommand().lower()
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")

            elif "whatsapp" in query:
                kit.sendwhatmsg("+917024433101", "this is a test protocol", 14, 32) #---->change time and number according to you

            elif "play" in query or "on youtube" in query:
                video = query.replace("play", "").replace("on youtube", "").strip()
                if video:
                    speak(f"Playing {video} on YouTube.")
                    kit.playonyt(video)
                else:
                    speak("What should I play on YouTube?")
                    video = self.takecommand().lower()
                    speak(f"Playing {video} on YouTube.")
                    kit.playonyt(video)

            elif "bye" in query:
                speak("thanks for using me, have a great day")
                sys.exit()

            elif "close notepad" in query:
                speak("okay sir, closing notepad")
                os.system(r"C:\Windows\System32\taskkill.exe /f /im notepad.exe")

            elif "close command prompt" in query:
                speak("okay sir, closing command prompt")
                os.system(r"C:\Windows\System32\taskkill.exe /f /im cmd.exe")

            elif "set alarm" in query:
                speak("Please tell me the time to set the alarm. Say like 6:30 AM or 7:45 PM")
                alarm_input = self.takecommand().lower()

                try:
                    alarm_input = alarm_input.replace("a.m.", "AM").replace("p.m.", "PM")
                    alarm_input = alarm_input.replace("am", " AM").replace("pm", " PM")
                    t = threading.Thread(target=self.set_alarm, args=(alarm_input.strip(),))
                    t.start()
                except:
                    speak("Sorry, I couldn't set the alarm. Try again.")
                
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down" in query:
                os.system("shutdown /s /t 5")

            elif "restart" in query:
                os.system("shutdown /r /t 5")

            elif "sleep" in query:
                os.system(r"C:\Windows\System32\rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "switch tab" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where am i" in query:
                speak("Wait sir, let me check.")
                try:
                    ipAdd = get('https://api.ipify.org').text
                    print(f"IP Address: {ipAdd}")
                    url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()

                    city = geo_data.get('city')
                    country = geo_data.get('country')

                    if city and country:
                        speak(f"Sir, I am not sure, but I think we are in {city} city of {country}.")
                    else:
                        speak("Sorry Sir, I couldn't retrieve the exact location.")

                except Exception as e:
                    speak("Sorry Sir, due to some network issue I am not able to find the location.")
                    print("Error:", e)

            elif "instagram profile" in query or "instagram" in query:
                speak("sir please enter the user name correctly.")
                name = input("enter the username: ")
                webbrowser.open(f"www.instagram.com/{name}")
                time.sleep(5)
                speak("Sir do you want me to download the profile picture of this account")
                condition = self.takecommand().lower()
                if "sure" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("i am done sir, profile picture is saved in your main folder now i am ready for your next command")
                else:
                    pass

            elif "take a screenshot" in query or "screenshot" in query:
                speak("Sir, tell me the name i should save the screenshot file")
                name = self.takecommand().lower()
                speak("please hold the screen for few seconds, i am taking the screenshot")
                time.sleep(2)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("i am done sir, the screenshot is saved in our main folder, i am ready for the next command")
            
            elif "calculate" in query:
                speak("Please tell me the calculation.")
                try:
                    calc_query = self.takecommand().lower()

                    calc_query = calc_query.replace("plus", "+")
                    calc_query = calc_query.replace("minus", "-")
            
                    calc_query = calc_query.replace("what is", "")
                    calc_query = calc_query.replace("calculate", "")
            
                    result = eval(calc_query)
                    speak(f"The answer is {result}")
            
                except Exception as e:
                    speak("Sorry, I could not understand the calculation.")

            elif "temperature" in query or "weather" in query:
                speak("Which city's weather do you want?")
                city = self.takecommand().lower()
                self.get_weather(city)

            elif "battery" in query:
                battery = psutil.sensors_battery() #----->know about battery
                percentage = battery.percent #------>to get percent
                speak(f"sir our system have {percentage} percent battery")

            elif "internet speed" in query:
                speak("sorry it might take few seconds please wait")
                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"Sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")

            #To make call
            elif "call" in query:
                account_sid = "ACbc6eac821f11ae5c292a3c592f53826b"
                auth_token = "a229840418f93c1ba6ed3d951302bfe3"

                client = Client(account_sid, auth_token)

                call = client.calls.create(
                    twiml='<Response><Say>Hello, my name is NEO. This is a test call.</Say></Response>',
                    from_="+12317972986",  
                    to="+919667771633"     
                )

                speak("Calling the number now.")

            #To send SMS
            elif "message" in query:
                account_sid = "ACbc6eac821f11ae5c292a3c592f53826b"
                auth_token = "a229840418f93c1ba6ed3d951302bfe3"
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body="Hello, my name is NEO. This is a test message?",
                    from_="+12317972986",  
                    to="+919667771633"     
                )

                speak("sending the message.")

            elif "volume up" in query:
                pyautogui.press("volumeup")

            elif "volume down" in query:
                pyautogui.press("volumedown")

            elif "mute" in query or "volume mute" in query:
                pyautogui.press("volumemute")

class Main(QMainWindow): #----->main UI interface
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) #----->pop up
        self.ui.pushButton_2.clicked.connect(self.startTask)
        self.ui.pushButton.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("NEO/UI/back.png")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("NEO/UI/nova.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("NEO/UI/start end.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie("NEO/UI/start end.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.thread = MainThread()
        self.thread.start()

app = QApplication(sys.argv) #--->feature of Pyqt5 overall app execution.
neo = Main() #---->custom GUI class added buttons, labels, events
neo.show() #----->This displays the GUI window on the screen.
sys.exit(app.exec_()) #------->keeps your app running and responsive