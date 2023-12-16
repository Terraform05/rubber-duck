from openai import OpenAI
from sensitive import OPENAI_ORGANIZATION, OPENAI_API_KEY

client = OpenAI(
    organization=OPENAI_ORGANIZATION,
    api_key=OPENAI_API_KEY
)

"""
file = client.files.create(
    file = open("speech.py", "rb"),
    purpose = "assistants"
) """

assistant = client.beta.assistants.create(
    name = "Java Tutor",
    instructions="You are a personal computer science tutor for the language Java. When asked a question, explain the Java coding logic, structure, and syntax neded to solve the problem. If you do not know the answer, ask questions to help you fully understand the problem.",
    model="gpt-4-1106-preview",
    tools=[{"type": "code_interpreter"}]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role = "user",
    content="What is a for loop?"   
)

print(message)

run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id
)

messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

for message in reversed(messages):
    print(message.role + ": "+message.content[0].text.value)
