#from tts import say
from stt import listen

#can override by passing in a question
def get_question_by_speech(question = None):
    """
    Gets a question from the user through speech inquiry.
    
    Args:
        question (str, optional): The user's question. If not provided, it is obtained by speech.
        
    Returns:
        str: The user's question.
    """
    question = None
    recognized_audio = None

    while question == None:
        print("Listening for your question...")

        recognized_audio = listen()

        if recognized_audio != '':
            question = recognized_audio # skip confirmation
            """ print(f'You asked: {recognized_audio}')
            say(f'Did you ask: {recognized_audio}')
            
            print(f'Yes or No')
            say(f'Yes or No')

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
                    say('Sorry, I didn\'t catch that Please say yes or no.') """

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