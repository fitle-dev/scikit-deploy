FROM python:3.7.0-slim

WORKDIR /python/scikit-deploy

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]