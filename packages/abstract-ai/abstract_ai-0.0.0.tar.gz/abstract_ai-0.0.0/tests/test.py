import requests
import os
import json
import requests
import openai
from abstract_security.envy_it import get_env_value
def get_openai_key(key:str='OPENAI_API_KEY'):
    """
    Retrieves the OpenAI API key from the environment variables.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable containing the API key. Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The OpenAI API key.
    """
    return get_env_value(key=key)
def load_openai_key():
    """
    Loads the OpenAI API key for authentication.
    """
    openai.api_key = get_openai_key()
class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.token_info = {
            "8192": ['gpt-4', 'gpt-4-0314'],
            "32768": ['gpt-4-32k', 'gpt-4-32k-0314'],
            "4097": ['gpt-3.5-turbo', 'gpt-3.5-turbo-0301', 'text-davinci-003', 'text-davinci-002'],
            "8001": ["code-davinci-002", "code-davinci-001"],
            "2048": ['code-cushman-002', 'code-cushman-001'],
            "2049": ['davinci', 'curie', 'babbage', 'ada', 'text-curie-001', 'text-babbage-001', 'text-ada-001']
        }
        self.endpoints = {
            'https://api.openai.com/v1/chat/completions': [
                "gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"],
            'https://api.openai.com/v1/completions': [
                "text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"],
            'https://api.openai.com/v1/edits': [
                "text-davinci-edit-001", "code-davinci-edit-001"],
            'https://api.openai.com/v1/audio/transcriptions': ['whisper-1'],
            'https://api.openai.com/v1/audio/translations': ['whisper-1'],
            'https://api.openai.com/v1/fine-tunes': [
                "davinci", "curie", "babbage", "ada"],
            'https://api.openai.com/v1/embeddings': [
                "text-embedding-ada-002", "text-search-ada-doc-001"],
            'https://api.openai.com/v1/moderations': [
                "text-moderation-stable", "text-moderation-latest"]
        }
    
    def request(self, endpoint, payload):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {get_openai_key()}'
        }
        
        response = requests.post(endpoint, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')
    
    def get_token_info(self, token_length):
        if str(token_length) in self.token_info:
            return self.token_info[str(token_length)]
        else:
            return []
    
    def get_endpoint(self, endpoint_name):
        if endpoint_name in self.endpoints:
            return self.endpoints[endpoint_name]
        else:
            return []
    
    def complete(self, model, prompt, **kwargs):
        endpoint = 'https://api.openai.com/v1/chat/completions' if model in self.endpoints['https://api.openai.com/v1/chat/completions'] else 'https://api.openai.com/v1/completions'
        payload = {'model': model, 'prompt': prompt}
        payload.update(kwargs)
        
        return self.request(endpoint, payload)
    
    def embed(self, model, input_text, **kwargs):
        endpoint = 'https://api.openai.com/v1/embeddings'
        payload = {'model': model, 'input': input_text}
        payload.update(kwargs)
        
        return self.request(endpoint, payload)
    
    def edit(self, model, input_text, instruction, **kwargs):
        endpoint = 'https://api.openai.com/v1/edits'
        payload = {'model': model, 'input': input_text, 'instruction': instruction}
        payload.update(kwargs)
        
        return self.request(endpoint, payload)
    
    def moderate(self, model, input_text, **kwargs):
        endpoint = 'https://api.openai.com/v1/moderations'
        payload = {'model': model, 'input': input_text}
        payload.update(kwargs)
        
        return self.request(endpoint, payload)

openai_api=OpenAIAPI(get_openai_key())
response = openai_api.complete('gpt-4', 'Hello,')
input(response)
# Call the `complete` method
response = openai_api.complete('text-davinci-003', 'Hello,')
print(response)

# Call the `embed` method
embedding = openai_api.embed('text-embedding-ada-002', 'This is a test.')
print(embedding)

# Call the `edit` method
edited_text = openai_api.edit('text-davinci-edit-001', 'This is the input text.', 'Edit the text.')
print(edited_text)

# Call the `moderate` method
moderated_text = openai_api.moderate('text-moderation-latest', 'This is an offensive text.')
print(moderated_text)
