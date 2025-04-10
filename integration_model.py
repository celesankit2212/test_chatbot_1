import os
from concurrent.futures import ThreadPoolExecutor
import openai
from openai import OpenAIError, OpenAI
import re


Open_AI_KEY = "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"

# OPENAI_API_KEY
# client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))
client = openai.OpenAI(api_key=Open_AI_KEY)
executor = ThreadPoolExecutor(max_workers=2)  # Run API call in the background


def generate_test_script(test_description):
    if 'API call' not in test_description:
        prompt = f"Write a Selenium Python test script using Pytest without any code comments and in headless mode for: {test_description}"
    else:
        prompt = f"Write a test script in Python without any code comments using Pytest and requests module for: {test_description}"

    # check for password or related email patterns on prompts and make it all dummy
    prompt = sanitize_everything(prompt)

    # Run OpenAI API call in a separate thread
    try:
        future = executor.submit(client.chat.completions.create,
                                 model="gpt-3.5-turbo",
                                 messages=[{"role": "user", "content": prompt}])

        response = future.result()

        # Access the response correctly: Extracting the generated text
        script_content = response.choices[0].message.content
        tokens_used = int(response.usage.completion_tokens) + int(response.usage.prompt_tokens)
        credits_consumed = (tokens_used / 1000) * 0.0015  # Cost for GPT-3.5-turbo (Mar 2025)
        return script_content, credits_consumed
    except OpenAIError as e:
        print(f"Error: {e}")
        return None


def sanitize_everything(text: str) -> str:
    # Email addresses
    text = re.sub(r'(?<=<)[^<>@]+@[^<>@]+\.[^<>@]+(?=>)', 'dummy_text', text)
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'dummy_text', text)

    # Patterns like: password = "abc", password abc, 'password': 'abc'
    sensitive_keywords = ['password', 'passwd', 'pwd', 'email', 'token', 'api_key', 'secret']
    for key in sensitive_keywords:
        # Match patterns like: key = value, key: value, key value (quoted or not)
        regex = rf'({key}\s*[:=]?\s*)(["\']?.+?["\']?)(?=\s|$|,|\n)'
        text = re.sub(regex, rf'\1dummy_text', text, flags=re.IGNORECASE)

    # Phone numbers
    text = re.sub(r'\b(\+?\d{1,3})?[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{4}\b', 'dummy_text', text)

    # Credit card numbers
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', 'dummy_text', text)

    # US Social Security Numbers
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'dummy_text', text)

    # Angle brackets with sensitive-looking content
    text = re.sub(r'<[^<>]{5,}>', 'dummy_text', text)

    # Replace anything quoted that looks suspiciously long
    text = re.sub(r'(["\'])(.{5,}?)(\1)', r'\1dummy_text\1', text)

    return text

