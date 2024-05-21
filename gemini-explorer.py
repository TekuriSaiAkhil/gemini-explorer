import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'gemini-explorer-423922'

vertexai.init(project = project)

config = generative_models.GenerationConfig(temperature = 0.4)

model = GenerativeModel("gemini-pro", generation_config = config)

chat = model.start_chat()


#helper func to disp and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )


st.title("Gemini Explorer")

# init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display and store chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )

    if index!=0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    chat.history.append(content)

# intial prompt to personalize the interactions
if len(st.session_state.messages) == 0:
    initial_prompt = '''Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive. Speak as a harry potter. 
                        you are assisting a user whose name is akhil and have personalized greeting while interacting'''
    llm_function(chat, initial_prompt)

# get user input
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)