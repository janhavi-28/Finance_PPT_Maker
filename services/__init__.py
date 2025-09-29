"""
Services package for FinancePPT AI
Contains all service modules for content generation, AI integration, and presentation creation.
"""

# Import key services for easy access
from .content_generator import FinancialContentGenerator as ContentGenerator

# or FinancialContentGenerator (whichever is the correct class name you want to expose)

from .ai_service import ai_service
from .ppt_generator import ppt_generator
from .chart_generator import chart_generator
# from .market_services import market_services

__all__ = [
    'content_generator',
    'ai_service', 
    'ppt_generator',
    'chart_generator'
]
