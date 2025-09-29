import requests
import json
from typing import Dict, List, Any, Optional
import streamlit as st
from config.settings import config

class SerpAPIService:
    """Service for fetching real financial data from Google search results via SerpAPI"""

    def __init__(self):
        self.api_key = config.serpapi_api_key
        self.base_url = "https://serpapi.com/search.json"
        if not self.api_key:
            st.warning("SERPAPI_API_KEY not found. Search-based content generation will not work.")


    def extract_bullet_points(self, search_results: Dict[str, Any], slide_title: str) -> List[str]:
        """Extract relevant bullet points from search results for a specific slide"""
        bullets = []
        results = search_results.get('results', [])

        # Keywords to match slide title
        slide_keywords = slide_title.lower().split()

        for result in results[:5]:  # Use top 5 results
            snippet = result.get('snippet', '')
            title = result.get('title', '')

            # Check relevance - be more lenient
            combined_text = (snippet + title).lower()
            relevance_score = sum(1 for keyword in slide_keywords if keyword in combined_text)

            # Also check for financial keywords
            financial_keywords = ['financial', 'analysis', 'performance', 'market', 'stock', 'nifty', 'report']
            financial_score = sum(1 for keyword in financial_keywords if keyword in combined_text)

            if relevance_score > 0 or financial_score > 1:
                # Extract key sentences or phrases
                sentences = snippet.split('. ')
                for sentence in sentences[:2]:  # Take first 2 sentences
                    if len(sentence.strip()) > 20:  # Meaningful length
                        # Clean and format as bullet
                        bullet = sentence.strip()
                        if not bullet.startswith('•'):
                            bullet = f"• {bullet}"
                        bullets.append(bullet)

                        if len(bullets) >= 4:  # Limit to 4 bullets per slide
                            break

            if len(bullets) >= 4:
                break

        # If not enough bullets, add generic ones based on slide title
        while len(bullets) < 3:
            if 'analysis' in slide_title.lower():
                bullets.append(f"• Comprehensive {slide_title.lower()} based on current market data")
            elif 'performance' in slide_title.lower():
                bullets.append(f"• Key performance indicators for {slide_title.lower()}")
            elif 'overview' in slide_title.lower():
                bullets.append(f"• Strategic overview of {slide_title.lower()}")
            else:
                bullets.append(f"• Industry insights for {slide_title.lower()}")
                break

        return bullets[:6]  # Max 6 bullets for more content

    def search_financial_topic(self, topic: str, num_results: int = 10) -> Dict[str, Any]:
        """Search for financial topic using SerpAPI"""
        try:
            params = {
                'engine': 'google',
                'q': f"{topic} financial analysis",
                'api_key': self.api_key,
                'num': num_results
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            results = []

            if 'organic_results' in data:
                for result in data['organic_results'][:num_results]:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', '')
                    })

            return {'results': results}

        except Exception as e:
            st.error(f"Error fetching search results: {str(e)}")
            return {'results': []}

    def search_images(self, query: str, num_results: int = 5) -> List[str]:
        """Search for images using SerpAPI"""
        try:
            params = {
                'engine': 'google_images',
                'q': query,
                'api_key': self.api_key,
                'num': num_results
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            image_urls = []

            if 'images_results' in data:
                for image in data['images_results'][:num_results]:
                    image_urls.append(image.get('original', ''))

            return image_urls

        except Exception as e:
            st.error(f"Error fetching images: {str(e)}")
            return []

    def generate_slide_content(self, topic: str, slide_titles: List[str]) -> Dict[str, Any]:
        """Generate complete slide content from search results"""
        # Search for the main topic
        search_results = self.search_financial_topic(topic)

        slides = []
        for slide_title in slide_titles:
            bullets = self.extract_bullet_points(search_results, slide_title)
            slides.append({
                'slide_number': len(slides) + 1,
                'title': slide_title,
                'content': bullets
            })

        return {
            'presentation_title': f'Financial Analysis: {topic}',
            'executive_summary': f'Comprehensive analysis of {topic} based on current market data and industry reports.',
            'slides': slides,
            'key_recommendations': [
                'Monitor key market indicators regularly',
                'Diversify investment portfolio',
                'Stay informed about industry developments',
                'Consult financial advisors for personalized advice'
            ]
        }

# Global serpapi service instance
serpapi_service = SerpAPIService()
