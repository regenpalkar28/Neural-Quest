from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="gemma:2b")

print("Welcome! This is an AI powered QnA App which will help you talk with any historical character")
character = input("Which character will you like to talk to today? : ")
question = input(f"What would you like to ask {character}? : ")
prompt = (f"You are going to adopt the persona of {character}. "
          "You must answer whatever questions I ask you."
          f"Respond in first person as if you are really {character}, with knowledge and tone consistent with {character}'s time period. "
          f"Stay true to {character}'s documented beliefs, speech style, and the scientific understanding available during their lifetime.\n"
          "For example, remember that someone like Copernicus or Leonardo Da Vinci will not be able to know anything about neural networks, but they can tell you a lot about geometry and physics. \n"
          "Avoid any references to inventions or discoveries made after their time. "
          f"Provide answers for this question: '{question}' assuming that you are {character}. "
          )
# print(prompt)
print(llm.invoke(prompt))