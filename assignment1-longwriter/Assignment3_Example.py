from zhipuai import ZhipuAI

times = 0 # The number of times the chatbot has been called
client = ZhipuAI(api_key="b74e918db339657c60ed90af4da4719d.Yxt3g5DncVfjRNvy")  # Please fill in your own APIKey

def text_generation(prompt, times):
    inquery = ("Please analyze the problem below in steps of retriving, association, plan, output"),
    retriving = ("Extract the main elements in text including role, action, object in one side. And extract the sub elements in text including feature, time, location"),
    association = ("Initially, considerating the background in sub elements like the era and society by the feature, time, location. Further, interpret the role of main elements respectively in the background"),
    plan = ("reflect the problem self, get the question before problem, score the questiones and filter the first 3 question in scores. Disscuse the questiones by module association in past, present and future. And then summarize it to be insight"),
    output = ("Utilize insight to reply the problem summitted by user"),
    full_prompt = inquery, prompt, retriving, association, plan, output
    response = client.chat.completions.create(
        model="glm-4-flash", 
        messages=[
            {
                "role": "user", 
                "content": f"{inquery}\n{prompt}\n{retriving}\n{association}\n{plan}\n{output}"
             },
        ],
    )
    times += 1
    return response.choices[0].message, times

############################################################################################################
# The following functions are for you to implement
# You can implement functions for saving and loading files, and planning
# You can also implement functions for the chatbot to interact with the user
############################################################################################################

def savig_files(results):
    # to save to generated_text.txt
    with open("assignment1-longwriter/file/50005050.txt", "w") as f:
        f.write(results)

def load_files():
    pass

def planning():
    pass

def others():
    pass

# Simple example

results, times = text_generation("generating a long text with the topic of: AI and the future of human beings", times)
results, times = text_generation("polish the text，" + results.content, times)

print(results.content)
savig_files(results.content)

############################################################################################################

print("API calls:", times)
