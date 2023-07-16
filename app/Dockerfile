FROM ubuntu:20.04

ENV TZ=Asia/Singapore

RUN apt-get update -y && apt-get install tzdata

RUN apt-get install -y build-essential cmake \
ffmpeg libsm6 libxext6 libxrender-dev \
python3.8 python3-pip python3-dev

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]