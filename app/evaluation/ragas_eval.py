"""
RAGAS Evaluation Framework - Production-grade RAG metrics
Uses RAGAS library for standard evaluation metrics
"""

from typing import List, Dict, Any
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
    answer_correctness,
    answer_similarity
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset

from ..state import EvaluationMetrics
from ..config import settings

# ============================================
# INITIALIZE RAGAS COMPONENTS
# ============================================
def get_ragas_llm():
    """Get RAGAS-compatible LLM"""
    if settings.LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=settings.OPENAI_MODEL)
    else:
        from langchain_community.llms import Ollama
        llm = Ollama(model=settings.OLLAMA_MODEL)
    
    return LangchainLLMWrapper(llm)

def get_ragas_embeddings():
    """Get RAGAS-compatible embeddings"""
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.RAGAS_EMBEDDING_MODEL
    )
    return LangchainEmbeddingsWrapper(embeddings)

# ============================================
# EVALUATION FUNCTION
# ============================================
async def evaluate_response(
    question: str,
    answer: str,
    contexts: List[str],
    ground_truth: str = None
) -> EvaluationMetrics:
    """
    Evaluate RAG response using RAGAS metrics
    
    Args:
        question: User's question
        answer: Generated answer
        contexts: Retrieved contexts
        ground_truth: Expected answer (for testing)
    
    Returns:
        EvaluationMetrics with all scores
    """
    
    # Prepare dataset for RAGAS
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts]
    }
    
    if ground_truth:
        data["ground_truth"] = [ground_truth]
    
    dataset = Dataset.from_dict(data)
    
    # Select metrics
    metrics_list = [
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    ]
    
    if ground_truth:
        metrics_list.extend([answer_correctness, answer_similarity])
    
    # Run evaluation
    try:
        result = evaluate(
            dataset=dataset,
            metrics=metrics_list,
            llm=get_ragas_llm(),
            embeddings=get_ragas_embeddings()
        )
        
        # Extract scores
        metrics = EvaluationMetrics(
            faithfulness=result["faithfulness"],
            answer_relevance=result["answer_relevancy"],
            context_recall=result["context_recall"],
            context_precision=result["context_precision"],
            hallucination_score=1 - result["faithfulness"]  # Inverse of faithfulness
        )
        
        if ground_truth:
            metrics.answer_correctness = result.get("answer_correctness", 0)
            metrics.answer_similarity = result.get("answer_similarity", 0)
        
        return metrics
        
    except Exception as e:
        print(f"RAGAS evaluation failed: {e}")
        return EvaluationMetrics()

# ============================================
# TRULENS EVALUATION (Alternative/Observability)
# ============================================
from trulens_eval import TruChain, Feedback, Tru
from trulens_eval.feedback import Groundedness, Relevance

def setup_trulens_tracking(chain):
    """Setup TruLens for production observability"""
    
    tru = Tru()
    tru.reset_database()
    
    # Define feedback functions
    grounded = Groundedness()
    relevance = Relevance()
    
    # Wrap chain with TruLens
    tru_chain = TruChain(
        chain,
        app_id="pharmacy_rag",
        feedbacks=[grounded, relevance]
    )
    
    return tru_chain, tru