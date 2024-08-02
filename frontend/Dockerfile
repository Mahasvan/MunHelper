FROM python:3.9.19-bookworm

# Install dependencies
RUN pip install streamlit requests

# Set the working directory
COPY . /app
WORKDIR /app

EXPOSE ${PORT}

# Run the app
ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
