from openai import OpenAI
from sensitive import OPENAI_API_KEY, OPENAI_ORGANIZATION

client = OpenAI(
    organization=OPENAI_ORGANIZATION,
    api_key=OPENAI_API_KEY
)

print(client.beta.assistants.list())

for ass in client.beta.assistants.list():
    client.beta.assistants.delete(ass.id)

print(client.beta.assistants.list())
