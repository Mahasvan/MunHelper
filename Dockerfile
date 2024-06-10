# escape=\

FROM ubuntu:latest

# install tesseract
RUN apt-get update

# install python
RUN apt-get install -y python3 python3-pip python3-venv git curl

COPY . /MunHelper
WORKDIR /MunHelper
RUN python3 -m ensurepip
RUN pip3 install -r requirements.txt
# install requirements

# Run
EXPOSE 8000
CMD python3 app.py
