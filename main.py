from openai import OpenAI
from sensitive import OPENAI_API_KEY, OPENAI_ORGANIZATION
from get_question import get_question_by_speech, get_question_by_text
import time
from tts import say
from other import highlight_string


class JavaTutor:

    assistant = None  # establish single assistant. Theoretically use same assistant for all threads, but I don't want to leave assistant open
    thread = None  # establish single thread

    def __init__(self, client):
        # Create assistant
        self.assistant = client.beta.assistants.create(
            name="Java Tutor",
            instructions="You are a personal computer science tutor for the language Java. When asked a question, explain the Java coding logic, structure, and syntax neded to solve the problem using only text as if you were talking to a student. Be extremely concise and clear, asking questions to clarify the students understanding.",
            model="gpt-4-1106-preview",
            tools=[{"type": "code_interpreter"}]
        )
        # Create thread
        self.thread = client.beta.threads.create()

    # execute run assistant on thread

    def run_assistant(self):
        self.run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            # instructions = f"Please address the user as {name}"
        )

    # Wait for the run to finish

    def wait_on_run(self):
        while self.run.status == "queued" or self.run.status == "in_progress":
            self.run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id,
            )
            time.sleep(0.5)

    # Get the answer from the run
    def get_thread_messages(self):
        self.thread_messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

    # Get the most recent assistant answer from thread messages
    def get_last_message(self):
        thread_messages = self.get_thread_messages()
        last_assistant = {}
        last_user = {}
        for message in reversed(thread_messages.data[-2:]):
            content = message.content[0].text.value
            if message.role == 'assistant':
                last_assistant = {
                    "role": message.role,
                    "content": content
                }
            if message.role == 'user':
                last_user = {
                    "role": message.role,
                    "content": content
                }
        return last_assistant, last_user

    # prints latest message by printing user question and then gpt answer
    def print_last_message(self, last_assistant, last_user):
        print(highlight_string(last_user.role+":\n")+last_user.content)
        print()
        print(highlight_string(last_assistant.role+":]n")+last_assistant.content)

    # Ask a question to the assistant on this thread
    def ask_question(self, question):
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=get_question_by_speech(question)
        )

    def say_answer(self, answer):
        say(answer)

    def cleanup(self):
        client.beta.assistants.delete(
            assistant_id=self.assistant.id
        )
        print(client.beta.assistants.list())

    def do_tutoring(self):
        self.ask_question()
        self.run_assistant()
        self.wait_on_run()
        last_assistant, last_user = self.get_last_message()
        self.say_answer(last_assistant.content)
        self.print_last_message(last_assistant, last_user)


if __name__ == "__main__":

    client = OpenAI(
        organization=OPENAI_ORGANIZATION,
        api_key=OPENAI_API_KEY
    )

    AlexGPTutor = JavaTutor(client)

    active_session = True
    while active_session == True:

        AlexGPTutor.do_tutoring()

        x = ''
        while x not in ['y', 'yes', 'n', 'no']:
            x = input('Continue Tutoring Session? Yes or No (y/n): ').lower()
            if x in ['y', 'yes']:
                print('continuing...')
            else:
                active_session = False
                break

    AlexGPTutor.cleanup()

    print('program end')
