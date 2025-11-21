"""Streamlit web application for AI Museum Curator."""
import streamlit as st
import json
from datetime import datetime
from orchestrator import ExhibitionOrchestrator
from agents.memory_bank_agent import MemoryBankAgent
from tools.knowledge_graph import KnowledgeGraphGenerator
from tools.ai_docent import AIDocent
from tools.safe_3d_viz import create_timeline_3d, create_concept_network_3d, create_room_flow_3d
import config
import base64

# Page configuration
st.set_page_config(
    page_title="MuseVerse - AI Museum Curator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main theme colors - Modern & Readable */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #3B82F6;
        --background-color: #F8FAFC;
        --text-color: #1E293B;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    
    .main-header h1 .icon {
        color: white;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    .main-header h1 .gradient-text {
        background: linear-gradient(135deg, 
            #FFD700 0%,
            #FFA500 25%,
            #FF6B6B 50%,
            #4ECDC4 75%,
            #45B7D1 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        animation: gradient-shift 8s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
        color: white !important;
    }
    
    /* Room card styling */
    .room-card {
        background: linear-gradient(to bottom, #EFF6FF, #DBEAFE);
        border-left: 5px solid #1E3A8A;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .room-title {
        color: #1E3A8A;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Exhibit card styling */
    .exhibit-card {
        background: white;
        border: 2px solid #3B82F6;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 6px;
        box-shadow: 0 2px 3px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    
    .exhibit-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .exhibit-title {
        color: #1E3A8A;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    /* FORCE LIGHT MODE AND READABLE TEXT */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* Style navbar with light theme */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 2px solid #3B82F6 !important;
    }
    
    .stApp > header {
        background-color: #FFFFFF !important;
    }
    
    /* Style toolbar */
    [data-testid="stToolbar"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Style toolbar buttons */
    [data-testid="stToolbar"] button {
        color: #1E3A8A !important;
    }
    
    [data-testid="stToolbar"] button:hover {
        background-color: #EFF6FF !important;
    }
    
    /* Fix any remaining black bars */
    .css-18e3th9, .css-1dp5vir {
        background-color: #FFFFFF !important;
    }
    
    /* Fix dropdown menu */
    [data-testid="stHeaderActionElements"] button {
        color: #000000 !important;
    }
    
    /* Fix menu dropdown background */
    [role="menu"], [role="menuitem"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Fix menu items */
    [data-testid="stMainMenu"] {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stMainMenu"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Fix all menu text */
    [data-testid="stMainMenu"] * {
        color: #000000 !important;
    }
    
    /* Fix popover/dropdown */
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1gulkj5 {
        background-color: #FFFFFF !important;
    }
    
    /* Fix menu container */
    [data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }
    
    [data-baseweb="popover"] * {
        color: #000000 !important;
    }
    
    /* Style the hamburger menu with light theme */
    #MainMenu {
        visibility: visible !important;
    }
    
    button[kind="header"] {
        display: block !important;
        color: #1E3A8A !important;
    }
    
    /* Alternative: Force light theme on menu if visible */
    [data-testid="stMainMenuPopover"] {
        background: #FFFFFF !important;
    }
    
    [data-testid="stMainMenuPopover"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Force all menu buttons to be light */
    button[data-testid="baseButton-header"] {
        color: #000000 !important;
    }
    
    /* Fix ALL text to be dark and readable */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    .stMarkdown li, .stMarkdown strong, .stMarkdown em {
        color: #000000 !important;
    }
    
    /* Ensure all text is dark and readable */
    body, p, div, span, li, td, th, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Fix expander styling - FORCE LIGHT THEME */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 12px 16px !important;
    }
    
    .streamlit-expanderHeader p, .streamlit-expanderHeader span, .streamlit-expanderHeader div {
        color: #000000 !important;
    }
    
    /* Fix expander content background */
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid #DBEAFE !important;
        border-radius: 0 0 8px 8px !important;
        padding: 16px !important;
    }
    
    /* Fix all expander text - FORCE BLACK */
    .streamlit-expanderContent *,
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent li {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    /* Fix expander container */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 8px !important;
        margin: 8px 0 !important;
        overflow: hidden !important;
    }
    
    /* Fix expander arrow/icon */
    .streamlit-expanderHeader svg {
        color: #1E3A8A !important;
    }
    
    /* Override any dark backgrounds in expanders */
    details summary {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
        color: #000000 !important;
    }
    
    details[open] summary {
        background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%) !important;
    }
    
    /* Fix the black bar issue */
    .st-emotion-cache-p5msec, .st-emotion-cache-16idsys {
        background-color: transparent !important;
    }
    
    /* Force all expander elements to have light background */
    [data-testid="stExpander"] > div {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stExpander"] > div > div {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
    }
    
    /* Fix tab text */
    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] p {
        color: #000000 !important;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1E3A8A !important;
        font-weight: 700;
        border-bottom: 2px solid #1E3A8A !important;
    }
    
    /* Fix sidebar - force light background and dark text */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
    }
    
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    .css-1d391kg,
    .css-1d391kg p {
        color: #000000 !important;
    }
    
    /* Fix sidebar markdown */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #000000 !important;
    }
    
    /* Fix all streamlit text elements */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] div,
    [data-testid="stMarkdownContainer"] span {
        color: #000000 !important;
    }
    
    /* Fix metric text */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    /* Style main buttons with gradient */
    .stButton button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Style sidebar buttons (recent exhibitions) */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        width: 100% !important;
        text-align: left !important;
        margin: 4px 0 !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%) !important;
        transform: translateX(4px) !important;
    }
    
    /* Style download buttons */
    .stDownloadButton button {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
    }
    
    .stDownloadButton button:before {
        content: "📥 ";
    }
    
    /* Style text input with gradient */
    .stTextInput input {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
        color: #000000 !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus {
        border-color: #1E3A8A !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Fix all paragraph text */
    p, span, div {
        color: #000000 !important;
    }
    
    /* Fix any dark containers */
    .element-container, .stMarkdown, [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }
    
    /* Force white background on content areas */
    .main .block-container {
        background-color: #FFFFFF !important;
    }
    
    /* Fix code blocks if any */
    code, pre {
        background-color: #F8FAFC !important;
        color: #000000 !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white !important;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Timeline styling */
    .timeline-event {
        border-left: 3px solid #D4AF37;
        padding-left: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .timeline-event::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 0;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #D4AF37;
        border: 3px solid white;
    }
    
    .timeline-year {
        color: #5D2E0F;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .timeline-event p {
        color: #2C1810 !important;

    
    /* Curator notes styling */
    .curator-notes {
        background: linear-gradient(to right, #EFF6FF, #DBEAFE);
        border: 2px solid #3B82F6;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        font-style: italic;
        line-height: 1.8;
        color: #1E293B !important;
    }
    
    .curator-notes p {
        color: #1E293B !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 6px;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Success rate indicator */
    .success-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .success-high {
        background: #4CAF50;
        color: white;
    }
    
    .success-medium {
        background: #FFC107;
        color: #333;
    }
    
    .success-low {
        background: #F44336;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = ExhibitionOrchestrator()
if 'current_exhibition' not in st.session_state:
    st.session_state.current_exhibition = None
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'knowledge_graph_gen' not in st.session_state:
    st.session_state.knowledge_graph_gen = KnowledgeGraphGenerator()
if 'ai_docent' not in st.session_state:
    st.session_state.ai_docent = AIDocent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def display_header():
    """Display main header."""
    st.markdown("""
    <div class="main-header">
        <h1><span class="icon">🏛️</span> <span class="gradient-text">MuseVerse</span></h1>
        <p>An AI Museum Curator</p>
    </div>
    """, unsafe_allow_html=True)

def display_generated_image(image_data: dict, caption: str = "Generated Image"):
    """Display AI-generated image with metadata."""
    if isinstance(image_data, dict):
        status = image_data.get('status', 'unknown')
        
        if status == 'placeholder_generated':
            # Show placeholder image
            placeholder_url = image_data.get('placeholder_url', '')
            if placeholder_url:
                st.image(placeholder_url, caption=f"🎨 {caption}", use_column_width=True)
            
            enhanced_desc = image_data.get('enhanced_description', '')
            if enhanced_desc:
                with st.expander("📝 View AI Image Description"):
                    st.write(enhanced_desc)
            
            st.caption("💡 Placeholder image shown. Connect to Imagen/DALL-E for actual AI-generated images")
        
        elif status == 'description_generated':
            # Show enhanced description only
            st.info("🎨 **AI Image Description Generated**")
            st.markdown(f"**{caption}**")
            
            enhanced_desc = image_data.get('enhanced_description', '')
            if enhanced_desc:
                with st.expander("View Image Description"):
                    st.write(enhanced_desc)
            
            st.caption("💡 Connect to Imagen or DALL-E API to generate actual images")
        
        elif status == 'error':
            st.warning(f"⚠️ Image generation error: {image_data.get('error', 'Unknown error')}")
        
        else:
            # If it's an actual image URL or path
            if 'url' in image_data:
                st.image(image_data['url'], caption=caption, use_column_width=True)
            elif 'path' in image_data:
                st.image(image_data['path'], caption=caption, use_column_width=True)
            elif 'placeholder_url' in image_data:
                st.image(image_data['placeholder_url'], caption=caption, use_column_width=True)
    elif isinstance(image_data, str):
        # Direct URL or path
        st.image(image_data, caption=caption, use_column_width=True)

def display_metrics(metrics: dict):
    """Display metrics in a beautiful layout."""
    st.markdown("### 📊 Exhibition Metrics")
    
    cols = st.columns(5)
    
    with cols[0]:
        score = metrics.get('overall_quality_score', 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Quality Score</div>
            <div class="metric-value">{score:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        rate = metrics.get('agent_success_rate', 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Success Rate</div>
            <div class="metric-value">{rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        narrative = metrics.get('narrative_quality', 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Narrative</div>
            <div class="metric-value">{narrative:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        factual = metrics.get('factual_quality', 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Factual</div>
            <div class="metric-value">{factual:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        sensitivity = metrics.get('cultural_sensitivity', 0) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sensitivity</div>
            <div class="metric-value">{sensitivity:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

def display_exhibition(exhibition: dict):
    """Display exhibition in beautiful format."""
    st.markdown(f"## {exhibition.get('title', exhibition.get('topic', 'Exhibition'))}")
    
    # Exhibition Poster (NEW!)
    if exhibition.get('poster_image'):
        st.markdown("### 🎨 Exhibition Poster")
        display_generated_image(exhibition['poster_image'], "Exhibition Poster")
        st.markdown("---")
    
    # Overview
    if exhibition.get('overview'):
        st.markdown(f"**{exhibition['overview']}**")
    
    st.markdown("---")
    
    # Curator Notes
    if exhibition.get('curator_notes'):
        st.markdown("### 📜 Curator's Notes")
        st.markdown(f"""
        <div class="curator-notes">
            {exhibition['curator_notes']}
        </div>
        """, unsafe_allow_html=True)
    
    # Rooms
    st.markdown("### 🚪 Exhibition Rooms")
    
    for i, room in enumerate(exhibition.get('rooms', []), 1):
        st.markdown(f"""
        <div class="room-card">
            <div class="room-title">Room {i}: {room.get('title', 'Untitled')}</div>
            <p><strong>Theme:</strong> {room.get('theme', 'N/A')}</p>
            <p>{room.get('description', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Room entrance image (NEW!)
        if room.get('entrance_image'):
            display_generated_image(room['entrance_image'], f"Room {i} Entrance")
        
        # Room narrative
        if room.get('narrative'):
            st.markdown(f"*{room['narrative']}*")
        
        # Exhibits in this room
        for j, exhibit in enumerate(room.get('exhibits', []), 1):
            with st.expander(f"🎨 Exhibit {j}: {exhibit.get('name', 'Untitled')}"):
                # Generated image (NEW!)
                if exhibit.get('generated_image'):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        display_generated_image(exhibit['generated_image'], exhibit.get('name', 'Exhibit'))
                    with col2:
                        st.markdown(f"""
                        <div class="exhibit-card">
                            <div class="exhibit-title">{exhibit.get('name', 'Untitled')}</div>
                            <p><strong>Time Period:</strong> {exhibit.get('time_period', 'Unknown')}</p>
                            <p>{exhibit.get('description', '')}</p>
                            
                            <p><strong>Cultural Significance:</strong></p>
                            <p>{exhibit.get('cultural_significance', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="exhibit-card">
                        <div class="exhibit-title">{exhibit.get('name', 'Untitled')}</div>
                        <p><strong>Time Period:</strong> {exhibit.get('time_period', 'Unknown')}</p>
                        <p>{exhibit.get('description', '')}</p>
                        
                        <p><strong>Cultural Significance:</strong></p>
                        <p>{exhibit.get('cultural_significance', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Facts
                if exhibit.get('facts'):
                    st.markdown("**Interesting Facts:**")
                    for fact in exhibit['facts']:
                        st.markdown(f"- {fact}")
                
                # Visual references
                if exhibit.get('visual_refs'):
                    st.markdown("**Visual References:**")
                    for ref in exhibit['visual_refs'][:3]:
                        if isinstance(ref, dict):
                            st.markdown(f"- {ref.get('description', 'Visual reference')}")
                        else:
                            st.markdown(f"- {ref}")
    
    # Timeline
    if exhibition.get('timeline'):
        st.markdown("### ⏳ Timeline")
        for event in exhibition['timeline']:
            st.markdown(f"""
            <div class="timeline-event">
                <div class="timeline-year">{event.get('year', 'Unknown')}</div>
                <p><strong>{event.get('event', 'Event')}</strong></p>
                <p>{event.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main application."""
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Create Exhibition")
        
        topic = st.text_input(
            "Enter a topic:",
            placeholder="e.g., Aztec Astronomy, Renaissance Art, Ancient Egypt..."
        )
        
        generate_btn = st.button("🎨 Generate Exhibition", use_container_width=True)
        
        st.markdown("---")
        
        # System stats
        st.markdown("## 📈 System Statistics")
        stats = st.session_state.orchestrator.get_system_stats()
        
        success_rate = stats.get('overall_success_rate', 0) * 100
        target_rate = stats.get('target_success_rate', 0) * 100
        
        # Success rate indicator
        if success_rate >= 95:
            indicator_class = "success-high"
        elif success_rate >= 85:
            indicator_class = "success-medium"
        else:
            indicator_class = "success-low"
        
        st.markdown(f"""
        <div class="success-indicator {indicator_class}">
            Success Rate: {success_rate:.1f}%
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Target:** {target_rate:.0f}%")
        st.markdown(f"**Total Executions:** {stats.get('total_executions', 0)}")
        st.markdown(f"**Successful:** {stats.get('total_successes', 0)}")
        
        # Recent exhibitions
        st.markdown("---")
        st.markdown("## 📚 Recent Exhibitions")
        
        memory_bank = MemoryBankAgent()
        recent = memory_bank.list_exhibitions(5)
        
        for ex in recent:
            if st.button(f"📖 {ex['topic'][:30]}...", key=f"load_{ex['id']}"):
                loaded = memory_bank.retrieve_exhibition(ex['id'])
                if loaded:
                    st.session_state.current_exhibition = {
                        'exhibition': loaded,
                        'metrics': {'overall_quality_score': ex['quality_score']}
                    }
                    st.rerun()
    
    # Main content
    if generate_btn and topic:
        with st.spinner("🎨 Curating your exhibition... This may take a minute..."):
            try:
                result = st.session_state.orchestrator.generate_exhibition(topic)
                st.session_state.current_exhibition = result
                st.session_state.generation_history.append({
                    'topic': topic,
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                })
                st.success("✅ Exhibition generated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error generating exhibition: {str(e)}")
                st.session_state.generation_history.append({
                    'topic': topic,
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': str(e)
                })
    
    # Display current exhibition
    if st.session_state.current_exhibition:
        result = st.session_state.current_exhibition
        exhibition = result.get('exhibition', {})
        
        # Metrics
        display_metrics(result.get('metrics', {}))
        
        st.markdown("---")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏛️ Exhibition", 
            "🧠 Knowledge Graph", 
            "🎮 Interactive", 
            "♿ Accessibility",
            "🎨 Multimedia",
            "💬 AI Docent"
        ])
        
        with tab1:
            # Optional 3D room flow
            try:
                fig_rooms = create_room_flow_3d(exhibition.get('rooms', []))
                if fig_rooms:
                    st.plotly_chart(fig_rooms, use_container_width=True)
                    st.markdown("---")
            except:
                pass
            
            # Exhibition content
            display_exhibition(exhibition)
        
        with tab2:
            st.markdown("### 🧠 Knowledge Graph")
            st.markdown("Visual representation of concepts and connections")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Generate 2D Graph"):
                    with st.spinner("Creating knowledge graph..."):
                        graph_data = st.session_state.knowledge_graph_gen.generate_graph(exhibition)
                        img_str = st.session_state.knowledge_graph_gen.visualize_graph(graph_data)
                        
                        st.image(f"data:image/png;base64,{img_str}")
                        
                        metrics = st.session_state.knowledge_graph_gen.get_graph_metrics(graph_data)
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Concepts", metrics['total_nodes'])
                        with col_b:
                            st.metric("Connections", metrics['total_edges'])
                        with col_c:
                            st.metric("Density", metrics['density'])
            
            with col2:
                if st.button("Generate 3D Network (Optional)"):
                    with st.spinner("Creating 3D visualization..."):
                        try:
                            concepts = exhibition.get("semantic_analysis", {}).get("key_concepts", [])
                            connections = exhibition.get("semantic_analysis", {}).get("connections", [])
                            
                            fig_3d = create_concept_network_3d(concepts, connections)
                            if fig_3d:
                                st.plotly_chart(fig_3d, use_container_width=True)
                            else:
                                st.info("3D visualization requires more concepts")
                        except Exception as e:
                            st.info("3D visualization not available (optional feature)")
            
            # Semantic Analysis
            if "semantic_analysis" in exhibition:
                st.markdown("### 🔍 Semantic Analysis")
                semantic = exhibition["semantic_analysis"]
                
                st.markdown("**Key Concepts:**")
                concepts = semantic.get("key_concepts", [])
                st.write(", ".join(concepts[:8]))
                
                st.markdown("**Thematic Insights:**")
                st.info(semantic.get("thematic_insights", ""))
                
                st.markdown("**Connections:**")
                for conn in semantic.get("connections", [])[:3]:
                    st.markdown(f"- **{conn.get('type', '').title()}**: {conn.get('connection', '')}")
        
        with tab3:
            st.markdown("### 🎮 Interactive Elements")
            
            # Quiz
            if "quiz" in exhibition and exhibition["quiz"].get("questions"):
                st.markdown("#### 📝 Knowledge Quiz")
                quiz = exhibition["quiz"]
                st.markdown(f"**{quiz.get('title', 'Quiz')}**")
                
                for i, q in enumerate(quiz.get("questions", [])[:3], 1):
                    with st.expander(f"Question {i}: {q.get('question', '')}"):
                        options = q.get("options", [])
                        if options:
                            answer = st.radio(f"Select answer for Q{i}:", options, key=f"q{i}")
                            if st.button(f"Check Answer {i}", key=f"check{i}"):
                                correct_idx = q.get("correct", 0)
                                if options.index(answer) == correct_idx:
                                    st.success("✅ Correct!")
                                else:
                                    st.error(f"❌ Incorrect. The answer is: {options[correct_idx]}")
                                st.info(f"💡 {q.get('explanation', '')}")
            
            # Challenges
            if "challenges" in exhibition:
                st.markdown("#### 🏆 Exploration Challenges")
                for challenge in exhibition["challenges"]:
                    with st.expander(f"🎯 {challenge.get('title', '')}"):
                        st.markdown(f"**Challenge:** {challenge.get('description', '')}")
                        st.markdown(f"**Reward:** {challenge.get('reward', '')}")
                        if st.button(f"Mark Complete", key=f"challenge_{challenge.get('title')}"):
                            st.balloons()
                            st.success("Challenge completed! 🎉")
            
            # Room Questions
            st.markdown("#### 💭 Discussion Questions")
            question_counter = 0
            for i, room in enumerate(exhibition.get("rooms", []), 1):
                if "interactive_questions" in room:
                    with st.expander(f"Room {i}: {room.get('title', '')}"):
                        for j, q in enumerate(room["interactive_questions"]):
                            question_counter += 1
                            st.markdown(f"**Q:** {q.get('question', '')}")
                            st.caption(f"💡 Hint: {q.get('hint', '')}")
                            st.text_area(f"Your thoughts:", key=f"room{i}_question{question_counter}_{j}", height=100)
        
        with tab4:
            st.markdown("### ♿ Accessibility Features")
            
            if "accessibility" in exhibition:
                access = exhibition["accessibility"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 👁️ Visual Accessibility")
                    visual = access.get("visual", {})
                    for key, value in visual.items():
                        st.markdown(f"- **{key.replace('_', ' ').title()}**: {value}")
                    
                    st.markdown("#### 👂 Auditory Accessibility")
                    auditory = access.get("auditory", {})
                    for key, value in auditory.items():
                        st.markdown(f"- **{key.replace('_', ' ').title()}**: {value}")
                
                with col2:
                    st.markdown("#### 🧠 Cognitive Accessibility")
                    cognitive = access.get("cognitive", {})
                    for key, value in cognitive.items():
                        st.markdown(f"- **{key.replace('_', ' ').title()}**: {value}")
                    
                    st.markdown("#### 🌍 Language Support")
                    language = access.get("language", {})
                    if "languages" in language:
                        st.markdown(f"**Available in:** {', '.join(language['languages'][:6])}")
        
        with tab5:
            st.markdown("### 🎨 Multimedia Experience")
            
            # Virtual Tour
            if "virtual_tour" in exhibition:
                st.markdown("#### 🎧 Virtual Tour Guide")
                tour = exhibition["virtual_tour"]
                st.info(tour.get("introduction", ""))
                
                st.markdown("**Tour Highlights:**")
                st.write(tour.get("highlights", ""))
            
            # Audio Guide
            if "audio_guide" in exhibition:
                st.markdown("#### 🔊 Audio Guide Stops")
                for stop in exhibition["audio_guide"]:
                    with st.expander(f"Stop {stop.get('stop_number')}: {stop.get('location')}"):
                        st.markdown(f"**Duration:** {stop.get('duration')}")
                        st.markdown(f"**Preview:** {stop.get('script_preview')}")
                        st.markdown(f"**Languages:** {', '.join(stop.get('language_options', []))}")
            
            # Multimedia per exhibit
            st.markdown("#### 🎬 Multimedia Elements")
            for room in exhibition.get("rooms", [])[:2]:
                for exhibit in room.get("exhibits", [])[:2]:
                    if "multimedia" in exhibit:
                        with st.expander(f"📱 {exhibit.get('name', '')}"):
                            mm = exhibit["multimedia"]
                            st.markdown(f"- **3D Model:** {mm.get('3d_model', '')}")
                            st.markdown(f"- **Video:** {mm.get('video', '')}")
                            st.markdown(f"- **AR Experience:** {mm.get('ar_experience', '')}")
        
        with tab6:
            st.markdown("### 💬 Ask the AI Docent")
            st.markdown("Have questions about the exhibition? Ask our AI guide!")
            
            # Suggested questions
            st.markdown("**Suggested Questions:**")
            suggestions = st.session_state.ai_docent.suggest_questions(exhibition)
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions[:4]):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"suggest_{i}"):
                        answer = st.session_state.ai_docent.ask_question(suggestion, exhibition)
                        st.session_state.chat_history.append({"q": suggestion, "a": answer})
            
            # Chat interface
            st.markdown("---")
            question = st.text_input("Ask your question:", key="docent_question")
            if st.button("Ask Docent") and question:
                with st.spinner("Docent is thinking..."):
                    answer = st.session_state.ai_docent.ask_question(question, exhibition)
                    st.session_state.chat_history.append({"q": question, "a": answer})
            
            # Display chat history
            if st.session_state.chat_history:
                st.markdown("### 📜 Conversation History")
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
                    with st.expander(f"Q: {chat['q'][:60]}..."):
                        st.markdown(f"**Question:** {chat['q']}")
                        st.markdown(f"**Answer:** {chat['a']}")
        
        # Exhibition content
        display_exhibition(exhibition)
        
        # Download options
        st.markdown("---")
        st.markdown("### 💾 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            json_str = json.dumps(result.get('exhibition', {}), indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"exhibition_{result.get('exhibition', {}).get('topic', 'export').replace(' ', '_')}.json",
                mime="application/json"
            )
        
        with col2:
            # Generate text version
            exhibition = result.get('exhibition', {})
            text_content = f"""
{exhibition.get('title', exhibition.get('topic', 'Exhibition'))}
{'=' * 80}

{exhibition.get('curator_notes', '')}

{'=' * 80}
ROOMS
{'=' * 80}

"""
            for i, room in enumerate(exhibition.get('rooms', []), 1):
                text_content += f"\nROOM {i}: {room.get('title', 'Untitled')}\n"
                text_content += f"{'-' * 80}\n"
                text_content += f"{room.get('description', '')}\n\n"
                
                for j, exhibit in enumerate(room.get('exhibits', []), 1):
                    text_content += f"\nExhibit {j}: {exhibit.get('name', 'Untitled')}\n"
                    text_content += f"{exhibit.get('description', '')}\n\n"
            
            st.download_button(
                label="📄 Download Text",
                data=text_content,
                file_name=f"exhibition_{exhibition.get('topic', 'export').replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        with col3:
            # Generate HTML/PDF version
            try:
                from utils.pdf_generator import ExhibitionPDFGenerator
                
                pdf_gen = ExhibitionPDFGenerator()
                html_content = pdf_gen.generate_pdf(
                    result.get('exhibition', {}),
                    result.get('metrics', {})
                )
                
                st.download_button(
                    label="📕 Download PDF (HTML)",
                    data=html_content,
                    file_name=f"exhibition_{exhibition.get('topic', 'export').replace(' ', '_')}.html",
                    mime="text/html",
                    help="Download as HTML - Open in browser and Print to PDF (Ctrl+P)"
                )
            except Exception as e:
                st.error(f"PDF generation error: {str(e)}")
    else:
        # Welcome message
        st.markdown("""
        ## Welcome to MuseVerse! 🏛️
        
        **An AI Museum Curator** that transforms any topic into a comprehensive exhibition with:
        
        - 🎨 **Curated Exhibits** - Detailed artifacts and displays
        - 📚 **Thematic Rooms** - Organized exhibition spaces
        - ⏳ **Historical Timelines** - Chronological context
        - 📜 **Curator Notes** - Expert commentary
        - 🖼️ **Visual References** - Contextual imagery
        
        ### How it works:
        
        1. Enter a topic in the sidebar (history, culture, science, art)
        2. Click "Generate Exhibition"
        3. Explore your custom museum experience
        4. Download and share your exhibition
        
        **Powered by multi-agent AI with 95-99% success rate!**
        """)

if __name__ == "__main__":
    main()
