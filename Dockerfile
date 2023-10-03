FROM python:3.11.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  