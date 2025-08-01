from langchain_community.llms import Ollama

llm = Ollama(model="gemma:2b")

text = input("Type a sentence that you want to finish: ")

prompt = f"Complete the following : {text}"

output = llm.invoke(prompt)
print(output)