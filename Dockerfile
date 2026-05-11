FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PROJECT_HOME=/app
CMD ["python", "resources/web/predict_flask.py"]