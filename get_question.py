from tts import say
from stt import listen

#can override by passing in a question
def get_question_by_speech(question = None):
    question = None
    recognized_audio = None

    while question == None:
        print("Listening for your question...")

        recognized_audio = listen()

        if recognized_audio != '':

            print(f'You asked: {recognized_audio}')
            say(f'You asked: {recognized_audio}')
            
            print(f'Would you like to proceed with this question? Yes or No')
            say(f'Would you like to proceed with this question? Yes or No')

            yes_or_no = ''
            while yes_or_no != 'yes' or yes_or_no != 'no':
                yes_or_no = listen()
                if yes_or_no == 'yes':
                    print('Proceeding...')
                    say('Proceeding...')
                    question = recognized_audio
                    break
                elif yes_or_no == 'no':
                    print('Apologies... Please repeat your question.')
                    say('Apologies... Please repeat your question.')
                    break

                else:
                    print('Sorry, I didn\'t catch that. Please say yes or no.')
                    say('Sorry, I didn\'t catch that Please say yes or no.')

    return question

""" 
# can override by passing in a question
def get_question_by_text(question = None):
    question = None
    recognized_text = None

    while question is None:
        recognized_text = input('Enter your question: ')
        if recognized_text != '':
            print(f'You asked: {recognized_text}')
            print('Would you like to proceed with this question?')
            yes_or_no = ''
            
            while yes_or_no not in ['y', 'yes', 'n', 'no']:
                yes_or_no = input('Yes or No (y/n): ').lower()

            if yes_or_no in ['y', 'yes']:
                print('Proceeding...')
                question = recognized_text
            else:
                print('Sorry, I didn\'t catch that. Please say yes or no.')

    return question """


#get_question_by_speech()
#get_question_by_text()