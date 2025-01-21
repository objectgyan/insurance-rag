# src/agent/insurance_agent.py
from typing import Dict, Any
import yaml
from loguru import logger
from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from .llm_handler import LLMHandler

class InsuranceAgent:
    def __init__(self, config_path: str):
        self.current_date = "2025-01-20 23:26:03"
        self.current_user = "objectgyan"
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.document_processor = DocumentProcessor(config_path)
        self.vector_store = VectorStore(config_path)
        self.llm_handler = LLMHandler(self.config)
        
        logger.info(f"InsuranceAgent initialized by {self.current_user}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def process_documents(self, file_paths: list):
        """Process and store documents"""
        try:
            for file_path in file_paths:
                documents = self.document_processor.process_document(file_path)
                self.vector_store.add_documents(documents)
            logger.info(f"Processed {len(file_paths)} documents")
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Process question and generate answer"""
        try:
            # Log the incoming question
            logger.info(f"Processing question: {question}")
            
            # Get relevant documents from vector store
            similar_docs = self.vector_store.search_similar(question)
            
            if not similar_docs:
                logger.warning("No relevant documents found")
                return {
                    'response': "I couldn't find any relevant information in the policy documents. Could you please rephrase your question or be more specific?",
                    'similar_documents': [],
                    'timestamp': self.current_date,
                    'user': self.current_user
                }
            
            # Generate response using LLM
            response = self.llm_handler.generate_response(
                question=question,
                context_docs=similar_docs
            )
            
            # Log successful response
            logger.info("Response generated successfully")
            
            return {
                'response': response,
                'similar_documents': similar_docs[:2],  # Return top 2 relevant documents
                'timestamp': self.current_date,
                'user': self.current_user
            }

        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                'response': f"I apologize, but I encountered an error while processing your question. Please try again.",
                'similar_documents': [],
                'timestamp': self.current_date,
                'user': self.current_user
            }