from fastapi import FastAPI, UploadFile, File
from anthropic import Anthropic
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.get("/")
def root():
    return {"status": "swagAi API is running"}

@app.post("/analyze-style")
async def analyze_style(files: list[UploadFile] = File(...)):
    
    image_content = []
    for file in files:
        image_data = base64.b64encode(await file.read()).decode("utf-8")
        image_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": file.content_type,
                "data": image_data
            }
        })
    
    image_content.append({
        "type": "text",
        "text": """Analyze these outfit images and return a JSON style profile with:
        - colors: main colors present
        - garments: types of clothing items
        - aesthetic: overall vibe/era (e.g. Y2K, dark academia, streetwear)
        - brands: any visible or matching brands
        - search_queries: 5 search terms to find similar items on Depop or Vinted
        Return only a raw valid JSON object. No markdown, no backticks, no extra text. Just the JSON."""
    })

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": image_content}]
    )

    return {"style_profile": response.content[0].text}
