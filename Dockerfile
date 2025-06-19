FROM python:3.9-slim

WORKDIR /app

COPY ai_agent_sdk.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "ai_agent_sdk.py"]