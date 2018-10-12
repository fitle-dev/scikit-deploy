FROM python:3.6-stretch

WORKDIR /python/scikit-deploy

COPY . .

RUN pip install --upgrade pip \
    && pip install gunicorn \
    && pip install -r requirements.txt \
    && python3 validate.py

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "main:app"]