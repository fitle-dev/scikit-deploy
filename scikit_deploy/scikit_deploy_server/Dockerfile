FROM python:3.6-slim

WORKDIR /python/scikit-deploy

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && python3 validate.py

EXPOSE 5000

CMD ["python3", "main.py"]