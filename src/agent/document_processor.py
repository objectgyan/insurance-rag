# src/agent/document_processor.py
from typing import List, Dict, Any
from pathlib import Path
import yaml
from loguru import logger
from datetime import datetime

class DocumentProcessor:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.current_date = "2025-01-20 22:38:06"  # Updated timestamp
        self.current_user = "objectgyan"
        logger.info(f"DocumentProcessor initialized by {self.current_user}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def _extract_text(self, file_path: Path) -> str:
        """Extract text from a file"""
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise ValueError(f"Unsupported file type: {suffix}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise

    def _split_text(self, text: str) -> List[str]:
        """Split text into sections based on policy type"""
        try:
            # Determine policy type
            is_health = 'HEALTH INSURANCE POLICY' in text
            is_auto = 'AUTO INSURANCE POLICY' in text

            # Keep the document as a single chunk with complete context
            if is_health or is_auto:
                return [text]
            
            # For other documents, split by sections
            sections = []
            current_section = []
            
            for line in text.split('\n'):
                if line.strip():
                    current_section.append(line)
                elif current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
                    
            if current_section:
                sections.append('\n'.join(current_section))
                
            return sections

        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise

    def _get_document_type(self, text: str) -> str:
        """Determine the type of document"""
        text_lower = text.lower()
        if 'health insurance policy' in text_lower:
            return 'health'
        elif 'auto insurance policy' in text_lower:
            return 'auto'
        return 'unknown'

    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a document and return as a single document with metadata"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Extract text from file
            text = self._extract_text(file_path)
            
            # Get document type
            doc_type = self._get_document_type(text)
            
            # Create a single document with complete content
            document = {
                'content': text,
                'metadata': {
                    'source': str(file_path),
                    'doc_type': doc_type,
                    'processed_at': self.current_date,
                    'processed_by': self.current_user,
                    'file_type': file_path.suffix.lower(),
                    'file_name': file_path.name
                }
            }

            logger.info(f"Successfully processed {doc_type} document: {file_path}")
            return [document]  # Return as list for consistency

        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def get_document_stats(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about processed documents"""
        try:
            stats = {
                'total_documents': len(documents),
                'by_type': {},
                'processed_at': self.current_date,
                'processed_by': self.current_user
            }
            
            for doc in documents:
                doc_type = doc['metadata']['doc_type']
                stats['by_type'][doc_type] = stats['by_type'].get(doc_type, 0) + 1
                
            return stats
            
        except Exception as e:
            logger.error(f"Error getting document stats: {str(e)}")
            raise