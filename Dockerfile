FROM python:3.10

WORKDIR app

COPY bot bot/
COPY morse morse/
COPY requirements.txt .

RUN pip install -r requirements.txt
CMD ["bash"]
