import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgentSDK(ABC):
    """Base SDK for creating AI agents compatible with GitHub Actions environment variables."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the AI Agent SDK with environment variable support.
        
        Args:
            config_path: Optional path to .env file for local development
        """
        # Load .env file if provided (useful for local development)
        if config_path:
            load_dotenv(config_path)
            
        # Required environment variables
        self.required_env_vars = [
            'OPENAI_API_KEY',  # Example for OpenAI integration
            'AGENT_NAME',      # Custom agent identifier
            'GITHUB_TOKEN'     # GitHub token for repository access
            'LICENSE_SERVER'
        ]
        
        # Optional environment variables with defaults
        self.default_env_vars = {
            'AGENT_LOG_LEVEL': 'INFO',
            'MAX_RETRIES': '3',
            'TIMEOUT_SECONDS': '30',
            'LICENSE_SERVER':'https://ai-agent-license-server.onrender.com/validate'
        }
        
        self.config = self._load_config()
        self._validate_config()
        self._setup_logging()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        # Load required environment variables
        for var in self.required_env_vars:
            value = os.getenv(var)
            if value is None:
                logger.warning(f"Environment variable {var} not found")
            config[var] = value
            
        # Load optional environment variables with defaults
        for var, default in self.default_env_vars.items():
            config[var] = os.getenv(var, default)
            
        return config
    
    def _validate_config(self) -> None:
        """Validate required environment variables."""
        missing_vars = [var for var in self.required_env_vars if not self.config.get(var)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
            
    def _setup_logging(self) -> None:
        """Configure logging based on environment variable."""
        log_level = getattr(logging, self.config['AGENT_LOG_LEVEL'].upper(), logging.INFO)
        logger.setLevel(log_level)
        
    def get_config(self, key: str) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key to retrieve
            
        Returns:
            Configuration value
        """
        return self.config.get(key)
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Abstract method to execute an AI agent task.
        
        Args:
            task: Task definition dictionary
            
        Returns:
            Task execution results
        """
        pass
    
    def safe_get_env(self, key: str, default: Any = None) -> Any:
        """
        Safely retrieve environment variable with fallback.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
    
    def update_config(self, key: str, value: Any) -> None:
        """
        Update configuration value.
        
        Args:
            key: Configuration key to update
            value: New value
        """
        self.config[key] = value
        logger.info(f"Updated configuration: {key}")

class SampleAIAgent(AIAgentSDK):
    """Sample implementation of an AI agent using the SDK."""
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a sample AI task.
        
        Args:
            task: Task definition dictionary with 'input' key
            
        Returns:
            Task execution results
        """
        try:
            # Sample task execution
            input_data = task.get('input', '')
            agent_name = self.get_config('AGENT_NAME')
            
            # Simulate AI processing
            result = {
                'status': 'success',
                'agent_name': agent_name,
                'processed_data': f"Processed: {input_data}",
                'github_token_used': len(self.get_config('GITHUB_TOKEN')) > 0
            }
            
            logger.info(f"Task executed successfully by {agent_name}")
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e)
            }

if __name__ == "__main__":
    # Example usage
    try:
        # Initialize agent with optional .env file for local testing
        agent = SampleAIAgent(config_path='.env')
        
        # Sample task
        task = {
            'input': 'Hello, AI Agent!'
        }
        
        # Execute task
        result = agent.execute_task(task)
        print(result)
        
    except Exception as e:
        logger.error(f"Agent initialization failed: {str(e)}")
