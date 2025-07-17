import os
from typing import Optional

class Config:
    """Configuration class for the PocketFlow application"""
    
    def __init__(self):
        # LLM Configuration
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.gemini_project_id: str = os.getenv("GEMINI_PROJECT_ID", "your-project-id")
        self.gemini_location: str = os.getenv("GEMINI_LOCATION", "us-central1")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
        
        # Anthropic Configuration
        self.anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
        
        # OpenAI Configuration
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        
        # GitHub Configuration
        self.github_token: str = os.getenv("GITHUB_TOKEN", "")
        
        # Logging Configuration
        self.log_directory: str = os.getenv("LOG_DIR", "logs")
        
        # Cache Configuration
        self.cache_file: str = os.getenv("CACHE_FILE", "llm_cache.json")
        
        # Default LLM Provider
        self.default_llm_provider: str = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
    
    def validate_gemini_config(self) -> bool:
        """Validate Gemini configuration"""
        return bool(self.gemini_api_key)
    
    def validate_anthropic_config(self) -> bool:
        """Validate Anthropic configuration"""
        return bool(self.anthropic_api_key)
    
    def validate_openai_config(self) -> bool:
        """Validate OpenAI configuration"""
        return bool(self.openai_api_key)

# Global config instance
config = Config()