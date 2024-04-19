## FitGenius-AI: Your AI-Powered Fitness Trainer

**About:**

FitGenius-AI is a project that leverages the power of Google's Generative Pre-trained Transformer (GPT-3) technology, specifically the Gemini-Pro model, to provide you with an interactive fitness trainer experience. It aims to guide you on your fitness journey by offering personalized advice and answering your questions based on your specific goals, health information, and preferences.

**Installation:**

**Prerequisites:**

- Python 3.x (Download from [https://www.python.org/downloads/](https://www.python.org/downloads/))
- Git version control (Download from [https://git-scm.com/downloads](https://git-scm.com/downloads))
- streamlit (Install using `pip install streamlit`)
- Additional libraries specified in the project's `requirements.txt` file (Install using `pip install -r requirements.txt`)

**Steps:**

1. **Clone the Repository:**
   Open a terminal or command prompt and navigate to the directory where you want to clone the repository.
   Run the following command:

   ```bash
   git clone https://github.com/manojkum-d/FitGenuis-ai.git
   ```

2. **Install Dependencies:**
   Navigate to the cloned repository directory:

   ```bash
   cd FitGenuis-ai
   ```

   Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

**Running the Project:**

1. **Set Up Google GenerativeAI API Key:**
   - Create a Google Cloud Project and enable the GenerativeAI API (refer to Google Cloud documentation for details).
   - Obtain an API key and store it securely in a `.env` file (outside of version control) following the instructions in the code (refer to comments or documentation within the codebase).

2. **Start the Streamlit App:**
   - In your terminal within the project directory, run the following command:

   ```bash
   streamlit run main.py
   ```

   - This will launch the FitGenius-AI app in your web browser, typically at `http://localhost:8501`.

**Note:**

- This is a general guide, and the specific instructions might vary slightly depending on your system configuration and the project's setup. Refer to any additional documentation or comments within the codebase for further guidance.
- Remember to replace placeholders like API keys with your actual credentials.
