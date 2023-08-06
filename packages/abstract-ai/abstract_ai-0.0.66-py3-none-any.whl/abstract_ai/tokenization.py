from nltk.tokenize import word_tokenize
def count_tokens(text):
    """
    Counts the number of tokens in the given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of tokens.
    """
    return len(word_tokenize(text))
def create_chunks(content, size_per_chunk):
    words = content.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(' '.join(current_chunk)) + len(word) > size_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(word)
    chunks.append(' '.join(current_chunk))
    return chunks
def calculate_token_distribution(max_tokens, prompt:str, completion_percentage:float=40, size_per_chunk:int=None):
    prompt_length = count_tokens(prompt)
    prompt_percentage = 1 - completion_percentage
    prompt_available = int(float(max_tokens) * float(prompt_percentage)) - int(prompt_length)
    completion_available = float(max_tokens) * float(completion_percentage)
    completion_desired = float(max_tokens) * float(completion_percentage)
    if size_per_chunk == None:
        size_per_chunk =float(max_tokens) * float(prompt_percentage)
    num_chunks = prompt_length // size_per_chunk + 1 if prompt_length % size_per_chunk > 0 else prompt_length // size_per_chunk

    chunked_data = create_chunks(prompt, size_per_chunk)

    token_distribution = {
        "percent_distribution": {
            "prompt": prompt_percentage * 100,
            "completion": completion_percentage * 100
        },
        "prompt": {
            "available": prompt_available,
            "used": prompt_length,
            "desired": max_tokens * prompt_percentage
        },
        "completion": {
            "available": prompt_available + completion_available,
            "used": 0,
            "desired": completion_desired
        },
        "chunks": {
            "total": num_chunks,
            "length_per": size_per_chunk,
            "data": chunked_data
        }
    }

    return token_distribution

