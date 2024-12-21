import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from enum import Enum
from typing import List
from services.llm_factory import LLMFactory
import google.generativeai as genai
from config.settings import get_settings

settings = get_settings()

# Configure Gemini client
genai.configure(api_key=settings.gemini.api_key)
client =instructor.from_gemini(
                genai.GenerativeModel(model_name="gemini-1.5-flash-latest"),
                mode=instructor.Mode.GEMINI_JSON,
            )

# Sample customer support tickets
ticket1 = """
I ordered a laptop from your store last week (Order #12345), but I received a tablet instead. 
This is unacceptable! I need the laptop for work urgently. Please resolve this immediately or I'll have to dispute the charge.
"""

ticket2 = """
Hello, I'm having trouble logging into my account. I've tried resetting my password, but I'm not receiving the reset email. 
Can you please help me regain access to my account? I've been a loyal customer for years and have several pending orders.
"""
# --------------------------------------------------------------
# Objective
# --------------------------------------------------------------

"""
Objective: Develop an AI-powered ticket classification system that:
- Accurately categorizes customer support tickets
- Assesses the urgency and sentiment of each ticket
- Extracts key information for quick resolution
- Provides confidence scores to flag uncertain cases for human review
Business impact:
- Reduce average response time by routing tickets to the right department
- Improve customer satisfaction by prioritizing urgent and negative sentiment tickets
- Increase efficiency by providing agents with key information upfront
- Optimize workforce allocation by automating routine classifications
"""

# --------------------------------------------------------------
# Pydantic data models
# --------------------------------------------------------------

"""
This code defines a structured data model for classifying customer support tickets using Pydantic and Python's Enum class. 
It specifies categories, urgency levels, customer sentiments, and other relevant information as predefined options or constrained fields. 
This structure ensures data consistency, enables automatic validation, and facilitates easy integration with AI models and other parts of a support ticket system.
"""

class TicketCategory(str, Enum):
    ORDER_ISSUE = "order_issue"
    ACCOUNT_ACCESS = "account_access"
    PRODUCT_INQUIRY = "product_inquiry"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING = "billing"
    OTHER = "other"

class CustomerSentiment(str, Enum):
    ANGRY = "angry"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    SATISFIED = "satisfied"

class TicketUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketClassification(BaseModel):
    category: TicketCategory
    urgency: TicketUrgency
    sentiment: CustomerSentiment
    confidence: float = Field(ge=0, le=1, description="Confidence score for the classification")
    key_information: List[str] = Field(description="List of key points extracted from the ticket")
    suggested_action: str = Field(description="Brief suggestion for handling the ticket")
    
    
ticket_classification = TicketClassification(
    category=TicketCategory.ORDER_ISSUE,
    urgency=TicketUrgency.HIGH,
    sentiment=CustomerSentiment.ANGRY,
    confidence=0.9,
    key_information=["Order #12345", "Received tablet instead of laptop"],
    suggested_action="Contact customer to arrange laptop delivery"
)

def classify_ticket(ticket_text: str) -> TicketClassification:    
    response = client.chat.completions.create(
        response_model=TicketClassification,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": "Analyze the following customer support ticket and extract the requested information."
            },
            {"role": "user", "content": ticket_text}
        ]
    )
    return response

result1 = classify_ticket(ticket1)
result2 = classify_ticket(ticket2)

print(result1.model_dump_json(indent=2))
print(result2.model_dump_json(indent=2))


# --------------------------------------------------------------
# Optimize your prompts and experiment
# --------------------------------------------------------------
# To optimize:
# 1. Refine the system message to provide more context about your business
# 2. Experiment with different models (e.g., gpt-3.5-turbo vs gpt-4)
# 3. Fine-tune the model on your specific ticket data if available
# 4. Adjust the TicketClassification model based on business needs

SYSTEM_PROMPT = """
You are an AI assistant for a large e-commerce platform's customer support team. 
Your role is to analyze incoming customer support tickets and provide structured information to help our team respond quickly and effectively.
Business Context:
- We handle thousands of tickets daily across various categories (orders, accounts, products, technical issues, billing).
- Quick and accurate classification is crucial for customer satisfaction and operational efficiency.
- We prioritize based on urgency and customer sentiment.
Your tasks:
1. Categorize the ticket into the most appropriate category.
2. Assess the urgency of the issue (low, medium, high, critical).
3. Determine the customer's sentiment.
4. Extract key information that would be helpful for our support team.
5. Suggest an initial action for handling the ticket.
6. Provide a confidence score for your classification.
Remember:
- Be objective and base your analysis solely on the information provided in the ticket.
- If you're unsure about any aspect, reflect that in your confidence score.
- For 'key_information', extract specific details like order numbers, product names, or account issues.
- The 'suggested_action' should be a brief, actionable step for our support team.
Analyze the following customer support ticket and provide the requested information in the specified format.
"""

def classify_ticket(ticket_text: str) -> TicketClassification:
    response = client.chat.completions.create(
        response_model=TicketClassification,
        temperature=0,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {"role": "user", "content": ticket_text}
        ]
    )
    return response

result1 = classify_ticket(ticket1)
result2 = classify_ticket(ticket2)

print(result1.model_dump_json(indent=2))
print(result2.model_dump_json(indent=2))