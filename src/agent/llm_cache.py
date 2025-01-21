# src/agent/llm_cache.py
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime
import hashlib

class LLMCache:
    def __init__(self, cache_dir: str = "cache/llm"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.current_date = "2025-01-20 22:57:56"
        self.current_user = "objectgyan"

    def _get_cache_key(self, question: str, context: str) -> str:
        """Generate cache key from question and context"""
        combined = f"{question}|{context}"
        return hashlib.md5(combined.encode()).hexdigest()

    def get_cached_response(self, question: str, context: str) -> Dict[str, Any]:
        """Get cached response if available"""
        cache_key = self._get_cache_key(question, context)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None

    def cache_response(self, 
                      question: str, 
                      context: str, 
                      response: str):
        """Cache the response"""
        cache_key = self._get_cache_key(question, context)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        cache_data = {
            'question': question,
            'context': context,
            'response': response,
            'cached_at': self.current_date,
            'cached_by': self.current_user
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)