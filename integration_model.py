import os
from concurrent.futures import ThreadPoolExecutor
import openai
from openai import OpenAIError, OpenAI


# OPENAI_API_KEY
client = openai.OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))
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
        return script_content
    except OpenAIError as e:
        print(f"Error: {e}")
        return None
