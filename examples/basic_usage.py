# examples/basic_usage.py
from src.agent.document_processor import DocumentProcessor
from src.agent.vector_store import VectorStore
import logging

def main():
    # Initialize components
    doc_processor = DocumentProcessor("config/config.yaml")
    vector_store = VectorStore("config/config.yaml")

    # Process a test document
    documents = doc_processor.process_document("examples/sample_docs/test.pdf")
    
    # Store in vector store
    vector_store.add_documents(documents)

    print("Processing completed successfully!")

if __name__ == "__main__":
    main()