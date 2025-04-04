import openai

# Set your OpenAI API Key here
openai.api_key = "your_openai_api_key_here"


def generate_test_script(test_description):
    prompt = f"Generate a Selenium Python test script for the following test case: {test_description}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a test automation assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()
