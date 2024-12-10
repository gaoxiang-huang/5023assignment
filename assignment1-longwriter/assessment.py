from zhipuai import ZhipuAI
import torch
import numpy as np
import random
from supervise import *
# from tqdm import tqdm

times = 0  # The number of times the chatbot has been called
client = ZhipuAI(api_key="b74e918db339657c60ed90af4da4719d.Yxt3g5DncVfjRNvy")  # Please fill in your own APIKey

def assess_generation(prompt):
    global times
    response = client.chat.completions.create(
        model="glm-4-flash", 
        messages=[
            {
                "role": "user", 
                "content": prompt
             },
        ],
    )
    times += 1
    return response.choices[0].message.content, times

material= load_file("prompts/generated_text.txt")
criteria = load_file("prompts/criteria.txt")
response = criteria.replace("[TEXT]", material)
score = assess_generation(response)
save_file("score.txt", str(score))
