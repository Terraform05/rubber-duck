from tts import say
from stt import listen


def get_question_by_speech():
    question = None
    recognized_audio = None

    while question == None:
        print("Listening for your question...")

        recognized_audio = listen()

        if recognized_audio != '':

            print(f'You asked: {recognized_audio}')
            print(f'Would you like to proceed with this question?')
            say(f'You asked: {recognized_audio}')
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
                    print('Question misunderstanding...')
                    say('Apologies... Please repeat your question.')
                    break

                else:
                    print('Sorry, I did not understand that. Please say yes or no.')
                    say('Sorry, I did not understand that. Please say yes or no.')

            # yes_or_no = input('Yes or No (y/n): ')

    print('FINAL QUESTION')
    print(question)
    return question


def get_question_by_text():
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
                print('Question misunderstanding...')
                print('Apologies... Please repeat your question.')


    print('FINAL QUESTION')
    print(question)
    return question


get_question_by_text()