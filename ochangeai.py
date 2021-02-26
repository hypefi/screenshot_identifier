import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
print(openai.api_key)
def english_correct(texts):
    texts = texts + "\nStandard American English:"

    print(texts)
    response = openai.Completion.create(
      engine="davinci",
      prompt=texts,
      temperature=0,
      max_tokens=60,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\n"]
    )
    return response

txt = input("Type something to correct: ")

cortxt = english_correct(txt)

print("corrected sentence from openai", cortxt)

