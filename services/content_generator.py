import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st

# Absolute imports
from services.ai_service import ai_service
from services.market_data_service import market_data_service
from services.serpapi_service import serpapi_service

class FinancialContentGenerator:
    """Advanced financial content generation with real data integration and visual suggestions"""
    
    def __init__(self):
        self.financial_templates = {
            "quarterly_analysis": {
                "slides": [
                    "Executive Summary & Key Highlights",
                    "Financial Performance Overview",
                    "Revenue Analysis & Growth Trends",
                    "Profitability & Margin Analysis",
                    "Cash Flow & Liquidity Position",
                    "Balance Sheet Strength",
                    "Market Position & Competitive Analysis",
                    "Risk Assessment & Mitigation",
                    "Strategic Initiatives & Outlook"
                ]
            },
            "investment_proposal": {
                "slides": [
                    "Investment Opportunity Overview",
                    "Market Analysis & Size",
                    "Financial Projections",
                    "Revenue Model & Assumptions",
                    "Competitive Landscape",
                    "Risk Analysis & Mitigation",
                    "Management Team & Execution",
                    "Financial Requirements",
                    "Expected Returns & Exit Strategy"
                ]
            },
            "budget_planning": {
                "slides": [
                    "Budget Overview & Objectives",
                    "Revenue Forecasting",
                    "Operating Expense Planning",
                    "Capital Expenditure Analysis",
                    "Cash Flow Projections",
                    "Variance Analysis",
                    "Scenario Planning",
                    "Resource Allocation",
                    "Performance Metrics"
                ]
            }
        }
        self.market_data_service = market_data_service

    def generate_presentation_content(self, topic: str, presentation_type: str, target_audience: str, slide_count: int, include_real_data: bool, content_provider: str) -> Dict[str, Any]:
        """Generate presentation content using SerpAPI for factual data with visual suggestions"""
        if content_provider != "SerpAPI":
            # Fallback to old AI method if needed
            return self._get_fallback_content(topic, presentation_type, target_audience, slide_count)
        
        # Use SerpAPI for real data
        search_results = serpapi_service.search_financial_topic(topic, num_results=15)
        
        # Get templates
        templates = self.financial_templates.get(presentation_type, self.financial_templates["quarterly_analysis"])
        slide_titles = templates["slides"][:slide_count]
        
        slides = []
        market_data = {}
        
        if include_real_data:
            # Get relevant market data
            symbols = self._extract_symbols_from_topic(topic)
            if symbols:
                market_data = self.market_data_service.get_comprehensive_analysis(symbols[0])  # Use first symbol
        
        for i, title in enumerate(slide_titles):
            # Search for slide-specific content
            slide_search = f"{topic} {title}"
            slide_results = serpapi_service.search_financial_topic(slide_search, num_results=5)
            
            bullets = serpapi_service.extract_bullet_points(slide_results, title)
            
            # Ensure 4-6 bullet points
            while len(bullets) < 4:
                bullets.append(f"• Additional insight on {title.lower()}")
            bullets = bullets[:6]  # Limit to max 6
            
            visual_suggestion = self._get_visual_suggestion(title, market_data, topic)
            
            # Search for relevant image
            image_query = f"{visual_suggestion['image_description']} finance {topic}"
            image_urls = serpapi_service.search_images(image_query, num_results=1)
            if image_urls:
                visual_suggestion["image_url"] = image_urls[0]
            
            slide = {
                "slide_number": i + 1,
                "title": title,
                "content": bullets,
                "visual_suggestion": visual_suggestion,
                "data_points": self._get_slide_data_points(title, market_data)
            }
            
            # Enhance with real data
            if include_real_data and market_data:
                self._enhance_slide_with_real_data(slide, title, market_data)
            
            slides.append(slide)
        
        executive_summary = f"This presentation provides a comprehensive {presentation_type} on {topic} for {target_audience}, based on current market data and industry reports from reliable sources."
        
        return {
            "presentation_title": f"{presentation_type.title()} - {topic}",
            "executive_summary": executive_summary,
            "slides": slides,
            "appendix_suggestions": self._get_appendix_suggestions(topic)
        }

    def _get_visual_suggestion(self, title: str, market_data: Dict, topic: str) -> Dict[str, Any]:
        """Suggest appropriate stock image for slide based on title and data - no charts/graphs"""
        title_lower = title.lower()

        # Map slide titles to stock image concepts (no charts, only professional stock photos)
        if 'revenue' in title_lower or 'market share' in title_lower:
            image_description = "professional stock image of business revenue growth and financial success"
        elif 'performance' in title_lower or 'growth' in title_lower:
            image_description = "professional stock image of business performance and growth trends"
        elif 'financial' in title_lower or 'projections' in title_lower:
            image_description = "professional stock image of financial planning and business projections"
        elif 'risk' in title_lower or 'volatility' in title_lower:
            image_description = "professional stock image of business risk management and strategy"
        elif 'cash flow' in title_lower:
            image_description = "professional stock image of cash flow management in business"
        elif 'profitability' in title_lower or 'margin' in title_lower:
            image_description = "professional stock image of business profitability and financial margins"
        elif 'balance sheet' in title_lower:
            image_description = "professional stock image of financial balance and business stability"
        elif 'market position' in title_lower:
            image_description = "professional stock image of market positioning and competitive business landscape"
        elif 'strategic' in title_lower or 'outlook' in title_lower:
            image_description = "professional stock image of business strategy and future outlook"
        else:
            image_description = f"professional stock image of {title_lower} in finance and business"

        # Use real market data if available to personalize
        if market_data:
            symbol = market_data.get('symbol', '')
            if symbol:
                image_description = f"professional stock image of {symbol} company in business context"

        return {
            "image_type": "stock_image",
            "image_description": image_description,
            "key_insight": f"Visual representation of {title}",
            "image_url": None  # To be populated by SerpAPI image search
        }

    def _get_slide_data_points(self, title: str, market_data: Dict) -> List[str]:
        """Get specific data points for slide"""
        data_points = []
        if market_data:
            title_lower = title.lower()
            if 'performance' in title_lower:
                if 'current_price' in market_data:
                    data_points.append(f"Current Price: ${market_data['current_price']}")
                if 'total_return' in market_data:
                    data_points.append(f"1-Year Return: {market_data['total_return']}%")
            elif 'risk' in title_lower:
                if 'volatility' in market_data:
                    data_points.append(f"Volatility: {market_data['volatility']}%")
                if 'max_drawdown' in market_data:
                    data_points.append(f"Max Drawdown: {market_data['max_drawdown']}%")
        return data_points


    def _enhance_slide_with_real_data(self, slide: Dict, title: str, market_data: Dict):
        """Enhance slide content with real market data"""
        title_lower = title.lower()
        if 'overview' in title_lower or 'summary' in title_lower:
            if 'current_price' in market_data:
                slide['content'].insert(0, f"Current Market Price: ${market_data['current_price']}")
        elif 'growth' in title_lower:
            if 'total_return' in market_data:
                slide['content'].append(f"Growth Rate: {market_data['total_return']}% YTD")

    def _extract_symbols_from_topic(self, topic: str) -> List[str]:
        """Extract stock symbols from topic"""
        # Simple extraction - improve with regex for production
        common_symbols = ['NIFTY', 'SENSEX', 'AAPL', 'GOOGL', 'MSFT', 'TSLA']
        for symbol in common_symbols:
            if symbol in topic.upper():
                return [symbol]
        return []

    def _get_recommendations(self, topic: str, market_data: Dict) -> List[str]:
        """Generate key recommendations"""
        recommendations = [
            "Monitor key market indicators regularly",
            "Diversify investment portfolio based on risk profile",
            "Stay informed about regulatory changes",
            "Review performance quarterly against benchmarks"
        ]
        if market_data and 'volatility' in market_data:
            if market_data['volatility'] > 20:
                recommendations.insert(0, "Consider risk mitigation strategies due to high volatility")
        return recommendations

    def _get_appendix_suggestions(self, topic: str) -> List[str]:
        """Get appendix suggestions"""
        return [
            "Detailed financial models and assumptions",
            "Supporting market research and data sources",
            "Risk assessment matrices and scenario analysis",
            "Competitive benchmarking and industry comparisons",
            "Regulatory compliance and legal considerations"
        ]

    def _get_fallback_content(self, topic: str, presentation_type: str, target_audience: str, slide_count: int) -> Dict[str, Any]:
        """Provide fallback content when generation fails"""
        slides = []
        templates = self.financial_templates.get(presentation_type, self.financial_templates["quarterly_analysis"])
        slide_titles = templates["slides"][:slide_count]

        for i, title in enumerate(slide_titles, 1):
            slides.append({
                "slide_number": i,
                "title": title,
                "content": [
                    f"Key point 1 for {title}",
                    f"Key point 2 for {title}",
                    f"Key point 3 for {title}"
                ],
                "visual_suggestion": {"chart_type": "bar", "data_description": "Sample data"},
                "data_points": []
            })

        return {
            "presentation_title": f"Financial Presentation: {topic}",
            "executive_summary": f"This presentation covers {topic} for {target_audience}.",
            "slides": slides,
            "key_recommendations": ["Conduct further analysis", "Monitor key metrics", "Implement recommendations"],
            "appendix_suggestions": ["Additional data", "Supporting documents"]
        }

    def _parse_text_response(self, response: str, topic: str, slides: List[str]) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails"""
        # Simple fallback parsing
        return self._get_fallback_content(topic, "quarterly_analysis", "General", len(slides))

    def _get_fallback_ai_response(self) -> str:
        """Fallback AI response"""
        return json.dumps(self._get_fallback_content("General Topic", "quarterly_analysis", "General", 5))

# Global content generator instance
content_generator = FinancialContentGenerator()
