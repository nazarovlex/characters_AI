FROM python:3.8

WORKDIR /app

COPY . ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH /app

CMD ["python3", "web_app/web_app.py" ]