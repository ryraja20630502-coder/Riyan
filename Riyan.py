import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import time
import wikipedia
import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


# =========================
# TEXT TO SPEECH SETUP
# =========================
engine = pyttsx3.init()
voices = engine.getProperty('voices')       # getting details of current voice
engine.setProperty('voice', voices[4].id)
engine.setProperty("rate",160)


# =========================
# Function to speak
# =========================
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    time.sleep(0.2) ## tiny pause to avoid microphone conflicts

# =========================
# SPEECH INPUT
# =========================
def command():
    # Recognizing speech came from user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source,phrase_time_limit=6)

            #Using google speech recognizer
            try:
                content = r.recognize_google(audio, language='en')
                print("You said:", content)
                return content.lower()
            except sr.UnknownValueError:
                print("Could not understand, please repeat...")
                speak("Could not understand, please repeat.")
            except sr.RequestError:
                print("Service error, please check your internet.")
                speak("Service error, please check your internet.")
                return ""



# =========================
# DICTIONARY OF IMPORTANT WEBSITES
# =========================
websites = {
    "google": "https://www.google.com",
    "internshala": "https://internshala.com",
    "AI": "https://chat.openai.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
    "geeksforgeeks": "https://www.geeksforgeeks.org",
    "w3schools": "https://www.w3schools.com",
    "stackoverflow": "https://stackoverflow.com",
    "leetcode": "https://leetcode.com",
    "codeforces": "https://codeforces.com",
    "coursera": "https://www.coursera.org",
    "udemy": "https://www.udemy.com"
}

# =========================
# DICTIONARY OF IMPORTANT APPLICATIONS
# =========================
applications = {
    "safari": "Safari",
    "terminal": "Terminal",
    "vs code": "Visual Studio Code",
    "notes": "Notes",
    "cap cut": "CapCut",
    "mk player": "MKPlayer",
    "chrome": "Google Chrome",
    "notion": "Notion",
    "page": "Pages",
    "whatsapp": "WhatsApp",
    "instagram": "Instagram",
    "chatgpt": "ChatGPT",
    "gemini": "Gemini",
    "youtube": "YouTube",
    "mail": "Mail"
}

# Function to OPEN APPS
def open_app(app_name):
    os.system(f'open -a "{app_name}"')




# =========================
# GEMINI SETUP
# =========================

# Pass your API key here or set it as an environment variable GEMINI_API_KEY
client = genai.Client(api_key="AIzaSyBBjg4icb30o2kpFOVrtneukhyBS9eipvU")

# 1. Text Generation (Using Gemini 3 Flash)
def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "I'm unable to think right now."

# 2. Image Generation (Using Nano Banana / Gemini 2.5)
def generate_image(prompt):
    try:
        speak("Generating the image for you, Neeraj. Please wait.")
        # We use the specific image model for this call
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )
        
        # Look for image data in the response parts
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                img = Image.open(BytesIO(part.inline_data.data))
                img.save("riyan_generated.png")
                img.show()
                return "Image generated and saved successfully!"
        return "The model didn't return an image. Try a different prompt."
    except Exception as e:
        if "429" in str(e):
            print("Quota exceeded")
            speak("I am a bit tired from drawing. Let's wait, Neeraj.")
            time.sleep(60) # Force a wait
        else:
            print(f"Error: {e}")

# =========================
# SAVE CHAT HISTORY
# =========================
def save_chat(role, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {role}: {message}\n")


def direct_ai_answer(prompt):
    try:
        # We send ONLY the question, no history, for a fast direct answer
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt + " (Give a very short, direct answer in one sentence)"
        )
        return response.text
    except Exception as e:
        return "I'm having trouble finding that right now."


# =========================
# CONVERSATION MEMORY (RAM)
# =========================
riyan_chat = [
    {
        "role": "user",
        "parts": [{"text": "You are an AI assistant named Riyan. Always greet the user by saying 'Hare Krishna Neeraj' at the start of your response."}]
    },
    {
        "role": "model",
        "parts": [{"text": "Hare Krishna Neeraj! I understand. I am Riyan, your assistant."}]
    }
]




# =========================
# MAIN PROCESS
# =========================
## Main processing to access the system
def main_process():
    while True:
        query=command().lower()

        # =========================
        # --- GREETING ---
        # =========================
        if "hare krishna riyan" in query:
            greeting="Hare Krishna Neeraj! How can i help you"
            speak(greeting)
            print(greeting)

        # =========================
        # --- Date and Time Logic ---
        # =========================

        # Telling the Time
        elif "say time" in query:
            # Formats time as: HH:MM AM/PM
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak("The current time is:"+ str(current_time))

        # Telling the Date
        elif "say date" in query:
            # Formats date as: Day, Month Date, Year
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {current_date}")

        # =========================
        # Making todo list
        # =========================
        elif "add new task" in query:
            task=query.replace("add new task","")
            task=task.strip()
            if task !="":
                speak("Adding new task :"+ task)
                with open ("todo.txt", "a") as file:
                    file.write(task + "\n")

        # =========================
        #speaking todo list from todo.txt
        # =========================
        elif "speak task" in query:
            with open ("todo.txt", "r") as file:
                    speak("Work we have to do taday are:" + file.read())
        # =========================
        # Searching wikipedia
        # =========================
        elif "wikipedia" in query:
            query = query.replace("riyan ","")
            query = query.replace("search wikipedia ","").strip()
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
            

        # =========================
        # Searching google
        # =========================
        elif "google" in query:
            query = query.replace("riyan ","")
            query = query.replace("search google ","").strip()
            webbrowser.open("https://www.google.com/search?q="+ query)
        

        # =========================
        # --- IMAGE GENERATION LOGIC ---
        # =========================
        elif "generate image" in query or "draw" in query:
            # Extract prompt: "Riyan generate image of a blue cat" -> "a blue cat"
            prompt = query.replace("generate image", "").replace("draw", "").replace("riyan", "").strip()
            if prompt:
                status = generate_image(prompt)
                speak(status)
            else:
                speak("What should I draw, Neeraj?")


        # ==========================================
        # If the query doesn't match any command, ask AI directly
        # ==========================================


        # WH-QUESTIONS & YES/NO QUESTION LOGIC
        # 1. Define lists of words that start questions
        wh_words = ("who", "what", "where", "when", "why", "how", "which", "whose")
        yn_words = ("do", "does", "did", "is", "are", "am", "was", "were", 
                    "have", "has", "can", "could", "will", "would", "should")

        # 2. Check if the query starts with any of these question words
        # (We strip 'riyan' first to accurately detect the first word)
        clean_query = query.replace("riyan", "").strip()
        
        if clean_query.startswith(wh_words) or clean_query.startswith(yn_words):
            save_chat("User", clean_query)

            # Use the riyan_chat memory for context
            riyan_chat.append({"role": "user", "parts": [{"text": clean_query}]})
            
            speak("Let me check... neeraj")
            
            # Get response from Gemini
            ai_response = ask_gemini(riyan_chat)
            
            # Save and Speak
            riyan_chat.append({"role": "model", "parts": [{"text": ai_response}]})
            save_chat("Gemini", ai_response)
            
            if not ai_response.lower().startswith("hare krishna neeraj"):
                ai_response = "Hare Krishna Neeraj! " + ai_response
                
            print("Riyan:", ai_response)
            speak(ai_response)
            continue # Skip the rest of the loop to avoid double-processing

        # =========================
        # ASK AI WITH MEMORY
        # =========================
        elif "ask ai" in query:
            # Clean the query so we don't send "riyan ask ai..." to the model
            request = query.replace("ask ai", "").replace("riyan", "").strip()
            
            if not request:
                speak("What would you like to ask?")
                continue

            save_chat("User", request)
            
            # Use the correct dictionary format for the append
            riyan_chat.append({"role": "user", "parts": [{"text": request}]})
            
            ai_response = ask_gemini(riyan_chat)

            # Append the response using the 'model' role
            riyan_chat.append({"role": "model", "parts": [{"text": ai_response}]})
            
            save_chat("Gemini", ai_response)
            
            if not ai_response.lower().startswith("hare krishna neeraj"):
                ai_response = "Hare Krishna Neeraj! " + ai_response
                
            print("Riyan:", ai_response)
            speak(ai_response)
        
        elif "read chat history" in query:
            if os.path.exists("chat_history.txt"):
                with open("chat_history.txt", "r", encoding="utf-8") as file:
                    speak(file.read())
            else:
                speak("No chat history found")

        # Clear chat memory and history
        elif "clear chat" in query or "reset chat" in query:
            # Clear RAM memory
            riyan_chat.clear()
            
            # Reset initial greeting in RAM
            riyan_chat.append({
                "role": "user",
                "parts": [{"text": "You are an AI assistant named Riyan. Always greet the user by saying 'Hare Krishna Neeraj' at the start of your response."}]
            })
            riyan_chat.append({
                "role": "model",
                "parts": [{"text": "Hare Krishna Neeraj! I understand. I am Riyan, your assistant."}]
            })
            
            # Clear chat history file
            if os.path.exists("chat_history.txt"):
                open("chat_history.txt", "w").close()  # empty the file
            
            speak("Chat history has been cleared. I am ready for new conversations!")
            print("Chat memory and history cleared.")

        
        # =========================
        # Check if user wants to open a website
        # =========================
        for name in websites:
            if f"riyan open {name}" in query:
                speak(f"Opening {name}")
                webbrowser.open(websites[name])
                break  # stop checking once matched

        # =========================
        # Application open
        # =========================
        if "open" in query:
            for app in applications:
                if app in query:
                    speak(f"Opening {app}")
                    open_app(applications[app])
                    break
        
        # =========================
        # Optional: exit loop
        # =========================
        if "exit" in query or "quit" in query:
            speak("Goodbye! Have a nice day neeraj.")
            break

if __name__ == "__main__":
    main_process()