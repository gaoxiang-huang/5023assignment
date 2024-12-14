from zhipuai import ZhipuAI
import torch
import numpy as np
import random
from supervise import *
# from tqdm import tqdm

times = 0  # The number of times the chatbot has been called
client = ZhipuAI(api_key="b74e918db339657c60ed90af4da4719d.Yxt3g5DncVfjRNvy")  # Please fill in your own APIKey

def text_generation(prompt):
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

def generate_outline(topic):
    prompt = f"Please as an author, analyze the task of generating a more than 10000 words long text with the topic of: {topic}. Think the story step by step and then list the outline details, including the main sections with the words number of the about 10000 words article."
    outline, times = text_generation(prompt)
    save_file("prompts/outline.txt", outline)
    return outline, times

def generate_long_text(outline):
    sections = outline.split("\n\n")  # Assuming sections are separated by newlines
    long_text = ""
    for section in sections:
        prompt = f"Generate a following words text for the section: {section}"
        section_text, times = text_generation(prompt)
        long_text += f"### {section}\n{section_text}\n\n"
    save_file("prompts/generated_text.txt", long_text)
    return long_text, times

def regenerate_text_with_feedback(outline, feedback):
    """
    Regenerate the text based on the feedback from supervise.py.
    """
    prompt = f"Here is the outline and feedback for improving the text:\n\nOutline:\n{outline}\n\nFeedback:\n{feedback}\n\nPlease regenerate the text based on this feedback."
    long_text, times = text_generation(prompt)
    save_file("prompts/regenerated_text.txt", long_text)
    return long_text, times

# Example usage
topic = "Stepping on the Rainy Street"
outline, times = generate_outline(topic)
print("Outline generated and saved to prompts/outline.txt")

long_text, times = generate_long_text(outline)
print("Long text generated and saved to prompts/generated_text.txt")

outline = load_file("prompts/outline.txt")
text = load_file("prompts/generated_text.txt")

score_outline_response, times = score_outline(outline)
print("Outline score and justification:", score_outline_response)

score_text_response, times = score_text(text)
print("Text score and justification:", score_text_response)

mind_map, times = generate_mind_map(outline)
print("Mind map generated:", mind_map)

questions, times = generate_questions(outline)
print("Generated questions:", questions)

answers, times = answer_questions(questions)
print("Answers to top questions:", answers)

feedback, times = provide_feedback(outline, text)
print("Feedback and suggestions:", feedback)

save_file("prompts/feedback.txt", feedback)



# Load feedback from supervise.py
feedback = load_file("prompts/feedback.txt")

# Regenerate text based on feedback
regenerated_text, times = regenerate_text_with_feedback(outline, feedback)
print("Regenerated text saved to prompts/regenerated_text.txt")

print("API calls:", times)