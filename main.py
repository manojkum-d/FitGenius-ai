import streamlit as st
from Audio import text_to_speech, get_audio
import cv2
import tempfile
import ExerciseAiTrainer as exercise
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
    print(gender, age, weight, height, activity_level, goals, dietary_restrictions, bp, sugar, food_allergy)
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

    # Define sidebar options for selecting functionality
    # options = st.sidebar.radio('Select Functionality', ('AI Assistant', 'Personal Trainer', 'Gemini Health App'))
    options = st.sidebar.radio('Select Functionality', ('AI Assistant ChatBot' ,'Personal Trainer', 'Ai vision for dietory'))

    with st.sidebar:
        if options != 'Personal Trainer':
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

        # Button to start conversation
        start_conversation = st.button("Start Conversation")

        if start_conversation or st.session_state.button_pressed:
            st.session_state.button_pressed = True
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            if prompt := st.chat_input("What is up?"):
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                # Add user message to chat history
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

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                if type(response) == str:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    elif options == 'Personal Trainer':
        st.write("""
            ## This Feature is not in the deployed version....
            """)

        # # Define Options for selecting video or webcam
        # options = st.sidebar.selectbox('Select Option', ('Video', 'WebCam'))

        # # Define Operations if Video Option is selected
        # if options == 'Video':

        #     st.write('## Import your video and select the correct type of Exercise')

        #     st.set_option('deprecation.showfileUploaderEncoding', False)

        #     # User can select different types of exercise
        #     exercise_options = st.sidebar.selectbox(
        #         'Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press')
        #     )

        #     st.sidebar.markdown('-------')

        #     # User can upload a video:
        #     video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])
        #     tfflie = tempfile.NamedTemporaryFile(delete=False)

        #     # if no video uploaded then use a demo
        #     if not video_file_buffer:
        #         DEMO_VIDEO = 'demo.mp4'
        #         cap = cv2.VideoCapture(DEMO_VIDEO)
        #         tfflie.name = DEMO_VIDEO

        #     # if video is uploaded then analyze the video
        #     else:
        #         tfflie.write(video_file_buffer.read())
        #         cap = cv2.VideoCapture(tfflie.name)

        #     # Visualize Video before analysis
        #     st.sidebar.text('Input Video')
        #     st.sidebar.video(tfflie.name)

        #     st.markdown('## Input Video')
        #     st.video(tfflie.name)

        #     # Visualize Video after analysis (analysis based on the selected exercise)
        #     st.markdown(' ## Output Video')
        #     if exercise_options == 'Bicept Curl':
        #         exer = exercise.Exercise()
        #         exer.bicept_curl(cap)

        #     elif exercise_options == 'Push Up':
        #         exer = exercise.Exercise()
        #         exer.push_up(cap)

        #     elif exercise_options == 'Squat':
        #         exer = exercise.Exercise()
        #         exer.squat(cap)

        #     elif exercise_options == 'Shoulder Press':
        #         exer = exercise.Exercise()
        #         exer.shoulder_press(cap)

        # # Define Operation if webcam option is selected
        # elif options == 'WebCam':

        #     # User can select different exercises
        #     exercise_general = st.sidebar.selectbox(
        #         'Select Exercise', ('Bicept Curl', 'Push Up', 'Squat', 'Shoulder Press')
        #     )

        #     # Define a button for start the analysis (pose estimation) on the webcam
        #     st.write(' ## Click button to activate AI Trainer')
        #     st.write("Say 'Ready' to get started")
        #     button = st.button('Activate AI Trainer')

        #     # Visualize video that explains the correct forms for the exercises
        #     if exercise_general == 'Bicept Curl':
        #         st.write('## Bicept Curl Execution')
        #         st.video('curl_form.mp4')

        #     elif exercise_general == 'Push Up':
        #         st.write('## Push Up Execution')
        #         st.video('push_up_form.mp4')

        #     elif exercise_general == 'Squat':
        #         st.write('## Squat Execution')
        #         st.video('squat_form.mp4')

        #     elif exercise_general == 'Shoulder Press':
        #         st.write('## Shoulder Press Execution')
        #         st.video('shoulder_press_form.mp4')

        #     # if the button is selected, after a Vocal command, start the webcam analysis (pose estimation)
        #     if button:
        #         # Ask user if want to start the training (using text to speech)
        #         text_to_speech('Are you Ready to start Training?')
        #         # get the audio of the user
        #         text = get_audio()

        #         # if user is ready (say 'yes' or 'ready') then start the webcam analysis
        #         if 'ready' or 'yes' in text:

        #             text_to_speech("Ok, Let's get started")
        #             st.write(str('READY'))
        #             ready = True

        #             # for each type of exercise call the method that analyzes that exercise
        #             if exercise_general == 'Bicept Curl':
        #                 while ready:
        #                     cap = cv2.VideoCapture(0)
        #                     exer = exercise.Exercise()
        #                     exer.bicept_curl(cap)

        #             elif exercise_general == 'Push Up':
        #                 while ready:
        #                     cap = cv2.VideoCapture(0)
        #                     exer = exercise.Exercise()
        #                     exer.push_up(cap)

        #             elif exercise_general == 'Squat':
        #                 while ready:
        #                     cap = cv2.VideoCapture(0)
        #                     exer = exercise.Exercise()
        #                     exer.squat(cap)

        #             elif exercise_general == 'Shoulder Press':
        #                 while ready:
        #                     cap = cv2.VideoCapture(0)
        #                     exer = exercise.Exercise()
        #                     exer.shoulder_press(cap)

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
