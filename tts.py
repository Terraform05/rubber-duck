import os

#revert to ava later
def say(text, voice = 'Ava (Premium)'):
    """
    Uses the system's text-to-speech functionality to speak the provided text using the specified voice.

    Args:
        text (str): The text to be spoken.
        voice (str, optional): The voice to use for speech. Defaults to 'Ava (Premium)'. Options ['Allison (Enhanced)', 'Ava (Premium)', 'Evan (Enhanced)', 'Samantha (Enhanced)', 'Isha (Premium)', 'Rishi (Enhanced)']

    Returns:
        None
    """
    try:
        os.system(f'say -v "{voice}" "{text}"')
    except:
        os.system(f'say "Error occurred: {voice} not found."')
   
   
   
#listen to each voice one by one
#names = ['Allison (Enhanced)', 'Ava (Premium)', 'Evan (Enhanced)', 'Samantha (Enhanced)', 'Siri', 'Isha (Premium)', 'Rishi (Enhanced)']
#for name in names:
#    say(f'Hi I\'m {name}', name)