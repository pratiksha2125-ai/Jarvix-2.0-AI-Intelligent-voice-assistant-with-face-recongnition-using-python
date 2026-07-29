
from face_login import face_login
import screen_brightness_control as sbc
from PIL import Image
import datetime
import os
import speech_recognition as sr
import pyautogui
from pycaw.pycaw import AudioUtilities
from google import genai
import webbrowser
import pyttsx3

from config import API_KEY


client = genai.Client(api_key=API_KEY)


def ai_chat(question):
    try:
        response = client.models.generate_content(
            model="models/gemini-3.1-flash-lite",
            contents=question
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"


# ---------------- Text To Speech Setup ----------------

def say(text):
    print("Jarvix 2.0 :", text)

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()

    engine.stop()


# ---------------- Speech Recognition ----------------

def take_command():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.energy_threshold = 300
        r.dynamic_energy_threshold = True

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        except sr.WaitTimeoutError:
            print("No voice detected")
            return ""

    try:

        print("Recognizing...")

        query = r.recognize_google(
            audio,
            language="en-IN"
        )

        print("You said:", query)

        return query.lower()

    except sr.UnknownValueError:
        print("Could not understand")
        return ""

    except sr.RequestError:
        print("Internet problem")
        return ""


# ---------------- Volume Control ----------------

def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    volume = devices.EndpointVolume
    return volume


def volume_up():
    volume = get_volume_control()

    current = volume.GetMasterVolumeLevelScalar()

    volume.SetMasterVolumeLevelScalar(
        min(current + 0.1, 1.0),
        None
    )


def volume_down():
    volume = get_volume_control()

    current = volume.GetMasterVolumeLevelScalar()

    volume.SetMasterVolumeLevelScalar(
        max(current - 0.1, 0.0),
        None
    )


# ---------------- Brightness Control ----------------

def brightness_up():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(min(current + 10, 100))


def brightness_down():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(max(current - 10, 0))


# ---------------- Websites ----------------

sites = {

    "youtube": "https://www.youtube.com",

    "google": "https://www.google.com",

    "wikipedia": "https://www.wikipedi0a.org",

    "github": "https://github.com",

    "chatgpt": "https://chat.openai.com",

    "facebook": "https://www.facebook.com",

    "instagram": "https://www.instagram.com",

    "linkedin": "https://www.linkedin.com",

    "twitter": "https://twitter.com",

    "amazon": "https://www.amazon.in",

    "flipkart": "https://www.flipkart.com",

    "gmail": "https://mail.google.com",

    "netflix": "https://www.netflix.com",

    "spotify": "https://open.spotify.com"

}


# ---------------- Applications ----------------

apps = {

    "camera": "microsoft.windows.camera:",

    "calculator": "calc.exe",

    "notepad": "notepad.exe",

    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",

    "files": "explorer.exe",

    "whatsapp": "whatsapp:"

}


# ---------------- Close Applications ----------------

close_process = {

    "camera": "WindowsCamera.exe",

    "calculator": "CalculatorApp.exe",

    "notepad": "notepad.exe",

    "word": "WINWORD.EXE",

    "files": "explorer.exe",

    "whatsapp": "WhatsApp.Root.exe"
}

# ---------------- Main Program ---------------

if __name__ == "__main__":

    # -------- Face Authentication --------

    if face_login():
        say("Welcome Pratiksha. Jarvix 2.0 activated.")
    else:
        say("Face not recognized. Access denied.")
        exit()

    say("Hello, I am Jarvix 2.0")

    # -------- Main Jarvis Loop --------

    while True:

        query = take_command().lower()

        if query == "":
            continue

        # ---------------- Exit Command ----------------

        if "exit" in query or "quit" in query or "stop" in query:
            say("Goodbye mam, shutting down")
            break

        # ---------------- Open Websites ----------------

        for site in sites:
            if f"open {site}" in query:
                say(f"Opening mam {site}")
                webbrowser.open(sites[site])
                break

        # ---------------- Close Browsers ----------------

        if "close browser" in query or "close chrome" in query:
            say("Closing browser mam")
            os.system("taskkill /f /im chrome.exe")

        elif "close microsoft" in query.lower():
            say("Closing Microsoft Edge")
            os.system("taskkill /f /im msedge.exe")

        # ---------------- Open Applications ----------------

        for application in apps:
            if f"open {application}" in query:
                say(f"Opening mam {application}")

                try:
                    os.startfile(apps[application])
                except Exception as e:
                    print(e)
                    say("Application not found")

                break

        # ---------------- Close Applications ----------------

        for application in close_process:
            if f"close {application}" in query:
                say(f"Closing {application}")

                os.system(
                    f"taskkill /f /im {close_process[application]}"
                )

                break

        # ---------------- Open Music Folder ----------------

        if "open music" in query:
            music_path = r"C:\Users\Pratiksha\Music"
            if os.path.exists(music_path):
                say("Opening music folder")
                os.startfile(music_path)
            else:
                say("Music folder not found")

        # ---------------- Time Command ----------------

        if "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Mam, the time is {current_time}")

        elif "date" in query:
            today = datetime.datetime.now()
            date = today.strftime("%d %B %Y")

            say(f" mam Today's date is {date}")

        elif "shutdown" in query:
            say("Shutting down your computer mam")
            os.system("shutdown /s /t 5")

        elif "restart" in query:
            say("Restarting your computer mam")
            os.system("shutdown /r /t 5")

        elif "lock computer" in query:
            say("Locking your computer mam")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "take screenshot" in query:

            say("Taking screenshot mam ")

            path = "Screenshots"

            if not os.path.exists(path):
                os.mkdir(path)

            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            screenshot = pyautogui.screenshot()

            file_path = f"{path}/{filename}.png"

            screenshot.save(file_path)

            say("Screenshot saved successfully")

            # Open screenshot
            img = Image.open(file_path)
            img.show()

        # ---------------- Volume Commands ----------------

        elif "increase volume" in query or "volume up" in query:
            say("Increasing volume mam")
            volume_up()

        elif "decrease volume" in query or "volume down" in query:
            say("Decreasing volume mam")
            volume_down()

        # ---------------- Brightness Commands ----------------

        elif "increase brightness" in query or "brightness up" in query:
            say("Increasing brightness mam")
            brightness_up()

        elif "decrease brightness" in query or "brightness down" in query:
            say("Decreasing brightness mam")
            brightness_down()

        # ---------------- Scroll Commands ----------------

        elif "scroll up" in query:
            pyautogui.scroll(500)
            say("Scrolling up")

        elif "scroll down" in query:
            pyautogui.scroll(-500)
            say("Scrolling down")

        # ---------------- Chat Mode ----------------

        elif "chat mode" in query:
            say("AI chat mode activated.")
            while True:

                user_query = take_command().lower()
                if "exit chat mode" in user_query:
                    say("Leaving chat mode.")
                    break
                answer = ai_chat(user_query)
                print("Jarvix 2.0 :", answer)
                say(answer)