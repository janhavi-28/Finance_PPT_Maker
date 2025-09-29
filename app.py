import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FinancePPT AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
from datetime import datetime
import json
from services.content_generator import FinancialContentGenerator
from services.ppt_generator import ppt_generator
from services.security_manager import security_manager
from config.settings import SETTINGS



# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: #e2e8f0;
        font-size: 1.2rem;
    }
    .template-card {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .template-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    .template-card.selected {
        border-color: #10b981;
        background-color: #f0fdf4;
    }
    .success-box {
        background-color: #f0fdf4;
        border: 1px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 FinancePPT AI</h1>
        <p>Create Professional Finance Presentations with AI-Powered Content Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check environment setup
    if not security_manager.validate_environment():
        st.error("⚠️ Environment setup incomplete. Please check your .env file configuration.")
        st.info("Required environment variables: SERPAPI_API_KEY, GOOGLE_API_KEY")
        return
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### ⚙️ Presentation Settings")
        slide_count = st.slider("Number of slides", min_value=5, max_value=20, value=10, key='slide_count')
        template_key = st.selectbox(
            "Presentation Template",
            options=["financial_green", "corporate_blue", "modern_white"],
            index=0,
            key='template_key',
            help="Select a visual theme for your PPT"
        )
        include_real_data = st.checkbox("Include real data", value=True, key='include_real_data')
        
        st.markdown("---")
        st.markdown("""
        ### How it works:
        1. Enter your financial topic below (press Enter to generate)
        2. Configure settings here
        3. Auto-generates your professional PPT!
        """)
    
    # Main page topic input section below title
    st.markdown("### 💡 Give me a PPT on this topic")
    topic = st.text_area(
        "📝 Enter your presentation topic (e.g., 'Q4 Financial Analysis')",
        placeholder="Enter your presentation topic here",
        height=100,
        key='topic_input'
    )
    
    # Generate button inside prompt window (directly below text area)
    generate_btn = st.button("🚀 Generate PPT", type="primary", key='generate_btn')
    
    # Trigger generation only on button press
    if generate_btn and topic.strip() and not st.session_state.get('generating', False):
        generate_presentation(topic, slide_count, include_real_data, template_key)
    
    # Full-width results area below topic input
    if 'ppt_result' in st.session_state:
        result = st.session_state['ppt_result']
        st.success("🎉 Your professional finance presentation is ready!")
        
        # Download button - full width
        if result.get('ppt_file') and os.path.exists(result['ppt_file']):
            with open(result['ppt_file'], "rb") as file:
                st.download_button(
                    label="📥 Download PowerPoint",
                    data=file.read(),
                    file_name=os.path.basename(result['ppt_file']),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    type="primary",
                    use_container_width=True
                )
        
        # Content preview - Full width, larger layout
        with st.expander("📖 Content Preview", expanded=True):
            st.subheader(result.get('title', 'Financial Presentation'))
            st.write(result.get('summary', ''))
            
            st.subheader("Slide Structure:")
            for slide in result.get('slides', [])[:5]:  # Show first 5 slides
                col1, col2 = st.columns([4, 1])  # Wider content column (80%)
                
                with col1:
                    st.markdown(f"**{slide.get('slide_number', '')}. {slide.get('title', '')}**")
                    for point in slide.get('content', []):
                        # Strip existing bullets to avoid doubles
                        clean_point = point.lstrip("• ").lstrip("•").lstrip("- ").lstrip("-").lstrip("* ").lstrip("*").strip()
                        st.markdown(f"• {clean_point}")
                
                with col2:
                    visual = slide.get('visual_suggestion', {})
                    if 'image_url' in visual and visual['image_url']:
                        try:
                            st.image(visual['image_url'], caption=visual.get('image_description', 'Slide Image'), use_container_width=True, width=200)  # Larger image
                        except:
                            st.write("Image not available")
                    else:
                        st.write("No image for this slide")
                
                st.markdown("---")  # Separator between slides
        
        # Recommendations - full width
        if result.get('recommendations'):
            st.subheader("🎯 Key Recommendations")
            for rec in result['recommendations']:
                st.write(f"• {rec}")
    elif 'generating' in st.session_state and st.session_state.generating:
        st.info("Generating your PPT...")
    else:
        st.info("Enter a topic above - it will auto-generate when you finish typing and press Enter/move focus.")

def generate_presentation(topic, slide_count, include_real_data, template_key):
    """Generate the complete presentation"""

    st.session_state['generating'] = True
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Step 1: Generate content
        status_text.text("🔍 Fetching real data from Google search...")
        progress_bar.progress(20)

        # ✅ Create an instance before calling the method
        content_generator = FinancialContentGenerator()
        content = content_generator.generate_presentation_content(
            topic=topic,
            presentation_type="quarterly_analysis",  # Default
            target_audience="Executive Leadership",  # Default
            slide_count=slide_count,
            include_real_data=include_real_data,
            content_provider="SerpAPI"  # Always use SerpAPI
        )
        
        if not content:
            st.error("Failed to generate presentation content. Please try again.")
            return
        
        # Step 2: Create PowerPoint
        status_text.text("📊 Creating professional PowerPoint...")
        progress_bar.progress(60)
        
        # Ensure template_key is properly formatted
        formatted_template = template_key.lower().replace(" ", "_")
        ppt_bytes = ppt_generator.create_presentation(
            content=content,
            template=formatted_template
        )
        
        if not ppt_bytes:
            st.error("Failed to create PowerPoint file. Please try again.")
            return
        
        # Sanitize topic for filename (remove newlines, invalid chars, replace spaces)
        sanitized_topic = topic.strip().replace('\n', '').replace('\r', '').replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        filename = f"{sanitized_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        ppt_file = ppt_generator.save_presentation(ppt_bytes, filename)
        
        # Step 3: Complete
        status_text.text("✅ Presentation ready!")
        progress_bar.progress(100)

        # Store results in session state
        st.session_state['ppt_result'] = {
            'ppt_file': ppt_file,
            'title': content.get('presentation_title', 'Financial Presentation'),
            'summary': content.get('executive_summary', ''),
            'slides': content.get('slides', [])[:5],
            'recommendations': content.get('key_recommendations', [])
        }

        # Rerun to display results
        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your API keys and try again.")

    finally:
        st.session_state['generating'] = False
        progress_bar.empty()
        status_text.empty()

if __name__ == "__main__":
    # Initialize session state
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = None
    
    main()
