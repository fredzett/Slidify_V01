import openai 
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """
Santa Clause riding on a horse on fifth avenue. In the style of an icon. 
"""

response = openai.Image.create(
  prompt=prompt,
  n=1,
  size="1024x1024",
)
image_url = response['data'][0]['url']
print(image_url)