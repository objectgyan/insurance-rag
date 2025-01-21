# src/agent/llm_handler.py
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMHandler:
    def __init__(self, config: Dict[str, Any]):
        self.current_date = "2025-01-20 23:18:40"
        self.current_user = "objectgyan"
        self.config = config
        self.model_name = "facebook/opt-350m"
        
        # Check GPU and CUDA version
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            self.gpu_name = torch.cuda.get_device_name(0)
            self.cuda_version = torch.version.cuda
            logger.info(f"Using GPU: {self.gpu_name} with CUDA {self.cuda_version}")
        else:
            logger.warning("No GPU found, using CPU")
            
        self._initialize_model()
        logger.info(f"LLMHandler initialized by {self.current_user}")

    def _initialize_model(self):
        """Initialize the model with CUDA 12.2 support"""
        try:
            # Initialize tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir="cache/models"
            )
            
            # Initialize model with CUDA support
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                cache_dir="cache/models"
            )
            
            # Move model to GPU if available
            if self.device == "cuda":
                self.model = self.model.to(self.device)
                logger.info(f"GPU Memory Allocated: {torch.cuda.memory_allocated(0)/1024**2:.2f}MB")
                logger.info(f"GPU Memory Reserved: {torch.cuda.memory_reserved(0)/1024**2:.2f}MB")
            
            logger.info(f"Model {self.model_name} loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_response(self, 
                         question: str, 
                         context_docs: List[Dict[str, Any]]) -> str:
        """Generate response using model"""
        try:
            # Prepare context from relevant documents
            context = "\n\n".join([doc['content'] for doc in context_docs])
            
            # Create prompt
            prompt = f"""### System: You are an insurance policy assistant. 
Provide accurate, clear answers based only on the provided policy information.

### Context: 
{context}

### Human: {question}

### Assistant: Let me help you with that based on the policy information provided."""

            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            # Move inputs to GPU if available
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response with GPU acceleration
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=500,
                    num_return_sequences=1,
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant's response
            if "### Assistant:" in response:
                response = response.split("### Assistant:")[-1].strip()
            
            return response

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return f"Error generating response: {str(e)}"

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        gpu_info = {}
        if self.device == "cuda":
            gpu_info = {
                'gpu_name': self.gpu_name,
                'cuda_version': self.cuda_version,
                'gpu_memory_allocated': f"{torch.cuda.memory_allocated(0)/1024**2:.2f}MB",
                'gpu_memory_reserved': f"{torch.cuda.memory_reserved(0)/1024**2:.2f}MB",
                'driver_version': "538.78"  # From nvidia-smi
            }
            
        return {
            'model_name': self.model_name,
            'provider': 'local',
            'device': self.device,
            'gpu_info': gpu_info,
            'cache_enabled': True,
            'last_used': self.current_date,
            'user': self.current_user
        }