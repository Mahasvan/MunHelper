# MunHelper
Your one-stop solution for context-based UN Resolution lookup. <br>
No more searching through hundreds of pages of documents to find resolutions affecting a particular agenda! <br> 

## Features
- OpenAPI-compatible API using FastAPI
- Instant ECOSOC Resolution lookup with semantic search
- Ability to update documents with latest resolutions
- Integrate with Ollama for inference from resolution extracts
- Docker Containerization
- Auto Update (coming soon)

## Run with Docker
### This is the recommended install method.
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Docker Compose](https://docs.docker.com/compose/install/)
  - If you want to use your GPU, follow [Ollama's instructions](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image).
- Start the Docker Engine
  - Open the app on Windows/macOS
  - [Linux instructions](https://docs.docker.com/config/daemon/start/)
- Navigate to the project directory
  - ```shell
    cd MunHelper
    ```
- Start the containers using docker-compose
  - ```shell
     docker-compose -f docker-compose.yml up -d
    ```
- API is now served at `http://localhost:5000/docs`.

## Other Install Methods 

> [!NOTE]
> Since this method may leave residue if you decide to stop using the application.
> I recommend using the Docker method for a cleaner installation.

<details>

<summary>
Bare Metal installation instructions
</summary>

## Installation - Bare Metal
- Clone the repository
  - ```shell
    git clone https://github.com/Mahasvan/Munhelper
    ```
- Install the dependencies
  - ```shell
    pip install -r requirements.txt
    ```
- Set up the ChromaDB database
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
</details>

<details>
<summary>Docker build images from scratch</summary>

## Run with Docker (build images from scratch)
- Follow all steps in the [Docker Instructions](#run-with-docker) until the last step.
- Start the containers using `docker-compose-build` instead of `docker-compose`
  - ```shell
     docker-compose -f docker-compose-build.yml up -d
    ```

</details>