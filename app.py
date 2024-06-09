import importlib.util
import os

from api.service import shell

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"ping": "I am alive!"}


# load API Routers
routes = [x.rstrip(".py") for x in os.listdir("api/route") if x.endswith(".py") and not x.startswith("_")]

for route in routes:
    shell.print_cyan_message(f"Loading {route}...")
    try:
        importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
        module = importlib.import_module(f"api.route.{route}")
        module.setup(app)
        shell.print_green_message("Success!")
    except Exception as e:
        shell.print_red_message(f"Failed:")
        print(e)


"""
Environment Variables:
CHAT_MODEL = llama3
OLLAMA_BASE_URL = http://localhost:11434
CHROMA_HOST = localhost
CHROMA_PORT = 8000
CHROMA_COLLECTION = ecosoc
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
