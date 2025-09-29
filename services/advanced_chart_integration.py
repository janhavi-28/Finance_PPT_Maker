import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import io
import base64
from PIL import Image
import yfinance as yf
from datetime import datetime, timedelta

class GammaAIStyleChartGenerator:
    """Advanced chart generation with Gamma AI-level sophistication"""
    
    def __init__(self):
        self.gamma_color_palettes = {
            "corporate_blue": {
                "primary": "#1f4e79",
                "secondary": "#4a90e2", 
                "accent": "#7bb3f0",
                "gradient": ["#1f4e79", "#4a90e2", "#7bb3f0", "#a8d0f7"],
                "success": "#28a745",
                "warning": "#ffc107",
                "danger": "#dc3545",
                "neutral": "#6c757d"
            },
            "financial_green": {
                "primary": "#2d5a27",
                "secondary": "#4caf50",
                "accent": "#81c784", 
                "gradient": ["#2d5a27", "#4caf50", "#81c784", "#c8e6c9"],
                "success": "#66bb6a",
                "warning": "#ff9800",
                "danger": "#f44336",
                "neutral": "#757575"
            },
            "modern_orange": {
                "primary": "#e65100",
                "secondary": "#ff9800",
                "accent": "#ffb74d",
                "gradient": ["#e65100", "#ff9800", "#ffb74d", "#ffe0b2"],
                "success": "#4caf50",
                "warning": "#ffc107", 
                "danger": "#f44336",
                "neutral": "#616161"
            }
        }
    
    def create_executive_dashboard(self, 
                                 financial_data: Dict[str, Any], 
                                 template: str = "corporate_blue") -> str:
        """Create a comprehensive executive dashboard with multiple KPIs"""
        
        colors = self.gamma_color_palettes[template]
        
        # Create subplot layout (2x2 grid)
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Revenue Growth", "Profitability Trends", "Cash Flow", "Key Metrics"),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "waterfall"}, {"type": "indicator"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Revenue Growth (Top Left)
        periods = financial_data.get("periods", ["Q1", "Q2", "Q3", "Q4"])
        revenue = financial_data.get("revenue", [100, 120, 135, 150])
        target = financial_data.get("revenue_target", [110, 125, 140, 155])
        
        fig.add_trace(
            go.Scatter(x=periods, y=revenue, name="Actual Revenue", 
                      line=dict(color=colors["primary"], width=4),
                      marker=dict(size=10, color=colors["primary"])),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=periods, y=target, name="Target", 
                      line=dict(color=colors["secondary"], width=3, dash="dash")),
            row=1, col=1
        )
        
        # Profitability Trends (Top Right)
        margins = ["Gross", "Operating", "Net"]
        q1_margins = [35, 18, 12]
        q4_margins = [41, 24, 18]
        
        fig.add_trace(
            go.Bar(x=margins, y=q1_margins, name="Q1", 
                  marker_color=colors["accent"], opacity=0.7),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=margins, y=q4_margins, name="Q4", 
                  marker_color=colors["primary"]),
            row=1, col=2
        )
        
        # Cash Flow Waterfall (Bottom Left)
        cash_categories = ["Starting", "Operating", "Investing", "Financing", "Ending"]
        cash_values = [100, 50, -20, -10, 120]
        
        fig.add_trace(
            go.Waterfall(
                x=cash_categories,
                y=cash_values,
                connector={"line": {"color": colors["neutral"]}},
                increasing={"marker": {"color": colors["success"]}},
                decreasing={"marker": {"color": colors["danger"]}},
                totals={"marker": {"color": colors["primary"]}},
                name="Cash Flow"
            ),
            row=2, col=1
        )
        
        # Key Metrics Gauge (Bottom Right)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=85,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': colors["primary"]},
                    'steps': [
                        {'range': [0, 50], 'color': colors["danger"]},
                        {'range': [50, 80], 'color': colors["warning"]},
                        {'range': [80, 100], 'color': colors["success"]}
                    ],
                    'threshold': {
                        'line': {'color': colors["secondary"], 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=2, col=2
        )
        
        # Update layout with professional styling
        fig.update_layout(
            title=dict(
                text="Executive Financial Dashboard",
                font=dict(size=24, color=colors["primary"], family="Arial Black"),
                x=0.5,
                y=0.95
            ),
            template="plotly_white",
            showlegend=True,
            height=600,
            width=1200,
            font=dict(family="Arial, sans-serif", size=12),
            paper_bgcolor="white",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return self._fig_to_high_quality_base64(fig)
    
    def create_market_analysis_chart(self, 
                                   market_data: Dict[str, Any], 
                                   template: str = "corporate_blue") -> str:
        """Create sophisticated market analysis visualization"""
        
        colors = self.gamma_color_palettes[template]
        
        # Create dual-axis chart
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Market Performance vs Benchmarks", "Volume & Volatility Analysis"),
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
            vertical_spacing=0.15
        )
        
        # Sample market data (in real implementation, this would come from yfinance)
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="M")
        market_performance = np.cumsum(np.random.normal(0.01, 0.05, len(dates))) * 100
        benchmark = np.cumsum(np.random.normal(0.008, 0.04, len(dates))) * 100
        volume = np.random.normal(1000000, 200000, len(dates))
        volatility = np.random.normal(0.15, 0.05, len(dates))
        
        # Market Performance (Top)
        fig.add_trace(
            go.Scatter(x=dates, y=market_performance, name="Portfolio", 
                      line=dict(color=colors["primary"], width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=dates, y=benchmark, name="S&P 500", 
                      line=dict(color=colors["secondary"], width=2)),
            row=1, col=1
        )
        
        # Volume (Bottom)
        fig.add_trace(
            go.Bar(x=dates, y=volume, name="Volume", 
                  marker_color=colors["accent"], opacity=0.6),
            row=2, col=1
        )
        
        # Volatility (Bottom, secondary y-axis)
        fig.add_trace(
            go.Scatter(x=dates, y=volatility, name="Volatility", 
                      line=dict(color=colors["danger"], width=2)),
            row=2, col=1, secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="Comprehensive Market Analysis",
                font=dict(size=22, color=colors["primary"], family="Arial Black"),
                x=0.5
            ),
            template="plotly_white",
            height=500,
            width=1000,
            showlegend=True,
            font=dict(family="Arial, sans-serif", size=11)
        )
        
        # Update y-axes labels
        fig.update_yaxes(title_text="Performance (%)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="Volatility", row=2, col=1, secondary_y=True)
        
        return self._fig_to_high_quality_base64(fig)
    
    def create_financial_projections_chart(self, 
                                         projection_data: Dict[str, Any], 
                                         template: str = "corporate_blue") -> str:
        """Create forward-looking financial projections with confidence intervals"""
        
        colors = self.gamma_color_palettes[template]
        
        fig = go.Figure()
        
        # Historical and projected periods
        historical_periods = ["2021", "2022", "2023"]
        projected_periods = ["2024", "2025", "2026"]
        all_periods = historical_periods + projected_periods
        
        # Revenue projections with confidence intervals
        historical_revenue = [100, 115, 132]
        projected_revenue = [150, 172, 198]
        all_revenue = historical_revenue + projected_revenue
        
        # Confidence intervals for projections
        upper_bound = projected_revenue + np.array([10, 20, 35])
        lower_bound = projected_revenue - np.array([8, 15, 25])
        
        # Historical data (solid line)
        fig.add_trace(go.Scatter(
            x=historical_periods, 
            y=historical_revenue,
            mode='lines+markers',
            name='Historical Revenue',
            line=dict(color=colors["primary"], width=4),
            marker=dict(size=10, color=colors["primary"])
        ))
        
        # Projected data (dashed line)
        fig.add_trace(go.Scatter(
            x=projected_periods, 
            y=projected_revenue,
            mode='lines+markers',
            name='Projected Revenue',
            line=dict(color=colors["secondary"], width=4, dash='dash'),
            marker=dict(size=10, color=colors["secondary"])
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=projected_periods + projected_periods[::-1],
            y=list(upper_bound) + list(lower_bound[::-1]),
            fill='toself',
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors['accent'][1:])) + [0.3])}",
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval',
            showlegend=True
        ))
        
        # Add scenario lines
        optimistic = np.array(projected_revenue) * 1.15
        pessimistic = np.array(projected_revenue) * 0.85
        
        fig.add_trace(go.Scatter(
            x=projected_periods, y=optimistic,
            mode='lines', name='Optimistic Scenario',
            line=dict(color=colors["success"], width=2, dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=projected_periods, y=pessimistic,
            mode='lines', name='Conservative Scenario',
            line=dict(color=colors["warning"], width=2, dash='dot')
        ))
        
        # Add vertical line to separate historical from projected
        fig.add_vline(
            x=2.5, line_width=2, line_dash="dash", 
            line_color=colors["neutral"],
            annotation_text="Projection Start"
        )
        
        fig.update_layout(
            title=dict(
                text="Revenue Projections with Scenario Analysis",
                font=dict(size=20, color=colors["primary"], family="Arial Black"),
                x=0.5
            ),
            xaxis_title="Year",
            yaxis_title="Revenue ($M)",
            template="plotly_white",
            height=400,
            width=800,
            showlegend=True,
            font=dict(family="Arial, sans-serif", size=12),
            hovermode='x unified'
        )
        
        return self._fig_to_high_quality_base64(fig)
    
    def create_competitive_analysis_radar(self, 
                                        competitive_data: Dict[str, Any], 
                                        template: str = "corporate_blue") -> str:
        """Create radar chart for competitive analysis"""
        
        colors = self.gamma_color_palettes[template]
        
        fig = go.Figure()
        
        # Competitive metrics
        categories = ['Market Share', 'Innovation', 'Financial Strength', 
                     'Customer Satisfaction', 'Operational Efficiency', 'Brand Value']
        
        # Company vs competitors data
        our_company = [85, 78, 92, 88, 82, 75]
        competitor_1 = [75, 85, 88, 82, 78, 85]
        competitor_2 = [68, 72, 85, 75, 88, 78]
        
        fig.add_trace(go.Scatterpolar(
            r=our_company,
            theta=categories,
            fill='toself',
            name='Our Company',
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors['primary'][1:])) + [0.4])}",
            line=dict(color=colors["primary"], width=3)
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=competitor_1,
            theta=categories,
            fill='toself',
            name='Competitor A',
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors['secondary'][1:])) + [0.3])}",
            line=dict(color=colors["secondary"], width=2)
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=competitor_2,
            theta=categories,
            fill='toself',
            name='Competitor B',
            fillcolor=f"rgba{tuple(list(bytes.fromhex(colors['accent'][1:])) + [0.3])}",
            line=dict(color=colors["accent"], width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor=colors["neutral"]
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color=colors["primary"])
                )
            ),
            title=dict(
                text="Competitive Analysis Matrix",
                font=dict(size=20, color=colors["primary"], family="Arial Black"),
                x=0.5
            ),
            showlegend=True,
            height=500,
            width=600,
            font=dict(family="Arial, sans-serif", size=11)
        )
        
        return self._fig_to_high_quality_base64(fig)
    
    def _fig_to_high_quality_base64(self, fig) -> str:
        """Convert plotly figure to high-quality base64 string"""
        # Export at high resolution for professional presentations
        img_bytes = fig.to_image(
            format="png", 
            width=1200, 
            height=600, 
            scale=2  # High DPI for crisp images
        )
        img_base64 = base64.b64encode(img_bytes).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def generate_chart_suggestions(self, slide_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent chart suggestions based on slide content"""
        
        title = slide_content.get("title", "").lower()
        content = " ".join(slide_content.get("content", [])).lower()
        
        # AI-powered chart type selection
        if any(word in title + content for word in ["trend", "growth", "over time", "historical"]):
            return {
                "chart_type": "line",
                "suggested_function": "create_financial_projections_chart",
                "data_description": "Time series analysis with trend lines and projections",
                "key_insight": "Shows growth trajectory and future outlook"
            }
        
        elif any(word in title + content for word in ["comparison", "vs", "versus", "competitive"]):
            return {
                "chart_type": "radar",
                "suggested_function": "create_competitive_analysis_radar", 
                "data_description": "Multi-dimensional competitive comparison",
                "key_insight": "Reveals competitive strengths and opportunities"
            }
        
        elif any(word in title + content for word in ["dashboard", "overview", "summary", "kpi"]):
            return {
                "chart_type": "dashboard",
                "suggested_function": "create_executive_dashboard",
                "data_description": "Comprehensive KPI dashboard with multiple metrics",
                "key_insight": "Provides holistic view of business performance"
            }
        
        elif any(word in title + content for word in ["market", "performance", "analysis"]):
            return {
                "chart_type": "market_analysis",
                "suggested_function": "create_market_analysis_chart",
                "data_description": "Market performance with volume and volatility analysis", 
                "key_insight": "Shows market context and performance drivers"
            }
        
        else:
            return {
                "chart_type": "bar",
                "suggested_function": "create_executive_dashboard",
                "data_description": "Professional bar chart with comparative analysis",
                "key_insight": "Clear comparison of key metrics"
            }

# Global advanced chart generator instance
advanced_chart_generator = GammaAIStyleChartGenerator()
