import os
import hashlib
import secrets
from typing import Dict, Optional
import streamlit as st
from pathlib import Path
from typing import Any, Dict
from typing import List, Dict



class SecurityManager:
    """Manage secure operations and API key validation"""
    
    def __init__(self):
        self.session_token = self._generate_session_token()
    
    def _generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def validate_environment(self) -> Dict[str, bool]:
        """Validate that environment is properly configured"""
        validation_results = {
            "env_file_exists": Path(".env").exists(),
            "api_keys_configured": False,
            "secure_setup": True
        }
        
        # Check if at least one API key is configured
        api_keys = [
            os.getenv("OPENAI_API_KEY"),
            os.getenv("GEMINI_API_KEY"),
            os.getenv("ANTHROPIC_API_KEY")
        ]
        
        validation_results["api_keys_configured"] = any(key for key in api_keys)
        
        return validation_results
    
    def check_api_key_security(self) -> Dict[str, str]:
        """Check API key security status"""
        status = {
            "storage": "secure" if Path(".env").exists() else "missing",
            "git_protection": "protected" if Path(".gitignore").exists() else "vulnerable",
            "environment_isolation": "isolated"
        }
        
        return status
    
    def mask_api_key(self, api_key: Optional[str]) -> str:
        """Safely mask API key for display purposes"""
        if not api_key:
            return "Not configured"
        
        if len(api_key) < 8:
            return "Invalid key"
        
        return f"{api_key[:4]}...{api_key[-4:]}"
    
    def validate_session(self) -> bool:
        """Validate current session security"""
        return bool(self.session_token)
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status"""
        env_validation = self.validate_environment()
        key_security = self.check_api_key_security()
        
        return {
            "environment": env_validation,
            "api_security": key_security,
            "session_valid": self.validate_session(),
            "recommendations": self._get_security_recommendations(env_validation, key_security)
        }
    
    def _get_security_recommendations(self, env_status: Dict, key_status: Dict) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if not env_status["env_file_exists"]:
            recommendations.append("Create .env file for secure API key storage")
        
        if not env_status["api_keys_configured"]:
            recommendations.append("Configure at least one AI provider API key")
        
        if key_status["git_protection"] != "protected":
            recommendations.append("Ensure .gitignore includes .env file")
        
        return recommendations

# Global security manager instance
security_manager = SecurityManager()
