import streamlit as st
from openai import OpenAI
import base64


# Background image
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        img_bytes = img_file.read()
    b64_img = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{b64_img}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .overlay {{
            background-color: rgba(0, 0, 0, 0.6);
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            z-index: -1;
        }}
        .hero {{
            color: black;
            text-align: center;
            padding: 10% 5%;
        }}
        .hero h1 {{
            font-size: 4em;
            font-weight: bold;
        }}
        .hero p {{
            font-size: 1.5em;
        }}
        .btn {{
            background-color: #0d6efd;
            color: white;
            padding: 12px 24px;
            font-size: 1.1em;
            border: none;
            border-radius: 8px;
            margin-top: 20px;
            text-decoration: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background image
set_background("static/background.jpg")  # Replace with your own image

# HTML Hero Section
st.markdown(
    """
    <div class="overlay"></div>
    <div class="hero">
        <h1>Welcome to AI Doc Analyzer</h1>
        <p>Understand contracts instantly. Powered by AI.</p>
        <a href="#start" class="btn">Get Started</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Placeholder section for more content
st.markdown("""<div id="start"></div>""", unsafe_allow_html=True)
st.markdown("## Upload Your Contract")

# Streamlit Page Configuration
# st.set_page_config(
#     page_title="DocAgent AI NEW",
#     page_icon="static/logo.png",
#     layout="wide",
#     initial_sidebar_state="auto",
#     menu_items={
#         "Get help": "https://streamlit.io/",
#         "Report a bug": "https://streamlit.io/",
#         "About": """
#             ## Streamly Streamlit Assistant
#         """
#     }
# )

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)


st.sidebar.markdown("---")

# Sidebar for Mode Selection
mode = st.sidebar.radio("Select Mode:", options=["DocsAnalyzer", "WeatherCheck"], index=1)

st.sidebar.markdown("---")

# Display basic interactions
show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
if show_basic_info:
    st.sidebar.markdown("""
    ### Basic Interactions
    - **Ask About Streamlit**: Type your questions about Streamlit's latest updates, features, or issues.
    - **Search for Code**: Use keywords like 'code example', 'syntax', or 'how-to' to get relevant code snippets.
    - **Navigate Updates**: Switch to 'Updates' mode to browse the latest Streamlit updates in detail.
    """)

# Display advanced interactions
show_advanced_info = st.sidebar.checkbox("Show Advanced Interactions", value=False)
if show_advanced_info:
    st.sidebar.markdown("""
    ### Advanced Interactions
    - **Generate an App**: Use keywords like **generate app**, **create app** to get a basic Streamlit app code.
    - **Code Explanation**: Ask for **code explanation**, **walk me through the code** to understand the underlying logic of Streamlit code snippets.
    - **Project Analysis**: Use **analyze my project**, **technical feedback** to get insights and recommendations on your current Streamlit project.
    - **Debug Assistance**: Use **debug this**, **fix this error** to get help with troubleshooting issues in your Streamlit app.
    """)

st.sidebar.markdown("---")