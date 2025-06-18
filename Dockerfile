FROM python:3.9-slim

WORKDIR /app

COPY ai_agent_sdk.py .

RUN ai_agent_sdk.py .

ENTRYPOINT ["python", "ai_agent_sdk.py"]
