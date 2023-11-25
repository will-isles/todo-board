FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install curl -y 
RUN apt-get install git -y
RUN apt-get install unzip -y
RUN apt-get install zip -y
RUN rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/will-isles/todo-board.git .
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]