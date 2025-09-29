from typing import Dict, List, Any
import json
import os

class TemplateManager:
    """Manage presentation templates and themes"""
    
    def __init__(self):
        self.templates_dir = "templates"
        os.makedirs(self.templates_dir, exist_ok=True)
        
        self.available_templates = {
            "corporate_blue": {
                "name": "Corporate Blue",
                "description": "Professional corporate template with blue theme",
                "primary_color": "#1f4e79",
                "secondary_color": "#4a90e2",
                "use_case": "Executive presentations, board meetings, corporate reports"
            },
            "financial_green": {
                "name": "Financial Green", 
                "description": "Finance-focused template with green accents",
                "primary_color": "#2d5a27",
                "secondary_color": "#4caf50",
                "use_case": "Financial analysis, investment proposals, budget reviews"
            },
            "modern_orange": {
                "name": "Modern Orange",
                "description": "Modern and energetic orange-themed template", 
                "primary_color": "#e65100",
                "secondary_color": "#ff9800",
                "use_case": "Innovation presentations, startup pitches, creative projects"
            },
            "executive_dark": {
                "name": "Executive Dark",
                "description": "Sophisticated dark theme for executive presentations",
                "primary_color": "#1a1a1a",
                "secondary_color": "#4a4a4a",
                "use_case": "Board meetings, strategic reviews, high-level executive briefings"
            }
        }
        
        self.presentation_types = {
            "quarterly_analysis": {
                "name": "Quarterly Analysis",
                "description": "Comprehensive quarterly financial review",
                "recommended_slides": 10,
                "key_sections": [
                    "Executive Summary",
                    "Financial Performance", 
                    "Revenue Analysis",
                    "Profitability Review",
                    "Cash Flow Analysis",
                    "Balance Sheet Review",
                    "Market Analysis",
                    "Risk Assessment",
                    "Strategic Outlook",
                    "Recommendations"
                ]
            },
            "investment_proposal": {
                "name": "Investment Proposal",
                "description": "Investment opportunity presentation",
                "recommended_slides": 12,
                "key_sections": [
                    "Investment Overview",
                    "Market Opportunity",
                    "Financial Projections",
                    "Revenue Model",
                    "Competitive Analysis",
                    "Risk Analysis",
                    "Management Team",
                    "Financial Requirements",
                    "Expected Returns",
                    "Exit Strategy",
                    "Investment Terms",
                    "Next Steps"
                ]
            },
            "budget_planning": {
                "name": "Budget Planning",
                "description": "Annual budget planning and review",
                "recommended_slides": 8,
                "key_sections": [
                    "Budget Overview",
                    "Revenue Forecast",
                    "Expense Planning", 
                    "Capital Expenditure",
                    "Cash Flow Projection",
                    "Variance Analysis",
                    "Scenario Planning",
                    "Approval Process"
                ]
            },
            "financial_dashboard": {
                "name": "Financial Dashboard",
                "description": "KPI and metrics dashboard presentation",
                "recommended_slides": 6,
                "key_sections": [
                    "Dashboard Overview",
                    "Key Performance Indicators",
                    "Financial Metrics",
                    "Trend Analysis",
                    "Benchmarking",
                    "Action Items"
                ]
            }
        }
        
        self.target_audiences = {
            "executive_leadership": {
                "name": "Executive Leadership",
                "description": "C-suite executives and senior leadership",
                "tone": "Strategic, high-level, decision-focused",
                "detail_level": "Summary with key insights",
                "time_allocation": "10-15 minutes per presentation"
            },
            "board_of_directors": {
                "name": "Board of Directors", 
                "description": "Board members and governance stakeholders",
                "tone": "Formal, comprehensive, governance-focused",
                "detail_level": "Detailed with supporting evidence",
                "time_allocation": "15-20 minutes per presentation"
            },
            "investors": {
                "name": "Investors",
                "description": "Current and potential investors",
                "tone": "Performance-focused, transparent, opportunity-driven",
                "detail_level": "Metrics-heavy with growth projections",
                "time_allocation": "10-12 minutes per presentation"
            },
            "management_team": {
                "name": "Management Team",
                "description": "Department heads and senior managers",
                "tone": "Operational, actionable, collaborative",
                "detail_level": "Detailed with implementation focus",
                "time_allocation": "15-25 minutes per presentation"
            }
        }
    
    def get_template_info(self, template_id: str) -> Dict[str, Any]:
        """Get detailed information about a template"""
        return self.available_templates.get(template_id, {})
    
    def get_presentation_type_info(self, type_id: str) -> Dict[str, Any]:
        """Get detailed information about a presentation type"""
        return self.presentation_types.get(type_id, {})
    
    def get_audience_info(self, audience_id: str) -> Dict[str, Any]:
        """Get detailed information about target audience"""
        return self.target_audiences.get(audience_id, {})
    
    def get_recommended_template(self, presentation_type: str, audience: str) -> str:
        """Get recommended template based on presentation type and audience"""
        
        # Business logic for template recommendations
        if presentation_type == "investment_proposal":
            return "financial_green"
        elif presentation_type == "quarterly_analysis" and audience == "executive_leadership":
            return "corporate_blue"
        elif presentation_type == "budget_planning":
            return "financial_green"
        elif "innovation" in presentation_type.lower() or "startup" in presentation_type.lower():
            return "modern_orange"
        else:
            return "corporate_blue"  # Default
    
    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate presentation configuration"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Validate template
        template = config.get("template")
        if template not in self.available_templates:
            validation_result["errors"].append(f"Invalid template: {template}")
            validation_result["valid"] = False
        
        # Validate presentation type
        pres_type = config.get("presentation_type")
        if pres_type not in self.presentation_types:
            validation_result["errors"].append(f"Invalid presentation type: {pres_type}")
            validation_result["valid"] = False
        
        # Validate audience
        audience = config.get("target_audience")
        if audience not in self.target_audiences:
            validation_result["errors"].append(f"Invalid target audience: {audience}")
            validation_result["valid"] = False
        
        # Validate slide count
        slide_count = config.get("slide_count", 10)
        if slide_count < 5 or slide_count > 25:
            validation_result["warnings"].append("Slide count should be between 5-25 for optimal presentation length")
        
        # Add recommendations
        if validation_result["valid"]:
            recommended_template = self.get_recommended_template(pres_type, audience)
            if template != recommended_template:
                validation_result["recommendations"].append(
                    f"Consider using '{self.available_templates[recommended_template]['name']}' template for better alignment with your presentation type and audience"
                )
        
        return validation_result
    
    def export_template_config(self, template_id: str) -> str:
        """Export template configuration as JSON"""
        template_config = {
            "template_info": self.get_template_info(template_id),
            "compatible_types": [],
            "compatible_audiences": []
        }
        
        # Find compatible presentation types and audiences
        for type_id in self.presentation_types:
            for audience_id in self.target_audiences:
                if self.get_recommended_template(type_id, audience_id) == template_id:
                    if type_id not in template_config["compatible_types"]:
                        template_config["compatible_types"].append(type_id)
                    if audience_id not in template_config["compatible_audiences"]:
                        template_config["compatible_audiences"].append(audience_id)
        
        return json.dumps(template_config, indent=2)

# Global template manager instance
template_manager = TemplateManager()
