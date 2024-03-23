import torch
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from fuzzywuzzy import fuzz
import re
# Load pre-trained model and tokenizer
model_name = "gpt2-medium"  # You can adjust the model size as needed
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Load the dataset
try:
    with open("algorithm_dataset.json", "r") as file:
        algorithms = json.load(file)    
except Exception as e:
    print("Error in opeaning the file.. ",str(e))  


# Function to check fuzzy string match with minimum accuracy threshold
def fuzzy_match(string1, string2, threshold=80):
    similarity_score = fuzz.token_sort_ratio(string1.lower(), string2.lower())
    return similarity_score >= threshold

def ask_which_algo(algorithm):
    #there send this algorithm and ask yer to press each
    for i in algorithm:
        print(i['name'])
    inp=input("which one? ")
    return int(inp)

def find_code_and_complexity(algorithm_name):
    for algo in algorithms:
        if fuzzy_match(algo["algorithm"], algorithm_name):
            ask_algo=0
            if len(algo["implementations"]) >  1:
                ask_algo=ask_which_algo(algo["implementations"])
               
            code = algo["implementations"][ask_algo]["code"]  # Taking the first implementation for simplicity
            complexity = algo["time_complexity"]
            name=None
            subCode=None
            try:
                if algo["sub_functions"]:
                    name=algo["sub_functions"][ask_algo]['name']
                    subCode=algo["sub_functions"][ask_algo]['code']
            except:
                pass        
            return code, complexity , name ,subCode
    return None, None ,None,None


def generate_response(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, max_length=100, num_return_sequences=1, early_stopping=True)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Function to get user input and return the response
def get_response(user_input):
    code, complexity ,name , subCode= find_code_and_complexity(user_input)
    if code and complexity:
        if(name and subCode):
            string=f"/*{code}\n//Time Complexity:{complexity}\n//{name}\n\n{subCode}*/"
        else:
            string=f"/*{code}\n//Time Complexity:{complexity}\n*/"
        return string
    else:
        return generate_response(f"CODE FOR {user_input}")

# Interactive loop



def get_algorithm(input_text):
    input_text=input_text.lower()
    try:
        algorithm_name =(input_text.split('algorithm'))[1]
    except:
        pass    
    response=None
    print(algorithm_name)
    if algorithm_name:
        response = get_response(algorithm_name)
        print("Bot:", response)
    return response   
