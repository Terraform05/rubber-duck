from openai import OpenAI
from handle_openai_obj import write_openai_obj_to_json_file, openai_response_to_json
from sensitive import OPENAI_ORGANIZATION, OPENAI_API_KEY

client = OpenAI(
    organization=OPENAI_ORGANIZATION,
    api_key=OPENAI_API_KEY
)

MODEL = "gpt-3.5-turbo"


#test of chat completion
completions_response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

print('completions response:')
print(openai_response_to_json(completions_response))
write_openai_obj_to_json_file(completions_response)


#test of moderation
prompt = "I want to kill myself."

moderation_response = client.moderations.create(
    input = prompt,
)

print('\nmoderation response:')
print(openai_response_to_json(moderation_response))
write_openai_obj_to_json_file(moderation_response)
