FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/will-isles/todo-board.git .

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]