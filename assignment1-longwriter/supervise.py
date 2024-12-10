from zhipuai import ZhipuAI
import torch
import numpy as np
import random

times = 0  # The number of times the chatbot has been called
client = ZhipuAI(api_key="b74e918db339657c60ed90af4da4719d.Yxt3g5DncVfjRNvy")  # Please fill in your own APIKey

def supervise_generation(prompt):
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

def save_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def load_file(filename):
    with open(filename, "r") as f:
        return f.read()
    
def score_outline(outline):
    prompt = f"Please score the following outline on a scale of 1 to 10, where 1 is poor and 10 is excellent. Provide a brief justification for your score:\n\n{outline}"
    score_response, times = supervise_generation(prompt)
    return score_response, times

def score_text(text):
    prompt = f"Please score the following text on a scale of 1 to 10, where 1 is poor and 10 is excellent. Provide a brief justification for your score:\n\n{text}"
    score_response, times = supervise_generation(prompt)
    return score_response, times

def generate_mind_map(outline):
    prompt = f"Please generate a mind map or a structured outline based on the following outline:\n\n{outline}"
    mind_map, times = supervise_generation(prompt)
    return mind_map, times

def generate_questions(outline):
    prompt = f"Please generate a list of questions based on the following outline. Rank them by importance:\n\n{outline}"
    questions, times = supervise_generation(prompt)
    return questions, times

def answer_questions(questions):
    top_questions = "\n".join(questions.split("\n")[:3])  # Assuming questions are separated by newlines
    prompt = f"Please answer the following questions:\n\n{top_questions}"
    answers, times = supervise_generation(prompt)
    return answers, times

def provide_feedback(outline, text):
    prompt = f"Please provide feedback and suggestions for improving the following outline and text:\n\nOutline:\n{outline}\n\nText:\n{text}"
    feedback, times = supervise_generation(prompt)
    return feedback, times