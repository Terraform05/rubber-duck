from openai import OpenAI
from sensitive import OPENAI_API_KEY, OPENAI_ORGANIZATION
from get_question import get_question_by_speech
from tts import say
from helpers import *
import sys
import time


@check_arguments(OpenAI)
class JavaTutor:
    """Methods for tutoring a student in Java using OpenAi's Beta Assistants API with GPT-4-1106-preview model"""

    assistant = None  # establish single assistant. Theoretically use same assistant for all threads, but I don't want to leave assistant open
    thread = None  # establish single thread

    def __init__(self, client):
        """ Initializes a new instance of the Java Tutor OpenAi Assistant class. If an active assistant exists, it is retrieved; otherwise, a new assistant is created. Then, a new cread is created for the assistant.

        Args:
            client (openai.OpenAi): An OpenAI client with a valid API key and organization ID.

        Returns:
            None

        """
        # Create assistant
        assistant_list = client.beta.assistants.list()
        if (assistant_list.last_id != None):
            self.assistant = client.beta.assistants.retrieve(
                assistant_list.last_id)
            print('retreived assistant')
        else:
            self.assistant = client.beta.assistants.create(
                name="Java Tutor",
                instructions="You are a personal computer science tutor for the language Java. When asked a question, explain the Java coding logic, structure, or syntax neded to solve the problem using only text as if you were speaking to a student. Be extremely concise and clear, asking questions to clarify the students understanding. Explain only the concepts simply and do not provide examples",
                model="gpt-4-1106-preview",
                tools=[{"type": "code_interpreter"}]
            )
            print('new assistant')
        # Create thread
        self.thread = client.beta.threads.create()

    # execute run assistant on thread
    def run_assistant(self):
        """
        Initiates the assistant to respond to a Java programming question.

        Raises:
            OpenAiApiError: If there is an issue with the OpenAI API during the assistant's execution.

        Returns:
            None
        """
        self.run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=f"Please answer the question about the programming language Java in a very short response. Be extremely concisely and clear, explaining the Java concepts simply as if you were a tutor speaking directly to the student. Do not provide examples."
        )

    # Wait for the run to finish
    def wait_on_run(self):
        """
        Waits for the assistant's response to finish processing.

        This method continuously checks the status of the assistant's run within the specified thread.
        It waits until the run is no longer in the 'queued' or 'in_progress' state.

        Returns:
            None
        """
        while self.run.status == "queued" or self.run.status == "in_progress":
            self.run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id,
            )
            sys.stdout.write('\rloading |')
            time.sleep(0.1)
            sys.stdout.write('\rloading /')
            time.sleep(0.1)
            sys.stdout.write('\rloading -')
            time.sleep(0.1)
            sys.stdout.write('\rloading \\')
            time.sleep(0.1)
        print('Response Received - Done!\n')

    # Get the answer from the run
    def get_thread_messages(self):
        """
        Retrieves messages from the assistant's thread.

        Returns:
            List: A list of messages in the assistant's thread.
        """
        thread_messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        return thread_messages

    # Get the most recent assistant answer from thread messages
    def get_last_message(self):
        """
        Retrieves the most recent assistant answer and user message from the thread.

        Returns:
            Tuple: A tuple containing the most recent assistant answer and user message.
                   Each element is a tuple with the role ('assistant' or 'user') and the associated text value content.
        """
        thread_messages = self.get_thread_messages()
        last_assistant = {}
        last_user = {}
        # print(highlight_string(thread_messages.data))
        for message in thread_messages.data[-2:]:
            content = message.content[0].text.value.replace("`", "'")
            if message.role == 'assistant':
                last_assistant = (message.role, content)
            if message.role == 'user':
                last_user = (message.role, content)
        return last_assistant, last_user

    # prints latest message by printing user question and then gpt answer
    def print_last_message(self, last_assistant, last_user):
        """
        Prints the latest user question and GPT assistant answer.

        Args:
            last_assistant (tuple): A tuple with the role ('assistant') and the content of the last assistant message.
            last_user (tuple): A tuple with the role ('user') and the content of the last user message.

        Returns:
            None
        """
        print(highlight_string(last_user[0]+":\n")+last_user[1])
        print()
        print(highlight_string(last_assistant[0]+":\n")+last_assistant[1])

    # Ask a question to the assistant on this thread
    def ask_question(self, question=None):
        """
        Adds a user question to the assistant's thread.

        Args:
            question (str, optional): The user's question. If not provided, it is obtained by speech.

        Returns:
            None
            
        Dependencies:
            This function depends on the 'get_question_by_speech' function for speech-based question retrieval.
        """
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=get_question_by_speech(question=None)
        )

    # speak response out loud
    def say_answer(self, answer):
        """
        Speaks the provided answer out loud.

        This method utilizes the 'say' function to audibly communicate the given answer.

        Args:
            answer (str): The text to be spoken.

        Returns:
            None

        Dependencies:
            This function depends on the 'say' function for audio output.
        """
        say(answer)

    # delete assistant at end
    def cleanup(self):
        """
        Deletes the assistant at the end of the session.

        This method removes the assistant associated with the current instance.

        Returns:
            None
        """
        client.beta.assistants.delete(
            assistant_id=self.assistant.id
        )
        print(client.beta.assistants.list())

    # perform sinple action of tutoring
    def tutor_single_response(self):
        """
        Conducts a single question tutor response using the assistant.

        This method sequentially performs the following steps:
        1. Asks a question.
        2. Runs the assistant to generate a response.
        3. Waits for the assistant's response to finish processing.
        4. Retrieves and prints the most recent conversation.
        5. Speaks the assistant's answer out loud.

        Returns:
            None
        """
        self.ask_question()
        self.run_assistant()
        self.wait_on_run()
        last_assistant, last_user = self.get_last_message()
        self.print_last_message(last_assistant, last_user)
        self.say_answer(last_assistant[1])
        
    # perform loop action of tutoring
    def tutor_loop_response(self):
        """
        Performs a looped tutoring session.
    
        This method iteratively conducts tutoring sessions by repeatedly calling the 'tutor_single_response'
        method. The user is prompted to continue the tutoring session after each interaction.
    
        Returns:
            None
        """
        active_session = True
        while active_session == True:

            self.tutor_single_response()

            x = ''
            while x not in ['y', 'yes', 'n', 'no']:
                x = input('Continue Tutoring Session? Yes or No (y/n): ').lower()
                if x in ['y', 'yes']:
                    print('continuing...')
                else:
                    active_session = False
                    break

        self.cleanup()
        print('Tutor Session Ended')
        


if __name__ == "__main__":

    client = OpenAI(
        organization=OPENAI_ORGANIZATION,
        api_key=OPENAI_API_KEY
    )

    AlexGPTutor = JavaTutor(client)
    AlexGPTutor.tutor_loop_response()
