from services.llm_factory import LLMFactory
from pydantic import BaseModel, Field
import google.generativeai as genai
class TestResponse(BaseModel):
    response: str = Field(description="The response from the LLM")

def test_gemini():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Explain how AI works")
    print(response.text)

if __name__ == "__main__":
    test_gemini()
