# MunHelper
Your one-stop solution for context-based UN Resolution lookup. <br>
No more searching through hundreds of pages of documents to find resolutions affecting a particular agenda! <br> 

## Features
- OpenAPI-compatible API using FastAPI
- Instant ECOSOC Resolution lookup with semantic search
- Other UN Bodies coming soon!
- Integrate with Ollama to infer context from resolution extracts using Local LLMs
- Docker Containerization (coming soon)
- Update documents with latest resolutions (coming soon)

## Usage
- Clone the repository
  - ```shell
    git clone https://github.com/Mahasvan/Munhelper
    ```
  - Install the dependencies
    - ```shell
      pip install -r requirements.txt
      ```
  - Set up the ChromaDB database
    - Add resolutions to vector database (Script soon)
    - Run the server using 
    - ```shell
      chroma run
      ```
  - Install Ollama and pull preferred model 
    - ```shell
      ollama pull llama3
      ```
  - Start the API
    - ```shell
      python app.py
      ```
  - Access the API
    - ```shell
      http://localhost:5000/docs
      ```
