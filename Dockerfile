FROM python:3.9-slim


WORKDIR /appAdd commentMore actions


COPY ai_agent_sdk.py .


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "ai_agent_sdk.py"]
