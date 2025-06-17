from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import sqlite3
from typing import Optional
import requests
import os
import logging
import hmac
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# SQLite database setup
DB_PATH = os.getenv("DB_PATH", "/data/subscriptions.db")

def init_db():
    """Initialize SQLite database for storing subscriptions."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                github_user_id TEXT,
                repository TEXT,
                plan TEXT,
                status TEXT,
                PRIMARY KEY (github_user_id, repository)
            )
        """)
        conn.commit()

init_db()

class LicenseRequest(BaseModel):
    github_token: str
    repository: str
    action_id: str

class LicenseResponse(BaseModel):
    licensed: bool
    message: Optional[str] = None

def verify_token(token: str, repo: str) -> Optional[dict]:
    """Verify GitHub token and get user/repo info."""
    try:
        headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github.v3+json'}
        user_response = requests.get('https://api.github.com/user', headers=headers, timeout=5)
        user_response.raise_for_status()
        user_data = user_response.json()
        
        repo_response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers, timeout=5)
        repo_response.raise_for_status()
        
        return {'user_id': str(user_data['id']), 'login': user_data['login']}
    except requests.RequestException as e:
        logger.error(f"GitHub API error: {str(e)}")
        return None

@app.post("/validate", response_model=LicenseResponse)
async def validate_license(request: LicenseRequest):
    """Validate license for a repository."""
    logger.info(f"Validating license for repository: {request.repository}")
    
    user_info = verify_token(request.github_token, request.repository)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid GitHub token or repository access")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM subscriptions WHERE github_user_id = ? AND repository = ?",
            (user_info['user_id'], request.repository)
        )
        result = cursor.fetchone()
        
        if result and result[0] == 'active':
            logger.info(f"Active subscription found for {user_info['login']} in {request.repository}")
            return LicenseResponse(licensed=True)
        
    marketplace_token = os.getenv('MARKETPLACE_TOKEN')
    if marketplace_token:
        try:
            headers = {'Authorization': f'Bearer {marketplace_token}', 'Accept': 'application/vnd.github.v3+json'}
            purchases = requests.get(
                f'https://api.github.com/user/marketplace_purchases',
                headers=headers,
                timeout=5
            )
            purchases.raise_for_status()
            for purchase in purchases.json():
                if purchase['account']['login'] == user_info['login'] and purchase['plan']['name'] == 'premium':
                    return LicenseResponse(licensed=True)
        except requests.RequestException as e:
            logger.warning(f"Marketplace API error: {str(e)}")
    
    return LicenseResponse(licensed=False, message="No active subscription found")

@app.post("/webhook")
async def handle_marketplace_webhook(payload: dict, request: Request):
    """Handle GitHub Marketplace webhook events."""
    webhook_secret = os.getenv('WEBHOOK_SECRET')
    if webhook_secret:
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not signature:
            raise HTTPException(status_code=401, detail="Missing webhook signature")
        raw_body = await request.body()
        computed = hmac.new(
            webhook_secret.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(f'sha256={computed}', signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    action = payload.get('action')
    sender = payload.get('sender', {})
    user_id = str(sender.get('id'))
    repository = payload.get('marketplace_purchase', {}).get('account', {}).get('login')
    plan = payload.get('marketplace_purchase', {}).get('plan', {}).get('name')
    
    logger.info(f"Received webhook: {action} for {repository}")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if action in ['purchased', 'changed']:
            status = 'active' if plan == 'premium' else 'inactive'
            cursor.execute(
                """
                INSERT OR REPLACE INTO subscriptions (github_user_id, repository, plan, status)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, repository, plan, status)
            )
        elif action in ['cancelled', 'pending_change_cancelled']:
            cursor.execute(
                "UPDATE subscriptions SET status = ? WHERE github_user_id = ? AND repository = ?",
                ('inactive', user_id, repository)
            )
        conn.commit()
    
    return {"status": "success"}
