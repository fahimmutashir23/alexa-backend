from django.http import JsonResponse
import json
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit



# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
alexa = pyttsx3.init()
voices = alexa.getProperty('voices')
alexa.setProperty('voice', voices[0].id)

def talk(text):
    alexa.say(text)
    alexa.runAndWait()

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'hey lady' in command:
                command = command.replace('hey lady', '')
    except Exception as e:
        print(f"Error: {e}")
    return command

def run_alexa(command):
    response_text = ""
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        response_text = 'Current Time is ' + time
        talk(response_text)

    elif 'play' in command:
        song = command.replace('play', '')
        pywhatkit.playonyt(song)
        response_text = f"Playing {song} on YouTube"
        print(response_text)

    else:
        response_text = 'I did not understand'
        talk(response_text)
    return response_text


def alexa_api_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        command = data.get('command', None)
        if command:
            response_command = run_alexa(command)
            return JsonResponse({'response': response_command, 'success': 'true'})
        else:
            return JsonResponse({'error': 'No command provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
