import os
from concurrent.futures import ThreadPoolExecutor
import openai
from openai import OpenAIError, OpenAI


Open_AI_KEY = "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"

# OPENAI_API_KEY
# client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))
client = openai.OpenAI(api_key=Open_AI_KEY)
executor = ThreadPoolExecutor(max_workers=2)  # Run API call in the background


def generate_test_script(test_description):
    prompt = f"Write a Selenium Python test script using Pytest for: {test_description}"

    # Run OpenAI API call in a separate thread
    try:
        future = executor.submit(client.chat.completions.create,
                                 model="gpt-3.5-turbo",
                                 messages=[{"role": "user", "content": prompt}])

        response = future.result()

        # Access the response correctly: Extracting the generated text
        script_content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        credits_consumed = (tokens_used / 1000) * 0.0015  # Cost for GPT-3.5-turbo (Mar 2025)
        return script_content, credits_consumed
    except OpenAIError as e:
        print(f"Error: {e}")
        return None
