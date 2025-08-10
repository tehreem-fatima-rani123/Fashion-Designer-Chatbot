# gemini_model.py (Enhanced)
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI, ModelSettings
from dotenv import load_dotenv
import os
import asyncio
import base64
import mimetypes

load_dotenv()
set_tracing_disabled(disabled=True)

# Get API keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize clients
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Text model
text_model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-r1-0528:free",
    openai_client=external_client
)

# Vision model
vision_model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

# Initialize Agents
designer_agent = Agent(
    name="Designer Agent",
    instructions="You are a fashion design expert. Provide creative outfit suggestions, style advice, and trend analysis. Consider user preferences, body type, and occasion. Be encouraging and helpful.",
    model=text_model,
    model_settings=ModelSettings(temperature=0.85, max_tokens=1024)
)

vision_agent = Agent(
    name="Vision Agent",
    instructions="Analyze fashion images. Describe clothing items, styles, colors, and patterns. Suggest matching outfits, similar styles, or improvements.",
    model=vision_model,
    model_settings=ModelSettings(temperature=0.3, max_tokens=1024)
)

def get_response(prompt: str, context: str = "") -> dict:
    """Get text response from fashion agent with context"""
    async def run_agent():
        full_prompt = f"{context}\n\nUser Question: {prompt}" if context else prompt
        result = await Runner.run(designer_agent, input=full_prompt)
        return result.final_output

    text_output = asyncio.run(run_agent())
    return {"text": text_output}

def get_image_response(image_path: str, prompt: str) -> dict:
    """Analyze image and get fashion insights"""
    async def run_vision_agent():
        # Read and encode image
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/jpeg"
            
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Create message with image
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": f"data:{mime_type};base64,{base64_image}"
                }
            ]
        }
        
        # Run vision agent
        result = await Runner.run(vision_agent, input=message)
        return result.final_output

    text_output = asyncio.run(run_vision_agent())
    return {"text": text_output}