from langchain_community.llms import Ollama

llm = Ollama(model="gemma:2b")

print("Hey, welcome to this recipe generator, We will help you create the perfect dish based on your preferences and what materials you have available.")
cuisine = input("Do you wish to have a recipe from a particular cuisine? (such as Indian, Chinese, Italian etc) : ")
ingredients = input("What ingredients do you have available? (such as chicken, potatoes, etc): ")
filt = input("Do you wish to apply any filters? (such as vegetarian, vegan, gluten free, or any allergies): ")

prompt = f"Show me a recipes for a dish in the cuisine {cuisine} with the following ingredients: {ingredients}. List all the ingredients used in the recipe, the recipe should adhere to the following filter {filt} : "

recipe = llm.invoke(prompt)
print(recipe)