import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are my blog genertor. You are required to create a blog on that topic{question}"),
        ("user", "Question:{question}")
    ]
)

# Initialize the model and output parser
model = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# Chain the prompt, model, and output parser
chain = prompt | model | output_parser

# Streamlit interface
st.title("LangChain OpenAI Streamlit App")

question = st.text_input("Enter your topic:")

if st.button("Generate blog..."):
    if not question:
        st.write("Please provide your topic.")
    else:
        result = chain.invoke({"question": question})
        st.write("Blog:")
        st.write(result)

