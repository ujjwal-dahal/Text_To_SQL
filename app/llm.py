from langchain_groq import ChatGroq

# project imports
from app.config import GROQ_API_KEY, GROQ_MODEL_NAME

llm = ChatGroq(model=GROQ_MODEL_NAME, api_key=GROQ_API_KEY, temperature=0)
