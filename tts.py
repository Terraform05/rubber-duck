import os

#revert to ava later
def say(text, voice = 'Ava (Premium)'):
    try:
        os.system(f'say -v "{voice}" "{text}"')
    except:
        os.system(f'say "Error occurred: {voice} not found."')
   
#names = ['Allison (Enhanced)', 'Ava (Premium)', 'Evan (Enhanced)', 'Samantha (Enhanced)', 'Siri', 'Isha (Premium)', 'Rishi (Enhanced)']
#for name in names:
#    say(f'I am {name}.', name)