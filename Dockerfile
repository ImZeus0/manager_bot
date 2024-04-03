FROM --platform=linux/amd64 python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y
LABEL service=manager_bot
WORKDIR /app
COPY ./ /app
RUN pip3 install -r req.txt
CMD ["python3","app.py"]
