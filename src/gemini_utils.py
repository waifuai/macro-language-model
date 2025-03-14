import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

def is_echoed_response(user_response: str, waifu_response: str) -> bool:
    return user_response.lower().strip() == waifu_response.lower().strip()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_with_retry(model, prompt, waifu_response: str):
    # print(f"Calling generate_content with prompt: {prompt[:100]}...")  # Truncate for readability
    response = model.generate_content(prompt)
    # Explicitly decode with UTF-8, replacing errors
    response_text = response.text.encode('utf-8', 'replace').decode('utf-8')
    # Add an extra check for valid UTF-8
    try:
        response_text.encode('ascii')
    except UnicodeEncodeError:
        print("DEBUG: Gemini response contains non-ASCII characters.")
        response_text = response_text.encode('utf-8', 'replace').decode('utf-8')
    else:
        # If it's all ASCII, it's safe, but we still want to return UTF-8
        response_text = response_text.encode('utf-8').decode('utf-8')

    # print(f"Response received: {response_text[:100]}...")  # Truncate for readability
    if is_echoed_response(response.text, waifu_response):
        raise Exception("Echoed response detected. Retrying...")
    return response_text