import os
from pathlib import Path
from typing import Optional
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for FinancePPT AI"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "output"
        self.assets_dir = self.base_dir / "assets"
        
        # Create directories if they don't exist
        self.templates_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment variables"""
        return os.getenv("OPENAI_API_KEY")
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Google Gemini API key from environment variables"""
        return os.getenv("GEMINI_API_KEY")
    
    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key from environment variables"""
        return os.getenv("ANTHROPIC_API_KEY")

    @property
    def openrouter_api_key(self) -> Optional[str]:
        """Get OpenRouter API key from environment variables"""
        return os.getenv("OPENROUTER_API_KEY")

    @property
    def serpapi_api_key(self) -> Optional[str]:
        """Get SerpAPI API key from environment variables"""
        return os.getenv("SERPAPI_API_KEY")
    
    def validate_api_keys(self) -> dict:
        """Validate that required API keys are present"""
        keys_status = {
            "openai": bool(self.openai_api_key),
            "gemini": bool(self.gemini_api_key),
            "anthropic": bool(self.anthropic_api_key),
            "serpapi": bool(self.serpapi_api_key)
        }
        return keys_status
    
    def get_available_models(self) -> list:
        """Get list of available AI models based on API keys"""
        models = []
        if self.openai_api_key:
            models.extend(["gpt-4", "gpt-3.5-turbo"])
        if self.gemini_api_key:
            models.extend(["gemini-pro", "gemini-pro-vision"])
        if self.anthropic_api_key:
            models.extend(["claude-3-opus", "claude-3-sonnet"])
        return models

# Global config instance
config = Config()

# For backward compatibility
SETTINGS = config
