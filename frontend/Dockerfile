FROM python:3.9.19-bookworm
LABEL authors="mahas"

# Set the working directory
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install streamlit requests

EXPOSE ${PORT}

# Run the app
ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
