import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import io
import base64

class FinancialChartGenerator:
    """Generate professional financial charts and visualizations"""
    
    def __init__(self):
        self.color_schemes = {
            "corporate_blue": {
                "primary": "#1f4e79",
                "secondary": "#4a90e2",
                "accent": "#7bb3f0",
                "success": "#28a745",
                "warning": "#ffc107",
                "danger": "#dc3545"
            },
            "financial_green": {
                "primary": "#2d5a27",
                "secondary": "#4caf50",
                "accent": "#81c784",
                "success": "#66bb6a",
                "warning": "#ff9800",
                "danger": "#f44336"
            },
            "modern_orange": {
                "primary": "#e65100",
                "secondary": "#ff9800",
                "accent": "#ffb74d",
                "success": "#4caf50",
                "warning": "#ffc107",
                "danger": "#f44336"
            }
        }
    
    def create_revenue_trend_chart(self, 
                                 data: Dict[str, List], 
                                 template: str = "corporate_blue") -> str:
        """Create a professional revenue trend chart"""
        
        colors = self.color_schemes[template]
        
        fig = go.Figure()
        
        # Add revenue line
        fig.add_trace(go.Scatter(
            x=data.get("periods", ["Q1", "Q2", "Q3", "Q4"]),
            y=data.get("revenue", [100, 120, 135, 150]),
            mode='lines+markers',
            name='Revenue',
            line=dict(color=colors["primary"], width=3),
            marker=dict(size=8, color=colors["primary"])
        ))
        
        # Add target line if provided
        if "target" in data:
            fig.add_trace(go.Scatter(
                x=data["periods"],
                y=data["target"],
                mode='lines',
                name='Target',
                line=dict(color=colors["secondary"], width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=dict(
                text="Revenue Trend Analysis",
                font=dict(size=20, color=colors["primary"]),
                x=0.5
            ),
            xaxis_title="Period",
            yaxis_title="Revenue ($M)",
            template="plotly_white",
            showlegend=True,
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return self._fig_to_base64(fig)
    
    def create_profitability_chart(self, 
                                 data: Dict[str, List], 
                                 template: str = "corporate_blue") -> str:
        """Create a profitability analysis chart"""
        
        colors = self.color_schemes[template]
        
        fig = go.Figure()
        
        # Add multiple profitability metrics
        metrics = ["Gross Margin", "Operating Margin", "Net Margin"]
        metric_colors = [colors["primary"], colors["secondary"], colors["accent"]]
        
        for i, metric in enumerate(metrics):
            fig.add_trace(go.Bar(
                x=data.get("periods", ["Q1", "Q2", "Q3", "Q4"]),
                y=data.get(metric.lower().replace(" ", "_"), [25, 28, 30, 32]),
                name=metric,
                marker_color=metric_colors[i]
            ))
        
        fig.update_layout(
            title=dict(
                text="Profitability Analysis",
                font=dict(size=20, color=colors["primary"]),
                x=0.5
            ),
            xaxis_title="Period",
            yaxis_title="Margin (%)",
            template="plotly_white",
            barmode='group',
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return self._fig_to_base64(fig)
    
    def create_cash_flow_waterfall(self, 
                                 data: Dict[str, Any], 
                                 template: str = "corporate_blue") -> str:
        """Create a cash flow waterfall chart"""
        
        colors = self.color_schemes[template]
        
        categories = data.get("categories", [
            "Starting Cash", "Operating CF", "Investing CF", 
            "Financing CF", "Ending Cash"
        ])
        values = data.get("values", [100, 50, -20, -10, 120])
        
        # Calculate cumulative values for waterfall
        cumulative = [values[0]]
        for i in range(1, len(values)-1):
            cumulative.append(cumulative[-1] + values[i])
        cumulative.append(sum(values[:-1]) + values[0])
        
        fig = go.Figure()
        
        # Add waterfall bars
        for i, (cat, val) in enumerate(zip(categories, values)):
            color = colors["success"] if val > 0 else colors["danger"]
            if i == 0 or i == len(categories)-1:
                color = colors["primary"]
            
            fig.add_trace(go.Bar(
                x=[cat],
                y=[abs(val)],
                name=cat,
                marker_color=color,
                showlegend=False
            ))
        
        fig.update_layout(
            title=dict(
                text="Cash Flow Analysis",
                font=dict(size=20, color=colors["primary"]),
                x=0.5
            ),
            xaxis_title="Cash Flow Components",
            yaxis_title="Amount ($M)",
            template="plotly_white",
            height=400,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        return self._fig_to_base64(fig)
    
    def create_kpi_dashboard(self, 
                           kpis: Dict[str, Dict], 
                           template: str = "corporate_blue") -> str:
        """Create a KPI dashboard visualization"""
        
        colors = self.color_schemes[template]
        
        fig = go.Figure()
        
        # Create gauge charts for each KPI
        kpi_names = list(kpis.keys())[:4]  # Limit to 4 KPIs
        
        for i, kpi_name in enumerate(kpi_names):
            kpi_data = kpis[kpi_name]
            
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=kpi_data.get("current", 75),
                domain={'x': [i*0.25, (i+1)*0.25], 'y': [0, 1]},
                title={'text': kpi_name},
                delta={'reference': kpi_data.get("target", 80)},
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
                        'value': kpi_data.get("target", 80)
                    }
                }
            ))
        
        fig.update_layout(
            title=dict(
                text="Key Performance Indicators",
                font=dict(size=20, color=colors["primary"]),
                x=0.5
            ),
            height=300,
            font=dict(family="Arial, sans-serif", size=10)
        )
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert plotly figure to base64 string for embedding"""
        img_bytes = fig.to_image(format="png", width=800, height=400)
        img_base64 = base64.b64encode(img_bytes).decode()
        return f"data:image/png;base64,{img_base64}"
    
    def generate_sample_data(self, chart_type: str) -> Dict[str, Any]:
        """Generate sample financial data for demonstration"""
        
        if chart_type == "revenue_trend":
            return {
                "periods": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
                "revenue": [125, 142, 158, 175],
                "target": [130, 145, 160, 180]
            }
        
        elif chart_type == "profitability":
            return {
                "periods": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
                "gross_margin": [35, 37, 39, 41],
                "operating_margin": [18, 20, 22, 24],
                "net_margin": [12, 14, 16, 18]
            }
        
        elif chart_type == "cash_flow":
            return {
                "categories": ["Starting Cash", "Operating CF", "Investing CF", "Financing CF", "Ending Cash"],
                "values": [100, 75, -25, -15, 135]
            }
        
        elif chart_type == "kpis":
            return {
                "ROE": {"current": 85, "target": 90},
                "ROA": {"current": 72, "target": 75},
                "Debt Ratio": {"current": 45, "target": 40},
                "Current Ratio": {"current": 88, "target": 85}
            }
        
        return {}

# Global chart generator instance
chart_generator = FinancialChartGenerator()
