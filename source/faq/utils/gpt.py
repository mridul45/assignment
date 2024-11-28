import openai
from decouple import config

api_key = config('API_KEY')

def get_chatgpt_response(user_question):
    try:
        # Use the OpenAI API key stored in settings
        openai.api_key = api_key

        # Call the OpenAI ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        # Extract the assistant's response
        gpt_response = response['choices'][0]['message']['content']
        return gpt_response, None

    except Exception as e:
        return None, str(e)
    


def sanitize_cache_key(question):
    """
    Sanitize the question to create a valid cache key.
    Non-alphanumeric characters are replaced with underscores.
    """
    return ''.join(e if e.isalnum() else '_' for e in question)