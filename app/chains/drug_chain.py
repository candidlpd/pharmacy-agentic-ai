"""
Drug Information Chain - LangChain chain for drug knowledge retrieval
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama

from ..config import settings

# ============================================
# PROMPT TEMPLATE (Prompt Engineering)
# ============================================
DRUG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a clinical pharmacist specializing in drug information.
    
    RULES:
    1. Only use information from the provided context
    2. Always cite your sources
    3. Include warnings and contraindications
    4. Do not provide off-label recommendations
    
    Return JSON format:
    {{
        "answer": "detailed answer",
        "citations": ["source1", "source2"],
        "warnings": ["warning1"],
        "confidence": 0.95
    }}
    """),
    ("human", """
    Drug: {drug}
    Indication: {indication}
    
    Context from reliable sources:
    {context}
    
    Question: What is the standard dosing and safety profile for {drug}?
    """)
])

# ============================================
# CREATE THE CHAIN
# ============================================
def create_drug_chain():
    """Create the LangChain chain for drug information"""
    
    # Initialize LLM (local or cloud)
    if settings.LLM_PROVIDER == "ollama":
        llm = Ollama(model=settings.OLLAMA_MODEL, temperature=settings.TEMPERATURE)
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=settings.TEMPERATURE)
    
    # Create the chain
    drug_chain = (
        DRUG_PROMPT 
        | llm 
        | JsonOutputParser()
    )
    
    return drug_chain

# Global chain instance
drug_chain = create_drug_chain()