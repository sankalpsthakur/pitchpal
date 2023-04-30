import openai
import requests
import json

def openai_response(prompt):
    try:
        model_engine = "text-davinci-002"
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=150, n=1, stop=None, temperature=0.8)
        if response.status != 200:
            return None
        return response.choices[0].text.strip()
    except Exception as e:
        print(e)
        return None