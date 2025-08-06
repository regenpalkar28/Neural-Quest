import os, time
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_huggingface import ChatHuggingFace

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    temperature=0.7,
    max_new_tokens=512,
    huggingfacehub_api_token=hf_token,
)

chat_model = ChatHuggingFace(llm=llm)

print("Welcome! This is an AI-powered QnA App which will help you talk with any historical character.")
character = input("Which character would you like to talk to today? : ")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that excels at adopting historical personas. Your purpose is to act as a historical character and respond to the user's questions in that persona. You must never break character."
    ),
    ("human", "From now on, you are {character}. You will respond to all of my messages as if you are really {character}, with knowledge and tone consistent with their time period. Stay true to their documented beliefs and speech style. Remember, you do not know about any inventions or discoveries made after their time. Do you understand?"
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | chat_model

message_histories = {}

def get_history(session_id: str):
    if session_id not in message_histories:
        message_histories[session_id] = ChatMessageHistory()
    return message_histories[session_id]

conversation = RunnableWithMessageHistory(
    chain,
    get_session_history=get_history,
    input_messages_key="input",
    history_messages_key="history"
)

print(f"\nYou can now talk to {character}. Type 'exit' to quit.")
session_id = "session_1"

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Ending conversation. Goodbye!")
        break

    tic = time.time()

    current_history = get_history(session_id)

    # UNCOMMENT THE BELOW FOR DEBUGGING
    # print("\n--- DEBUG PROMPT ---")
    # formatted_prompt = prompt.format_messages(input=user_input, character=character, history=current_history.messages)
    # for msg in formatted_prompt:
    #     print(f"{msg.type.upper()}: {msg.content}")
    # print("---------------------\n")

    response = conversation.invoke(
        {"input": user_input, "character": character},
        config={"configurable": {"session_id": session_id}}
    )

    print(f"{character}: {response.content.strip()}")
    toc = time.time()
    print(f"(Generated in {round(toc - tic, 2)} s)")
