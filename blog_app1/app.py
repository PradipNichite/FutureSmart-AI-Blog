import streamlit as st
import openai
from streamlit_chat import message
import pinecone
import os
import pinecone_utils

# We will  pasting our openai credentials over here
openai.api_key = os.getenv("openai_key")

pinecone.init(api_key=os.getenv("pinecone_key"), environment="us-east-1-aws")

index = pinecone.Index("demo-youtube-app")


# openai embeddings method
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )

    return response['data'][0]['embedding']


def find_top_match(query, k):
    query_em = pinecone_utils.get_embedding(query)
    result = index.query(query_em, top_k=k, includeMetadata=True)

    return [result['matches'][i]['metadata']['video_url'] for i in range(k)], [result['matches'][i]['metadata']['title']
                                                                               for i in range(k)], [
               result['matches'][i]['metadata']['context']
               for i in range(k)]


def get_message_history(contexts):
    message_hist = [
        {"role": "system",
         "content": """As a Bot, it's important to show empathy and understanding when answering questions.You are a smart AI who have to answer the question only from the provided context If you 
     are unable to understand the question and need more clarity then your response should be 'Could you please be 
     more specific?'. If you are unable to find the answer from the given context then your response should be 'Answer is not present in the provided video' \n"""},
        {"role": "system", "content": contexts},
    ]

    return message_hist


def chat(var, message, role="user"):
    message_history.append({"role": role, "content": f"{var}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
    )
    reply = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": f"{reply}"})
    return reply


st.title("Youtube Chatbot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["How can I assist you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input(key="input", label="Type your query here")
    return input_text


# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    user_input = get_text()

    if st.session_state.past or user_input:
        urls, title, context = find_top_match(user_input, 1)
        message_history = get_message_history(context[0])

        with st.spinner("Generating the answer..."):
            response = chat(user_input, message_history)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

        st.subheader("References")

        link_expander = st.expander("Context obtained from url")
        link_expander.write(urls)

    # st.session_state.pastModified.append(user_input)

with response_container:
    if st.session_state['generated'] or len(message_history) > 0:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["generated"][i], key=str(i))
            if i < len(st.session_state['past']):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
