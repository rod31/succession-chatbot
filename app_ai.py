import streamlit as st
import re
import random
import time
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai, os

# set your key
openai.api_key = st.secrets["OPENAI_API_KEY"] or os.getenv("OPENAI_API_KEY")

# instantiate the new client
client = openai.OpenAI()

# ─ your existing data & helpers ─
@st.cache_data
def load_character(character):
    character_str = character.lower()
    df = pd.read_csv(f'{character_str}_roy_sarcasm_labels.csv')

    return df['text'].dropna().tolist()


STOPWORDS = {
    "the","and","is","in","on","at","of","a","an","to","for","with","that","this",
    "i","you","your","we","they","he","she","it","do","does","did","will","can","could",
    "should","would","what","why","how","when","where","me","my","myself","yourself",
    "so", "am",
    "are", "were", "was"
}


def extract_keywords(text):
    return [
        w for w in re.findall(r"\b\w+\b", text.lower())
        if w not in STOPWORDS
    ]

def choose_response(question, pool):
    words = extract_keywords(question)
    # build a list of matching indices
    indices = []
    for word in words:
        for i, resp in enumerate(pool):
            tokens = re.findall(r"\b\w+\b", resp.lower())
            if word in tokens:
                indices.append(i)
    if indices:
        return pool[random.choice(indices)]
    return random.choice(pool)

# Roy Family Options
roy_names =[
    "Roman",
    "Shiv", 
    "Kendall", 
    "Logan"
]

# LLM
@st.cache_resource
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')


def create_index(dialogues):
    embeddings = model.encode(dialogues)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

def get_top_quotes(user_query, dialogue_list, faiss_index, model, k=3):
    query_vec = model.encode([user_query])
    _, indices = faiss_index.search(np.array(query_vec), k)
    return [dialogue_list[i] for i in indices[0]]

def gpt_reply(character, quotes, user_input):
    system_prompt = f"You are {character} Roy from Succession. Answer like them and include your name in the response (e.g. Roman Roy). Don't be afraid to curse. Here are some quotes to guide your tone:\n" + "\n".join(quotes)
    user_prompt = f"The user said: '{user_input}'\nRespond as {character} Roy."
    
    # is this block supposed to be here?
    history_msgs = [{"role": r, "content": c} for r,c in st.session_state.history]
    messages = (
    [{"role":"system", "content": system_prompt}] +
    history_msgs +
    [{"role":"user",   "content": user_prompt}]
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # GPT-4.1 Mini
        messages=messages,
        temperature=0.9,
    )
    return response.choices[0].message.content

@st.cache_resource
def get_faiss_index(character):
    responses = load_character(character)
    index, embeddings = create_index(responses)
    return index, embeddings, responses



# Streamlit UI

# UI Layout
st.title("Succesion Chatbot")
st.header("💬 Chat with the Roy family")
# st.subheader("💬 Chat with the Roy family")
st.logo("succession_logo.jpg")
st.set_page_config(
    page_title="Chat with the Roys",
    page_icon="🧑‍💼",            # you can also point to a local .png
    layout="wide"
)
st.image("./succession_bg.jpg")

st.markdown("Ask anything, and get a Roy‐style reply!")
character_option = st.sidebar.selectbox(
    'Which Roy do you wanna talk to?',
    roy_names
)

chat_option = st.selectbox(
    'Chat Mode',
    ['Smart Reply','Roy Parrot']
)

RESPONSES = load_character(character_option)
# Session State Setup
# If the user just picked a *new* Roy, reset the conversation
if st.session_state.get("character") != character_option:
    # each entry is a tuple: (role, message)
    st.session_state.character = character_option
    st.session_state.history = [("assistant", f"**{character_option} Roy:** {RESPONSES[0]}")] # "Hey hey hey, motherfuckers!"
#
if st.session_state.get("mode") != chat_option:
    st.session_state.mode = chat_option
    st.session_state.history = [("assistant", f"**{character_option} Roy:** {RESPONSES[0]}")]
question = st.chat_input("What do you want?")

# SMART REPLY block
model = load_embedder()

if chat_option == 'Smart Reply':
    st.write(f"You are talking to **{character_option} Roy** (Smart Mode).")

    if question: 
        for role, msg in st.session_state.history:
            st.chat_message(role).write(msg)
        st.chat_message("user").write(question)

        with st.spinner(f"🤖 {character_option}'s thinking..."):
            faiss_index, embeddings, responses = get_faiss_index(character_option)
            top_quotes = get_top_quotes(question, responses, faiss_index, model)
            answer = gpt_reply(character_option, top_quotes, question)

        st.chat_message("assistant").write(f"{answer}")
        st.session_state.history.append(("user", question))
        st.session_state.history.append(("assistant", f"{answer}"))
    else:
        for role, msg in st.session_state.history:
            if role == "assistant":
                st.chat_message(role).write(f"{msg}")
            else:
                st.chat_message(role).write(msg)

# ROY PARROT BLOCK
else:
    st.write(f"You are talking to **{character_option} Roy** (Keyword Parrot Mode).")

    if question:
        for role, msg in st.session_state.history:
            st.chat_message(role).write(msg)
        st.chat_message("user").write(question)

        with st.spinner("🤔…"):
            # simulate little delay
            time.sleep(random.uniform(0.5,1.6))
            answer = choose_response(question, RESPONSES)

        st.chat_message("assistant").write(f"**{character_option} Roy:** {answer}")
        # append both user and assistant turns to history
        st.session_state.history.append(("user", question))
        st.session_state.history.append(("assistant", f"**{character_option} Roy:** {answer}"))
    else:
        # Show entire chat history
        for role, msg in st.session_state.history:
            if role == "assistant":
                st.chat_message(role).write(f"**{character_option} Roy:** {msg}")
            else:
                st.chat_message(role).write(msg)

