import requests
import openai
import os
import json
import requests
import openai
from abstract_security.envy_it import get_env_value
from abstract_utilities.time_utils import get_time_stamp,get_date
from tokenization import count_tokens, check_token_size
from prompts import default_prompt,create_prompt,default_tokens
from endpoints import default_model,default_endpoint
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

        openai.api_key = self.api_key
    
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

    def request(self, endpoint, payload):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        response = requests.post(endpoint, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Request failed with status code {response.status_code}')
    
    def complete(self, model, prompt, **kwargs):
        endpoint = 'https://api.openai.com/v1/chat/completions' if 'chat' in model else 'https://api.openai.com/v1/completions'
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


class OpenAIRequest:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

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
    
    def openai_request(self, method_name:str, model_name:str, params:dict):
        for key in self.endpoints:
            if model_name in self.endpoints[key]:
                endpoint = key
                break
        else:
            raise ValueError('Invalid model name')

        # Use the endpoint to call the appropriate function
        if "chat/completions" in endpoint:
            response = openai.ChatCompletion.create(engine=model_name, **params)
        elif "completions" in endpoint:
            response = openai.Completion.create(engine=model_name, **params)
        elif "edits" in endpoint:
            response = openai.Editing.create(engine=model_name, **params)
        elif "audio/transcriptions" in endpoint:
            response = openai.Transcription.create(engine=model_name, **params)
        elif "audio/translations" in endpoint:
            response = openai.Translation.create(engine=model_name, **params)
        elif "fine-tunes" in endpoint:
            response = openai.FineTuning.create(engine=model_name, **params)
        elif "embeddings" in endpoint:
            response = openai.Embedding.create(engine=model_name, **params)
        elif "moderations" in endpoint:
            response = openai.Moderation.create(engine=model_name, **params)
        else:
            raise ValueError('Unsupported method name')

        return response


class CombinedAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai_api = OpenAIAPI(api_key)
        self.openai_request = OpenAIRequest(api_key)
    
    def request(self, model_name:str, params:dict):
        if model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/chat/completions'):
            return self.openai_api.complete(model_name, params['prompt'], **params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/completions'):
            return self.openai_api.complete(model_name, params['prompt'], **params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/edits'):
            return self.openai_api.edit(model_name, params['input'], params['instruction'], **params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/audio/transcriptions'):
            return self.openai_request.openai_request(method_name, model_name, params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/audio/translations'):
            return self.openai_request.openai_request(method_name, model_name, params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/fine-tunes'):
            return self.openai_request.openai_request(method_name, model_name, params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/embeddings'):
            return self.openai_request.openai_request(method_name, model_name, params)
        elif model_name in self.openai_api.get_endpoint('https://api.openai.com/v1/moderations'):
            return self.openai_request.openai_request(method_name, model_name, params)
        else:
            raise ValueError('Unsupported model name')

# Example usage:
load_openai_key()

# Call the `request` method
response = CombinedAPI.request('complete', 'text-davinci-003', {'prompt': 'Hello,', 'temperature': 0.8})
print(response)

# Call the `request` method with different parameters
response = CombinedAPI.request('complete', 'gpt-4', {'prompt': 'Hello,', 'temperature': 0.8})
print(response)
