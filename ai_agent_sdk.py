import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path
import requests 

__version__ = "0.1.0"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgentSDK:
    """SDK for AI-powered task automation in GitHub Actions."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the AI Agent SDK.
        
        Args:
            config_path: Optional path to .env file for local development
        """
        if config_path:
            load_dotenv(config_path)
            
        self.required_env_vars = [
            'OPENAI_API_KEY',
            'AGENT_NAME',
            'GITHUB_TOKEN'
        ]
        
        self.default_env_vars = {
            'AGENT_LOG_LEVEL': 'INFO',
            'MAX_RETRIES': '3',
            'TIMEOUT_SECONDS': '30',
            'LICENSE_SERVER': 'https://your-license-server.com/validate'  # Placeholder for paid tier validation
        }
        
        self.config = self._load_config()
        self._validate_config()
        self._setup_logging()
        self.is_licensed = self._check_license()
        self._requests.get = self._requests.get()
       self._requests.post = self_requests.post()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        for var in self.required_env_vars:
            config[var] = os.getenv(var)
        for var, default in self.default_env_vars.items():
            config[var] = os.getenv(var, default)
        return config
    
    def _validate_config(self) -> None:
        """Validate required environment variables."""
        missing_vars = [var for var in self.required_env_vars if not self.config.get(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
    def _setup_logging(self) -> None:
        """Configure logging based on environment variable."""
        log_level = getattr(logging, self.config['AGENT_LOG_LEVEL'].upper(), logging.INFO)
        logger.setLevel(log_level)
        
    def _check_license(self) -> bool:
        """
        Check if the Action is licensed for private repos.
        For free tier, allow public repos only.
        """
        repo_visibility = os.getenv('GITHUB_REPOSITORY_VISIBILITY', 'public')
        if repo_visibility == 'public':
            return True  # Free tier for public repos
        try:
            response = requests.post(
                self.config['LICENSE_SERVER'],
                json={'github_token': self.config['GITHUB_TOKEN'], 'repo': os.getenv('GITHUB_REPOSITORY')},
                timeout=5
            )
            return response.json().get('licensed', False)
        except Exception as e:
            logger.warning(f"License check failed: {str(e)}. Defaulting to free tier.")
            return False
    
    def get_config(self, key: str) -> Any:
        """Get configuration value by key."""
        return self.config.get(key)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an AI task.
        
        Args:
            task: Task definition dictionary with 'input' key
            
        Returns:
            Task execution results
        """
        if not self.is_licensed and os.getenv('GITHUB_REPOSITORY_VISIBILITY') == 'private':
            return {
                'status': 'error',
                'error_message': 'Paid license required for private repositories'
            }
        
        try:
            input_data = task.get('input', '')
            agent_name = self.get_config('AGENT_NAME')
            result = {
                'status': 'success',
                'agent_name': agent_name,
                'processed_data': f"Processed: {input_data}",
                'github_token_used': len(self.config['GITHUB_TOKEN']) > 0,
                'license_status': 'premium' if self.is_licensed else 'free'
            }
            logger.info(f"Task executed successfully by {agent_name}")
            return result
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e)
            }
    
    def safe_get_env(self, key: str, default: Any = None) -> Any:
        """Safely retrieve environment variable with fallback."""
        return os.getenv(key, default)

def main():
    """Entry point for CLI or GitHub Action execution."""
    try:
        agent = AIAgentSDK(config_path=os.getenv('CONFIG_PATH', '.env'))
        task_input = os.getenv('TASK_INPUT', '{}')
        task_file = os.getenv('TASK_FILE')
        if task_file and Path(task_file).exists():
            with open(task_file, 'r') as f:
                task = json.load(f)
        else:
            task = json.loads(task_input)
        result = agent.execute_task(task)
        print(json.dumps(result))
    except Exception as e:
        logger.error(f"Agent initialization failed: {str(e)}")
        print(json.dumps({'status': 'error', 'error_message': str(e)}))

if __name__ == "__main__":
    main()
