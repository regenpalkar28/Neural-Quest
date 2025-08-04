import ollama



no_recipes = input("No. of recipes: ")
ingredients = input("List of ingredients: ")
filter_type = input("Filter (e.g., veg, vegan): ")

prompt = (
    f"Show me {no_recipes} recipes using the following ingredients: {ingredients}. "
    f"Each recipe should list all ingredients used. The recipes must be {filter_type}."
)
messages=[{"role": "user", "content": prompt}]

response=ollama.chat(
    model="llama3",
    messages= messages
)


recipes = response['message']['content']
print("\n====== Recipes ======\n")
print(recipes)


shopping_prompt = (
    f"Given these ingredients already at home: {ingredients}, "
    f"and these recipes: {recipes}, "
    f"create a shopping list that excludes ingredients already available."
)
messages=[{"role":"user", "content":shopping_prompt}]

response2= ollama.chat(
    model="llama3",
    messages=messages
)

print("\n====== Shopping List ======\n")
print(response2['message']['content'])