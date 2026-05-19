"""
Simple Index Builder for Windows
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path

print("=" * 50)
print("Building Vector Index for Pharmacy Documents")
print("=" * 50)

# Paths
data_dir = Path("data/pdfs")
vector_dir = Path("vector_store/faiss_index")

# Create vector store directory
vector_dir.mkdir(parents=True, exist_ok=True)

# Load documents
documents = []
if data_dir.exists():
    for file_path in data_dir.glob("*"):
        if file_path.suffix in ['.txt', '.pdf']:
            try:
                if file_path.suffix == '.txt':
                    loader = TextLoader(str(file_path), encoding='utf-8')
                    documents.extend(loader.load())
                    print(f"✓ Loaded: {file_path.name}")
            except Exception as e:
                print(f"✗ Error loading {file_path.name}: {e}")
else:
    print("No documents found. Creating sample document...")
    # Create a sample document
    sample_text = """
    Trulicity (dulaglutide) - Type 2 Diabetes Mellitus
    Dose: 0.75 mg once weekly, max 4.5 mg once weekly
    Contraindications: MTC, MEN2
    Common side effects: nausea, diarrhea
    """
    sample_path = data_dir / "sample_drug_info.txt"
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sample_path, 'w') as f:
        f.write(sample_text)
    
    loader = TextLoader(str(sample_path), encoding='utf-8')
    documents.extend(loader.load())
    print(f"✓ Created and loaded sample document")

if not documents:
    print("ERROR: No documents found or loaded!")
    sys.exit(1)

print(f"\nLoaded {len(documents)} document(s)")

# Split documents
print("Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Create embeddings
print("Creating embeddings (this may take a minute)...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector store
print("Building FAISS index...")
vector_store = FAISS.from_documents(chunks, embeddings)

# Save
print("Saving index...")
vector_store.save_local(str(vector_dir))
print(f"✓ Index saved to {vector_dir}")

print("\n" + "=" * 50)
print("SUCCESS! Vector index built.")
print("=" * 50)