# Insurance Policy RAG Assistant

A Python-based AI-powered assistant that uses RAG (Retrieval-Augmented Generation) to answer questions about insurance policies.

## Features

- Processes insurance policy documents (health and auto)
- Uses ChromaDB for vector storage and semantic search
- Leverages the OPT-350M language model for response generation
- Supports both health and auto insurance policy queries
- Includes document caching and GPU acceleration

## Installation

1. **Clone the repository**
    ```sh
    git clone <repository-url>
    ```

2. **Create and activate virtual environment**
    - **Linux/Mac**
        ```sh
        python -m venv venv
        source venv/bin/activate
        ```
    - **Windows**
        ```sh
        python -m venv venv
        venv\Scripts\activate
        ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

## Project Structure

- **agent**: Core agent components
- **examples**: Sample documents and usage examples
- **config**: Configuration files
- **data**: Vector store data
- **cache**: Model and response caching

## Usage

1. **Process sample documents**
    ```sh
    python setup_documents.py
    ```

2. **Run interactive test session**
    ```sh
    python test_interactive.py
    ```

## Configuration

Edit `config.yaml` to modify:
- LLM settings (model, temperature, etc.)
- Vector store configuration
- Document processing parameters

## Sample Questions

### Health Insurance
- What is my primary care copay?
- What's my prescription drug coverage?
- How do I access virtual care?

### Auto Insurance
- What is my collision deductible?
- What are my liability limits?
- How do I file a claim?

## Dependencies

- torch==2.5.1
- transformers==4.36.2
- sentence-transformers==2.2.2
- chromadb==0.4.22
- huggingface-hub==0.19.4
- loguru==0.7.2
- pyyaml==6.0.1
