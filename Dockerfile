FROM python:3.10

WORKDIR app

COPY bot bot/
COPY requirements.txt .

RUN pip install -r requirements.txt
CMD ["python", "bot/app.py"]
