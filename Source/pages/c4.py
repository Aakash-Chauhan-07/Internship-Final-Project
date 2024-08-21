import streamlit as st
import google.generativeai as genai
import os
import re
from pymongo import MongoClient
import time

# Streamlit page configuration
st.set_page_config(page_title="General Chat - bot", page_icon=None, layout="centered")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['chat_db']
collection = db['chat_collection']  # Use a single collection for all chat sessions

# Helper function to convert text to dictionary
def convert_to_dict(text):
    # Define regular expressions to match key-value pairs
    pattern = r'"([^"]+)"\s*:\s*"((?:[^"\\]|\\.)*?)"\s*,?'

    # Initialize an empty dictionary to store results
    dictionary = {}

    # Use regular expressions to find and extract key-value pairs
    matches = re.findall(pattern, text)

    for match in matches:
        key = match[0]
        value = match[1].replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        dictionary[key] = value

    return dictionary

# Chat ID initialization
current_chat_id = os.path.basename(__file__)

# Message Initialization
if "messages" not in st.session_state:
    st.session_state.messages = {}

# Retrieve past chat messages from MongoDB
if current_chat_id not in st.session_state.messages:
    chat_history = collection.find_one({"chat_id": current_chat_id})
    if chat_history:
        st.session_state.messages[current_chat_id] = chat_history['messages']
    else:
        st.session_state.messages[current_chat_id] = []

# Display past chat messages
for message in st.session_state.messages[current_chat_id]:
    with st.chat_message(message['role']):
        if message['role'] == 'user':
            st.markdown(message['parts'])
        if message['role'] == "model":
            content = convert_to_dict(message['parts'])
            st.markdown(content['response'])
            if "code" in content.keys():
                try:
                    st.code(content['code'], language=content['code_language'], line_numbers=True)
                except Exception as e:
                    st.code(content['code'], line_numbers=True)

# Configuration outside the function
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
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
    }
]

@st.cache_data
def get_model_config():
    return generation_config, safety_settings

@st.cache_resource
def initialize_convo(chat_id):
    genai.configure(api_key="AIzaSyCZWGizEsHfDbVZFOma9eYrOdJb51ILDOo")

    generation_config, safety_settings = get_model_config()
    content = None
    with open("chat_system_instruction.txt", "r") as f:
        content = f.readlines()

    sys_instruction = ""
    for i in content:
        sys_instruction += i

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction=sys_instruction
    )

    chat_history = st.session_state.messages.get(chat_id, [])
    convo = model.start_chat(history=chat_history)

    return convo

convo = initialize_convo(current_chat_id)

def response_generator(response):
    for word in response['response'].split():
        yield word + " "
        time.sleep(0.02)

    if "code" in response.keys():
        try:
            st.code(response['code'], language=response['code_language'], line_numbers=True)
        except Exception as e:
            st.code(response['code'], line_numbers=True)

# Sidebar for chat management
with st.sidebar:
    st.header("Chat Management")

    chat_id = st.text_input("Create New Chat: ", max_chars=60)
    if chat_id:
        parts = None
        with open(__file__, "r") as file:
            file.seek(0)
            parts = file.readlines()

        with open(f"{chat_id}.py", "w+") as f:
            f.writelines(parts)

        os.system(f"""move "{chat_id}.py" pages""")
        time.sleep(1)
        st.success("New Chat created Successfully")

if prompt := st.chat_input("What is up?"):
    st.session_state.messages[current_chat_id].append({"role": "user", "parts": prompt})
    with st.chat_message("User"):
        st.markdown(prompt)

    with st.chat_message("model"):
        response_original = convo.send_message(prompt)
        response = convert_to_dict(response_original.text)
        st.write_stream(response_generator(response))

        if "operation_status" in response.keys() and response["operation_status"] == "true":
            import json
            for i in range(5):
                try:
                    with open(r"Automation\service.json", "w") as f:
                        json.dump(response, f, indent=4)
                    time.sleep(1)
                    break
                except:
                    pass

    st.session_state.messages[current_chat_id].append({"role": "model", "parts": response_original.text})

    # Save chat history to MongoDB
    collection.update_one(
        {"chat_id": current_chat_id},
        {"$set": {"messages": st.session_state.messages[current_chat_id]}},
        upsert=True
    )
