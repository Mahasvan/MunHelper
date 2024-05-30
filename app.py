import importlib.util
import os

from api.service import shell

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# load API Routers
routes = [x.rstrip(".py") for x in os.listdir("api/route") if x.endswith(".py") and not x.startswith("_")]

for route in routes:
    print(f"Loading {route}...")
    try:
        importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
        module = importlib.import_module(f"api.route.{route}")
        module.setup(app)
        shell.print_green_message("Success!")
    except Exception as e:
        shell.print_red_message(f"        |--- Failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
