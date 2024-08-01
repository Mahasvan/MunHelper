## Source
## https://github.com/ShawnHymel/hopper-chat/blob/master/servers/ollama/Dockerfile

# Use an appropriate base image
FROM ollama/ollama:latest

ARG OLLAMA_MODEL=gemma:2b
ARG OLLAMA_PORT=11434

# Set the working directory
WORKDIR /app

# Set the port for the ollama server
ENV OLLAMA_HOST 0.0.0.0:${OLLAMA_PORT}
EXPOSE ${OLLAMA_PORT}

RUN apt-get update && apt-get install -y curl

# Download the model
RUN \
    ollama serve & \
    sleep 5 ; \
    ollama pull ${OLLAMA_MODEL} ; \
    echo "kill 'ollama serve' process" ; \
    ps -ef | grep 'ollama serve' | grep -v grep | awk '{print $2}' | xargs -r kill -9

# Command to run the server
ENTRYPOINT ["/bin/bash", "-c", "ollama serve"]
