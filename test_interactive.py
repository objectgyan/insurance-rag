# test_interactive.py
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger
import yaml
from typing import List, Dict

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.agent import InsuranceAgent

class InteractiveTest:
    def __init__(self):
        self.current_date = "2025-01-20 22:18:11"  # Updated timestamp
        self.current_user = "objectgyan"
        self.history: List[Dict] = []
        
        # Sample questions categorized by policy type
        self.auto_questions = [
            "What is my collision deductible?",
            "What's my comprehensive coverage limit?",
            "How do I file an auto claim?",
            "What are my liability limits for auto?",
            "What is my auto policy number?"
        ]

        self.health_questions = [
            "What is my primary care copay?",
            "Is my annual check-up covered?",
            "What's my prescription drug coverage?",
            "What's my emergency room copay?",
            "How do I find a health provider?"
        ]

        self.sample_questions = {
            'auto': self.auto_questions,
            'health': self.health_questions
        }

    def print_header(self):
        print("\n" + "="*50)
        print("Insurance RAG Interactive Test Session")
        print(f"Date: {self.current_date}")
        print(f"User: {self.current_user}")
        print("="*50 + "\n")

    def show_chroma_stats(self):
        """Display ChromaDB collection statistics with detailed information"""
        try:
            print("\nChromaDB Collection Statistics:")
            print("=" * 50)
            
            # Get health collection details
            health_docs = self.agent.vector_store.health_collection.get()
            print("\nHealth Insurance Collection:")
            print(f"Number of Documents: {len(health_docs['ids']) if 'ids' in health_docs else 0}")
            if 'ids' in health_docs and health_docs['ids']:
                print("\nDocument IDs:")
                for idx, doc_id in enumerate(health_docs['ids']):
                    print(f"{idx + 1}. {doc_id}")

            # Get auto collection details
            auto_docs = self.agent.vector_store.auto_collection.get()
            print("\nAuto Insurance Collection:")
            print(f"Number of Documents: {len(auto_docs['ids']) if 'ids' in auto_docs else 0}")
            if 'ids' in auto_docs and auto_docs['ids']:
                print("\nDocument IDs:")
                for idx, doc_id in enumerate(auto_docs['ids']):
                    print(f"{idx + 1}. {doc_id}")

            print("\nTimestamp:", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
            print("=" * 50)
        except Exception as e:
            print(f"Error getting ChromaDB stats: {str(e)}")

    def print_help(self):
        print("\nAvailable Commands:")
        print("  help       - Show this help message")
        print("  auto       - Show auto insurance questions")
        print("  health     - Show health insurance questions")
        print("  history    - Show question history")
        print("  list       - Show list of stored documents")
        print("  stats      - Show ChromaDB collection statistics")
        print("  llm        - Show LLM model information")
        print("  model      - Select different LLM model")
        print("  show_doc auto    - Show full auto insurance policy")
        print("  show_doc health  - Show full health insurance policy")
        print("  clear      - Clear screen")
        print("  exit       - Exit the program")

        
        print("\nExample Auto Insurance Questions:")
        for i, q in enumerate(self.auto_questions, 1):
            print(f"  a{i}. {q}")
        
        print("\nExample Health Insurance Questions:")
        for i, q in enumerate(self.health_questions, 1):
            print(f"  h{i}. {q}")
            
        print("\nTip: You can use 'a1'-'a5' for auto questions or 'h1'-'h5' for health questions")
        print()

    def clear_screen(self):
        print("\n" * 50)
        self.print_header()

    def show_history(self):
        if not self.history:
            print("\nNo questions asked yet.")
            return

        print("\nQuestion History:")
        for i, item in enumerate(self.history, 1):
            print(f"\n{i}. Q: {item['question']}")
            print(f"   A: {item['answer'][:150]}...")
            print(f"   Policy Type: {item['policy_type']}")
        print()

    def get_policy_type(self, question: str) -> str:
        """Determine which policy the question is about"""
        question = question.lower()
        
        # Keywords for each policy type
        auto_keywords = ['auto', 'car', 'vehicle', 'collision', 'comprehensive', 'liability']
        health_keywords = ['health', 'medical', 'prescription', 'copay', 'doctor', 'hospital', 
                         'emergency room', 'specialist', 'therapy', 'mental health']

        for keyword in auto_keywords:
            if keyword in question:
                return 'auto'
                
        for keyword in health_keywords:
            if keyword in question:
                return 'health'

        return 'unknown'

    def get_llm_info(self):
        """Get information about current LLM model"""
        try:
            model_info = self.agent.llm_handler.get_model_info()
            print("\nCurrent LLM Configuration:")
            print("=" * 50)
            print(f"Model: {model_info['model_name']}")
            print(f"Provider: {model_info['provider']}")
            print(f"Cache Enabled: {model_info['cache_enabled']}")
            print(f"Last Used: {model_info['last_used']}")
            print("=" * 50)
        except Exception as e:
            print(f"Error getting LLM info: {str(e)}")

    def select_model(self):
        """Allow user to select different free models"""
        print("\nAvailable Free LLM Models:")
        print("1. TinyLlama-1.1B-Chat (Recommended)")
        print("2. facebook/opt-350m (Faster)")
        print("3. google/flan-t5-base (Good for Q&A)")
        
        choice = input("\nSelect model (1-3): ").strip()
        
        models = {
            "1": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "2": "facebook/opt-350m",
            "3": "google/flan-t5-base"
        }
        
        if choice in models:
            self.agent.llm_handler.change_model(models[choice])
            print(f"\nSwitched to model: {models[choice]}")
        else:
            print("\nInvalid choice. Keeping current model.")

    def show_documents(self):
        docs_dir = Path("examples/sample_docs")
        if not docs_dir.exists():
            print("\nNo documents directory found.")
            return

        print("\nStored Documents:")
        print("=" * 50)
        
        for file_path in docs_dir.glob("*.txt"):
            print(f"\nFile: {file_path.name}")
            print("-" * 50)
            try:
                content = file_path.read_text()
                # Print first section of each document
                sections = content.split('\n\n')
                # Print header and first few sections
                for section in sections[:3]:
                    if section.strip():
                        print(section.strip())
                print("...")
                print(f"\nTotal sections: {len(sections)}")
                print("-" * 50)
            except Exception as e:
                print(f"Error reading file: {str(e)}")

    def show_specific_document(self, doc_type: str):
        docs_dir = Path("examples/sample_docs")
        
        if doc_type.lower() == 'auto':
            file_name = "auto_policy.txt"
        elif doc_type.lower() == 'health':
            file_name = "health_policy.txt"
        else:
            print(f"Unknown document type: {doc_type}")
            return

        file_path = docs_dir / file_name
        if not file_path.exists():
            print(f"\nDocument not found: {file_name}")
            return

        print(f"\nFull content of {file_name}:")
        print("=" * 50)
        try:
            content = file_path.read_text()
            print(content)
        except Exception as e:
            print(f"Error reading file: {str(e)}")

    def run(self):
        try:
            self.print_header()
            
            # Initialize agent
            print("Initializing Insurance Agent...")
            self.agent = InsuranceAgent("config/config.yaml")

            # Process existing documents
            docs_dir = Path("examples/sample_docs")
            if docs_dir.exists():
                documents = list(docs_dir.glob("*.txt"))
                if documents:
                    print(f"Processing {len(documents)} documents...")
                    self.agent.process_documents([str(doc) for doc in documents])
                    print("Documents processed successfully!")

            print("\nType 'help' for available commands or start asking questions!")
            print("Type 'exit' to quit\n")

            while True:
                try:
                    user_input = input("\nYour question: ").strip()

                    if not user_input:
                        continue

                    # Handle commands
                    if user_input.lower() == 'exit':
                        print("\nThank you for using Insurance RAG. Goodbye!")
                        break
                    elif user_input.lower() == 'help':
                        self.print_help()
                    elif user_input.lower() == 'auto':
                        print("\nAuto Insurance Questions:")
                        for i, q in enumerate(self.auto_questions, 1):
                            print(f"a{i}. {q}")
                    elif user_input.lower() == 'health':
                        print("\nHealth Insurance Questions:")
                        for i, q in enumerate(self.health_questions, 1):
                            print(f"h{i}. {q}")
                    elif user_input.lower() == 'history':
                        self.show_history()
                    elif user_input.lower() == 'clear':
                        self.clear_screen()
                    elif user_input.lower() == 'stats':
                        self.show_chroma_stats()
                    else:
                        # Process the question
                        self.process_question(user_input)

                except KeyboardInterrupt:
                    print("\n\nInterrupted by user. Type 'exit' to quit or continue asking questions.")
                    continue
                except Exception as e:
                    print(f"\nError: {str(e)}")
                    logger.error(f"Error: {str(e)}")

        except Exception as e:
            logger.error(f"Session Error: {str(e)}")
            return 1

        return 0

    def process_question(self, question: str):
        """Process a question and display the response"""
        try:
            print("\nProcessing your question...")
            
            # Get response from agent
            response = self.agent.answer_question(question)
            
            # Display response
            print("\nAnswer:")
            print("=" * 50)
            print(response['response'])
            print("=" * 50)
            
            # Display relevant documents
            if response['similar_documents']:
                print("\nRelevant Policy Sections:")
                for idx, doc in enumerate(response['similar_documents'], 1):
                    print(f"\n{idx}. {doc['content'][:200]}...")
            
            # Add to history
            self.history.append({
                'question': question,
                'answer': response['response'],
                'timestamp': self.current_date,
                'policy_type': self.get_policy_type(question)
            })
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            logger.error(f"Error processing question: {str(e)}")
        
    def show_system_info(self):
        """Display complete system information"""
        try:
            print("\nSystem Information:")
            print("=" * 50)
            print(f"Date/Time (UTC): {self.current_date}")
            print(f"User: {self.current_user}")
            
            # LLM Information
            model_info = self.agent.llm_handler.get_model_info()
            print("\nLLM Configuration:")
            print(f"- Model: {model_info['model_name']}")
            print(f"- Provider: {model_info['provider']}")
            print(f"- Cache: {'Enabled' if model_info['cache_enabled'] else 'Disabled'}")
            
            # Vector Store Information
            print("\nVector Store:")
            stats = self.agent.vector_store.get_collection_stats()
            print(f"- Health Documents: {stats['health_documents']}")
            print(f"- Auto Documents: {stats['auto_documents']}")
            
            # System Status
            print("\nSystem Status:")
            print("- Document Processor: Active")
            print("- Vector Store: Active")
            print("- LLM Integration: Active")
            print("=" * 50)
        except Exception as e:
            print(f"Error showing system info: {str(e)}")

if __name__ == "__main__":
    interactive_test = InteractiveTest()
    sys.exit(interactive_test.run())