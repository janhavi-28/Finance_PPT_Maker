from openai import OpenAI
import google.generativeai as genai
import anthropic
import httpx
from typing import Optional, Dict, Any, List
import streamlit as st
from config.settings import config
import json

class AIService:
    """Secure AI service manager for multiple providers"""
    
    def __init__(self):
        self.clients: Dict[str, Any] = {}
        self.available_models: Dict[str, List[str]] = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI clients based on available API keys"""
        # Create HTTP client with timeout
        http_client = httpx.Client(timeout=30.0)
        
        # OpenRouter for GPT-5 - disabled for SerpAPI-only mode
        if config.openrouter_api_key:
            try:
                self.clients['openrouter'] = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=config.openrouter_api_key,
                    http_client=http_client
                )
                self.available_models['openrouter'] = ['openai/gpt-5']
            except Exception as e:
                pass  # Silent skip
        else:
            # Silent fallback - no warnings
            pass
            # Fallback to direct OpenAI - disabled
            if config.openai_api_key:
                try:
                    self.clients['openai'] = OpenAI(
                        api_key=config.openai_api_key,
                        http_client=http_client
                    )
                    self.available_models['openai'] = ['gpt-4o']
                except Exception as e:
                    pass  # Silent skip
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        return list(self.clients.keys())
    
    def get_default_model(self, provider: str) -> str:
        """Get the default model for a provider"""
        defaults = {
            'openai': 'gpt-5'
        }
        return defaults.get(provider.lower(), 'gpt-5')

    def generate_content(self, prompt: str, model: str) -> str:
        """Generate content using the specified model"""
        try:
            if model == "openai/gpt-5" and self.clients.get('openrouter'):
                response = self.clients['openrouter'].chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7,
                    extra_headers={
                        "HTTP-Referer": "https://finance-ppt-ai.local",
                        "X-Title": "Finance PPT AI",
                    },
                    extra_body={}
                )
                return response.choices[0].message.content
            elif 'gpt' in model.lower() and self.clients.get('openai'):
                response = self.clients['openai'].chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content

            else:
                raise ValueError(f"Unsupported model or no client available: {model}")

        except Exception as e:
            st.error(f"Error generating content with {model}: {str(e)}")
            raise
    # services/ai_service.py

ai_service = AIService()

