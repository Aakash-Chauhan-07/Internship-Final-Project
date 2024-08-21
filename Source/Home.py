import streamlit as st
import time

# Set page config
st.set_page_config(page_title="General Home", layout="centered", page_icon="😊")

# Sidebar for chat management
with st.sidebar:
    st.header("Chat Management")

    # Button to create a new chat instance
    chat_id = st.text_input("Create New Chat: ", max_chars=60)

    if chat_id:
        content = None

        # New chat file for new instance
        with open("chat_template.py", "r") as file:
            content = file.readlines()

        with open(f"pages/{chat_id}.py", "w+") as f:
            f.writelines(content)

        time.sleep(1)  # Wait for file creation

        st.success("New Chat created Successfully")

# Main area
st.header("Welcome to the General - Chat App!")
st.write("Use the sidebar to create or navigate to chat instances.")

st.subheader("Wanna Play with Machine Learning Model.")

# Ensure the selectbox options are properly formatted
option = st.selectbox("Select the Machine Learning Task you want to do.", ("Select the Option" ,
                                                                           "Logistic Regression", 
                                                                           "Artificial Neural Network", 
                                                                           "Sentiment Analysis", "Data Preprocessing",
                                                                            "Google Search",
                                                                            "Crop Face and Paste it on main image",
                                                                            "Custom Image"))

if option == "Logistic Regression":
    from Logistic_reg import Log_reg
    Log_reg()

elif option == "Artificial Neural Network":
    from ANN import Full_ANN
    Full_ANN()

elif option == "Sentiment Analysis":
    from Sentiment_Analysis import sentiment_analysis
    sentiment_analysis()

elif option == "Data Preprocessing":
    from data_preprocessing import preprocess_data
    preprocess_data()

elif option == "Google Search":
    from gsearch import google_search
    google_search()

elif option == "Crop Face and Paste it on main image":
    from crop_face_and_paste import process
    process()

elif option == "Custom Image":
    from custom_image import custom_image
    custom_image()