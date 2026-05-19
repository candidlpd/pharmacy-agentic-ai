"""
Retrieval Tool - LangChain tool for document retrieval
Uses FAISS vector store with sentence transformers
"""

from typing import Type, List, Dict, Any
from langchain_core.tools import BaseTool
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pydantic import BaseModel, Field
import pickle

from ..config import settings

# ============================================
# TOOL INPUT SCHEMA
# ============================================
class RetrievalInput(BaseModel):
    """Input schema for retrieval tool"""
    query: str = Field(description="The search query")
    k: int = Field(default=5, description="Number of documents to retrieve")

# ============================================
# RETRIEVAL TOOL (LangChain BaseTool)
# ============================================
class PharmacyRetrievalTool(BaseTool):
    """LangChain tool for retrieving pharmacy documents"""
    
    name: str = "pharmacy_retrieval"
    description: str = "Retrieves relevant pharmacy documents, drug labels, and policies"
    args_schema: Type[BaseModel] = RetrievalInput
    
    vector_store: FAISS = None
    embeddings: Embeddings = None
    
    def __init__(self):
        super().__init__()
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize FAISS vector store"""
        try:
            # Load or create embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Load existing FAISS index if available
            index_path = settings.VECTOR_STORE_PATH / "faiss_index"
            if index_path.exists():
                self.vector_store = FAISS.load_local(
                    str(index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
        except Exception as e:
            print(f"Warning: Could not load vector store: {e}")
            self.vector_store = None
    
    def _run(self, query: str, k: int = 5) -> Dict[str, Any]:
        """
        Synchronous run method
        """
        if not self.vector_store:
            return {
                "documents": [],
                "error": "Vector store not initialized"
            }
        
        # Perform similarity search
        docs = self.vector_store.similarity_search(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                "text": doc.page_content,
                "metadata": doc.metadata,
                "score": getattr(doc, "score", 1.0)
            })
        
        return {"documents": results}
    
    async def _arun(self, query: str, k: int = 5) -> Dict[str, Any]:
        """Asynchronous run method"""
        return self._run(query, k)

# ============================================
# TOOL FACTORY
# ============================================
def get_retrieval_tool() -> PharmacyRetrievalTool:
    """Factory function to get the retrieval tool"""
    return PharmacyRetrievalTool()