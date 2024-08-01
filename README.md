# MunHelper

Context-based UN Resolution lookup. <br>
Searches through every existing ECOSOC resolution and shows relevant data and extracts.

## Features

- OpenAPI-compatible API using FastAPI
- Instant ECOSOC Resolution lookup with semantic search
- Ability to update documents with latest resolutions
- Integration with Ollama for inference from resolution extracts
- Docker Containerization
- Auto Update (coming soon)

## Installation with Docker

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and make sure [Docker Compose](https://docs.docker.com/compose/install/) is present.
  - If you want to use your GPU, follow [Ollama's instructions](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image).
- Start the Docker Engine
  - Windows/macOS - Open the app.
  - [Linux instructions](https://docs.docker.com/config/daemon/start/)
- Navigate to the project directory
  - ```shell
    cd MunHelper
    ```
- Start the containers in detached mode using docker-compose
  - ```shell
     docker-compose -f docker-compose.yml up -d
    ```
- API is now served at `http://localhost:5000/docs`.

## Usage

- Before using anything, update the ChromaDB database.
  - If using the Documentation WebUI:
    - Visit the API Documentation at `http://localhost:5000`.
    - Run the `/manage/update-chromadb` endpoint.
  - If using the Frontend:
    - Hold on, I'm working on something.
  - Otherwise, perform a **GET** request on the `/manage/update-chromadb` endpoint and wait for the resolutions to populate.
- They will now persist on local storgage.
- If you wish to delete this data, delete the `chroma-data` volume on Docker.
  - ```shell
    docker volume ls
    ```
  - ```shell
    docker volume rm munhelper_chroma-data
    ```

## Other Installation Methods

> [!NOTE]
> These methods may leave residue if you decide to uninstall.
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
- Set up environment variables (refer `app.py`)
- Change `bare_metal` variable in `app.py` to True
- Start the API
  - ```shell
    python app.py
    ```
- Access the API at `http://localhost:5000/docs` 
- Setting up the frontend
  - Open another terminal window, and `cd` into the `frontend` folder
  - Run `streamlit run frontend.py`
  - Frontend is served at `http://localhost:8051`
</details>

<details>
<summary>Docker build images from scratch</summary>

## Run with Docker (build images from scratch)

- Follow all steps in the [Docker Instructions](#installation-with-docker) until the last step.
- Start the containers using `docker-compose-build` instead of `docker-compose`
  - ```shell
     docker-compose -f docker-compose-build.yml up -d
    ```
- Make sure to read the [Usage](#usage) section.
</details>