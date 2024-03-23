# Import necessary module
import google.generativeai as genai

# Configure and set up model
genai.configure(api_key="ENTER_YOUR_GEMINI_API_KEY")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                               generation_config=generation_config,
                               safety_settings=safety_settings)

convo = model.start_chat(history=[])

def get_time(code_snippet):
    try:
        convo = model.start_chat(history=[])
        convo.send_message(code_snippet + "\nPlease analyze the time complexity of this code snippet.")

        # Extract and print only the time complexity information
        response = convo.last.text
        time_complexity = response.split("O(")[1].split(")")[0]
        print("Time Complexity:", "O(" + time_complexity + ")")

        return "Time Complexity:" + " O(" + time_complexity + ")"

    except Exception as e:
        import traceback
        traceback.print_exc()