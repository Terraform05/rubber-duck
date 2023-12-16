import os
import json


def chat_completion_to_json(response):
    """Extracts relevant data from the OpenAI chat completion response object

    Args:
        response (openai.types.chat.chat_completion.ChatCompletion): OpenAI chat completion response object

    Returns:
        str: JSON representation of chat completion response
    """
    extracted_data = {
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": choice.message.content,
                    "role": choice.message.role,
                },
                "logprobs": choice.logprobs,
            }
            for choice in response.choices
        ],
        "created": response.created,
        "id": response.id,
        "model": response.model,
        "object": response.object,
        "usage": {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens
        }
    }
    return json.dumps(extracted_data, indent=2)


def moderation_to_json(response):
    """Extracts relevant data from the OpenAI text moderation response object

    Args:
        response (openai.types.moderation_create_response.ModerationCreateResponse): OpenAI text moderation response object

    Returns:
        JSON: representation of text moderation response
    """
    extracted_data = {
        "id": response.id,
        "model": response.model,
        "results": [
            {
                "flagged": result.flagged,
                "categories": {category: getattr(result.categories, category) for category in result.categories.__annotations__},
                "category_scores": {category: getattr(result.category_scores, category) for category in result.category_scores.__annotations__}
            }
            for result in response.results
        ]
    }
    return json.dumps(extracted_data, indent=2)


def openai_response_to_json(response):
    """ Converts OpenAI response object to JSON

    Args:
        response (_type_): OpenAI response object

    Raises:
        ValueError: Unsupported response type

    Returns:
        JSON: JSON representation of OpenAI response object
    """
    extraction_functions = {
        "ChatCompletion": chat_completion_to_json,
        "ModerationCreateResponse": moderation_to_json
    }
    extraction_function = extraction_functions.get(type(response).__name__)
    if extraction_function:
        return extraction_function(response)
    else:
        raise ValueError(
            f"Unsupported response type: {type(response)}")


def json_response_to_file(response, folder):
    """ Writes JSON response to a file

    Args:
        response (JSON): JSON response
        folder (String): folder name
    """
    main_folder = "responses"

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    folder_path = os.path.join(main_folder, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    existing_files = [f for f in os.listdir(
        folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    response_index = len(existing_files) + 1

    filename = os.path.join(folder_path, f"response_{response_index}.json")

    with open(filename, 'w') as file:
        json.dump(response, file, indent=2)

    print(f"JSON -w dump >> {filename}")


def write_openai_obj_to_json_file(openai_obj_response, folder="unnamed"):
    """ Writes OpenAI response object to a JSON file

    Args:
        openai_obj_response (_type_): Open AI response object
        folder (str, optional): _description_. Defaults to Open Ai Object type name.
    """

    folder = type(
        openai_obj_response).__name__ if folder == "unnamed" else folder
    json_response = openai_response_to_json(openai_obj_response)
    json_response_to_file(json_response, folder)
