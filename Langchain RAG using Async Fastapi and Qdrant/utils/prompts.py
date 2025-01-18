from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from services.logger import logger

def get_main_prompt():
    prompt = """ 
    "You are an assistant for question-answering tasks."
    "Use the following pieces of retrieved context and user information to answer the question."
    "If you don't find the answer of the query,then just say I don't have that information at hand. Please provide more details or check your sources."
    """

    prompt=prompt + "\n\n" + "{context}"
    
    final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        MessagesPlaceholder (variable_name="messages"),
        ("human", "{user_query}")
    ])
    return final_prompt


def get_query_refiner_prompt():
    contextualize_q_system_prompt = ("""
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as it is."
    """)

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("human","{query}"),
        ]
    )
    # print(final_prompt)
    return final_prompt