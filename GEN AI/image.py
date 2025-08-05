from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Example image generation call (DALL·E)
response = client.images.generate(
    model="dall-e-3",
    prompt="a futuristic city skyline at sunset",
    size="1024x1024",
    quality="standard",
    n=1,
)

# Print the image URL
print(response.data[0].url)
