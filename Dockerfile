FROM python:3.7.0-slim

WORKDIR data

COPY './scikit-deploy' .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]