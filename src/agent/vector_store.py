# src/agent/vector_store.py
from typing import List, Dict, Any
import yaml
from pathlib import Path
from datetime import datetime
from loguru import logger

class VectorStore:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.persist_directory = "data/chroma"
        
        # Check for required packages
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            logger.error(f"Required package not found: {str(e)}")
            logger.info("Installing required packages...")
            import subprocess
            import sys
            
            # Install required packages
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                "sentence-transformers==2.2.2",
                                "chromadb==0.4.22"])
            
            # Try importing again
            import chromadb
            from sentence_transformers import SentenceTransformer
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Initialize embedding function
        from chromadb.utils import embedding_functions
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get collections
        self.health_collection = self.client.get_or_create_collection(
            name="health_insurance",
            embedding_function=self.embedding_function
        )
        
        self.auto_collection = self.client.get_or_create_collection(
            name="auto_insurance",
            embedding_function=self.embedding_function
        )
        
        logger.info(f"VectorStore initialized at {datetime.utcnow()}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def _get_policy_type(self, text: str) -> str:
        """Determine the policy type of a document or query"""
        text = text.lower()
        if 'health insurance' in text or 'copay' in text or 'prescription' in text or 'medical' in text:
            return 'health'
        elif 'auto insurance' in text or 'collision' in text or 'comprehensive' in text:
            return 'auto'
        return 'unknown'

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the appropriate ChromaDB collection"""
        try:
            health_docs = []
            auto_docs = []
            
            for idx, doc in enumerate(documents):
                content = doc['content']
                policy_type = self._get_policy_type(content)
                
                if policy_type == 'health':
                    health_docs.append({
                        'id': f"health_{idx}",
                        'content': content,
                        'metadata': doc.get('metadata', {})
                    })
                elif policy_type == 'auto':
                    auto_docs.append({
                        'id': f"auto_{idx}",
                        'content': content,
                        'metadata': doc.get('metadata', {})
                    })

            # Add to ChromaDB collections
            if health_docs:
                self.health_collection.add(
                    ids=[doc['id'] for doc in health_docs],
                    documents=[doc['content'] for doc in health_docs],
                    metadatas=[doc['metadata'] for doc in health_docs]
                )
                logger.info(f"Added {len(health_docs)} health insurance documents")

            if auto_docs:
                self.auto_collection.add(
                    ids=[doc['id'] for doc in auto_docs],
                    documents=[doc['content'] for doc in auto_docs],
                    metadatas=[doc['metadata'] for doc in auto_docs]
                )
                logger.info(f"Added {len(auto_docs)} auto insurance documents")

        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def search_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents using ChromaDB"""
        try:
            policy_type = self._get_policy_type(query)
            results = []

            if policy_type == 'health' or policy_type == 'unknown':
                health_results = self.health_collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if health_results['documents']:
                    for idx, doc in enumerate(health_results['documents'][0]):
                        results.append({
                            'content': doc,
                            'metadata': health_results['metadatas'][0][idx],
                            'policy_type': 'health',
                            'distance': health_results['distances'][0][idx] if 'distances' in health_results else None
                        })

            if policy_type == 'auto' or policy_type == 'unknown':
                auto_results = self.auto_collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                if auto_results['documents']:
                    for idx, doc in enumerate(auto_results['documents'][0]):
                        results.append({
                            'content': doc,
                            'metadata': auto_results['metadatas'][0][idx],
                            'policy_type': 'auto',
                            'distance': auto_results['distances'][0][idx] if 'distances' in auto_results else None
                        })

            # Sort results by distance if available
            if results and results[0].get('distance') is not None:
                results.sort(key=lambda x: x['distance'])

            return results

        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    def get_collection_stats(self):
        """Get statistics about the stored documents"""
        try:
            health_count = self.health_collection.count()
            auto_count = self.auto_collection.count()
            
            return {
                'health_documents': health_count,
                'auto_documents': auto_count,
                'total_documents': health_count + auto_count
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            raise