"""
BUILD VECTOR INDEX
Creates FAISS index from sample documents
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import PDFS_DIR, VECTOR_STORE_DIR

print("=" * 50)
print("Building FAISS Vector Index")
print("=" * 50)

try:
    from langchain_community.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    
    print("✓ LangChain imports successful")
    
    # Load documents
    documents = []
    for file_path in PDFS_DIR.glob("*.txt"):
        try:
            loader = TextLoader(str(file_path), encoding='utf-8')
            documents.extend(loader.load())
            print(f"✓ Loaded: {file_path.name}")
        except Exception as e:
            print(f"✗ Error loading {file_path.name}: {e}")
    
    if not documents:
        print("\n⚠️ No documents found. Run create_sample_data.py first!")
        sys.exit(1)
    
    # Split documents
    print(f"\nSplitting {len(documents)} document(s)...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Create embeddings
    print("\nCreating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create vector store
    print("Building FAISS index...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_DIR / "faiss_index"))
    print(f"✓ Index saved to {VECTOR_STORE_DIR}")
    
    print("\n" + "=" * 50)
    print("INDEX BUILDING COMPLETE!")
    print("=" * 50)
    
except ImportError as e:
    print(f"\n❌ Missing dependencies: {e}")
    print("\nRun: pip install langchain langchain-community faiss-cpu sentence-transformers")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)