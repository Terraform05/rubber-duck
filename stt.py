import speech_recognition as sr

from tts import say
r = sr.Recognizer()

def listen():
    recognized_audio = ''

    try:
        with sr.Microphone() as mic:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(mic, duration=0.5)  # Use the 'mic' instance here
            print('Adjusted for ambient noise')
            audio = r.listen(mic)
            recognized_audio = r.recognize_google(audio).lower()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error occurred")

    return recognized_audio


# parrot listen and speak back to user
""" while True:
    print("Listening... (Ctrl+C to exit)")
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio = r.listen(source2)

            # Using google to recognize audio
            recognized_text = r.recognize_google(audio).lower()

            print("Did you say:", recognized_text)
            say('Did you say '+recognized_text+'?')

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error occurred") """