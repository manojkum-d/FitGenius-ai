import streamlit as st
import cv2
import tempfile
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question, gender, age, weight, height, activity_level, goals, dietary_restrictions, bp, sugar, food_allergy):
    text = f'Act as a fitness trainer and give a short but to the point answer according to the given information that I am {age} years old {gender}, my weight is {weight} kg, my height is {height}cm, i am {activity_level}, my goal is to {goals}, and i am {dietary_restrictions}. My blood pressure is {bp}, my sugar level is {sugar}, and I have food allergies: {food_allergy}. My question is that {question}'
    response = chat.send_message(text, stream=True)
    return response

def get_gemini_health_response(input, image, gender, age, weight, height, activity_level, goals, dietary_restrictions, bp, sugar, food_allergy):
    input_prompt = f"""
    IMPORTANT: Please ensure that the uploaded image contains ONLY food items. Any non-food items in the image will lead to inaccurate results.
    If you are confident that the image contains solely food items: 
    As a nutritionist, your task is to meticulously analyze the food items from the image and calculate their total calories. Additionally, provide the details of every food item with its corresponding calorie intake in the following format:
    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    Pay careful attention to the following information provided:
    - Age: {age} years old
    - Gender: {gender}
    - Weight: {weight} kg
    - Height: {height} cm
    - Activity Level: {activity_level}
    - Goal: {goals}
    - Dietary Restrictions: {', '.join(dietary_restrictions)}
    - Blood Pressure: {bp}
    - Sugar Level: {sugar}
    - Food Allergies: {food_allergy}
    It is essential to strictly follow these guidelines for accurate analysis. Failure to do so may result in incorrect conclusions. Take into account all provided information, particularly blood pressure, sugar levels, and food allergies, to determine whether the individual can safely consume the identified food items.
    STRICT ADHERENCE TO THE INSTRUCTIONS IS REQUIRED.    
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], input_prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    st.title('Your AI Personal Trainer')
    st.write("""
        ## Welcome to your personal AI trainer
        """)

    options = st.sidebar.radio('Select Functionality', ('AI Assistant ChatBot' ,'Ai vision for dietory'))

    with st.sidebar:
        if options != 'Ai vision for dietory':
            gender = st.selectbox("Gender", ["male", "female"])
            age = st.number_input("Age", min_value=0, max_value=150, value=30)
            weight = st.number_input("Weight (kg)", min_value=0.0, step=1.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=0.0, step=1.0, value=170.0)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
            goals = st.radio("Goals", ["Loss Weight", "Maintain Weight", "Gain Weight"])
            dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"])
            bp = st.number_input("Blood Pressure", min_value=60, max_value=300, value=120)
            sugar = st.number_input("Sugar Level", min_value=0, max_value=500, value=80)
            food_allergy = st.text_input("Food Allergy", "")

    if options == 'AI Assistant ChatBot':
        st.write("""
            ## Fitness AI ChatBot
            """)

        st.write("Ask me anything about Fitness")

        if 'button_pressed' not in st.session_state:
            st.session_state.button_pressed = False

        start_conversation = st.button("Start Conversation")

        if start_conversation or st.session_state.button_pressed:
            st.session_state.button_pressed = True
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            if prompt := st.chat_input("What is up?"):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
            if prompt is None:
                response = 'Ask me anything about Fitness'
            else:
                with st.spinner('Typing...'):
                    re = get_gemini_response(str(prompt), gender, age, weight, height, activity_level, goals, dietary_restrictions, bp, sugar, food_allergy)
                    response = ''
                    for chunk in re:
                        for ch in chunk.text.split(' '):
                            response += ch + ' '

            with st.chat_message("assistant"):
                if type(response) == str:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})


    elif options == 'Ai vision for dietory':
        st.header("Gemini Health App")
        input = st.text_input("Input Prompt: ", key="input")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image = ""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)

        submit = st.button("Tell me the total calories")

        if submit:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_health_response(input, image_data, gender, age, weight, height, activity_level, goals, dietary_restrictions, bp, sugar, food_allergy)
            st.subheader("The Response is")
            st.write(response)


if __name__ == '__main__':
    main()
