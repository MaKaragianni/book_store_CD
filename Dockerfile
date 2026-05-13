FROM python:3.13-slim

# Do not create .pyc bytecode cache files
ENV PYTHONDONTWRITEBYTECODE=1 
# Print logs/output immediately.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]