import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import time
import random
import pandas as pd
from datetime import datetime

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Script generation function using the official Gemini library
def generate_script(content_type, title, tone="casual", duration="medium", target_audience="general"):
    # Create a more detailed prompt based on all parameters
    if content_type == "instagram":
        prompt = f"""
        Generate an engaging Instagram reel/story script about: "{title}"
        Tone: {tone}
        Duration: {duration} (keep it under 60 seconds of speaking time)
        Target Audience: {target_audience}
        
        Format the script with clear sections for:
        - Hook (attention-grabbing opening)
        - Main content (2-3 key points)
        - Call to action
        
        Include suggestions for visual elements/transitions in [brackets].
        """
    elif content_type == "youtube":
        prompt = f"""
        Generate a structured YouTube video script for: "{title}"
        Tone: {tone}
        Duration: {duration}
        Target Audience: {target_audience}
        
        Format with:
        - Attention-grabbing intro (30 seconds)
        - Main content with clear sections/timestamps
        - Conclusion and call to action
        
        Include B-roll suggestions, talking points, and transitions in [brackets].
        """
    elif content_type == "podcast":
        prompt = f"""
        Generate a set of insightful Q&A prompts for a podcast titled: "{title}"
        Tone: {tone}
        Target Audience: {target_audience}
        
        Include:
        - 5-8 thought-provoking questions
        - 2-3 follow-up questions for each main question
        - Suggested talking points for the host
        - Opening and closing segments
        
        Questions should encourage in-depth, interesting responses.
        """
    
    try:
        # Add a simulated loading delay for better UX
        with st.spinner("AI is crafting your script..."):
            # Simulate API call delay
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)  # Simulate API processing time
                progress_bar.progress(i + 1)
            
            # Create the model and generate content
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_k=40,
                    top_p=0.95,
                    max_output_tokens=1024
                )
            )
            
            # Remove the progress bar after completion
            progress_bar.empty()
            
            # Extract generated text from response
            generated_text = response.text
            return generated_text
    except Exception as e:
        return f"Error generating script: {str(e)}"

# Function to save script to history
def save_to_history(content_type, title, script):
    if 'script_history' not in st.session_state:
        st.session_state.script_history = []
    
    # Save to history with timestamp
    st.session_state.script_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "content_type": content_type,
        "title": title,
        "script": script
    })

# Function to load script from history
def load_from_history(index):
    if 'script_history' in st.session_state and index < len(st.session_state.script_history):
        return st.session_state.script_history[index]
    return None

# Set page configuration with custom theme
st.set_page_config(
    page_title="ScriptCraft AI | Content Creator Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS with enhanced vibrant design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7f9 0%, #e8f0fe 100%);
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .script-container {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
        border-left: 5px solid #4B61D1;
    }
    
    .content-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.4s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .content-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.12);
        border-color: rgba(75, 97, 209, 0.2);
    }
    
    .stat-box {
        background: linear-gradient(135deg, #4B61D1 0%, #7C8CE8 100%);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(75, 97, 209, 0.3);
    }
    
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    h2, h3 {
        color: #1E3A8A;
        font-weight: 600;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4B61D1 0%, #3B4FBF 100%);
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-weight: 500;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(59, 79, 191, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #3B4FBF 0%, #2A3CA9 100%);
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 15px rgba(59, 79, 191, 0.4);
    }
    
    .tab-content {
        padding: 20px 0;
    }
    
    /* Styling for sidebar */
    .sidebar .css-1d391kg {
        background: linear-gradient(180deg, #f8faff 0%, #e8f0fe 100%);
    }
    
    .sidebar-header {
        padding: 25px 0;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .sidebar-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .sidebar-item:hover {
        background-color: rgba(75, 97, 209, 0.1);
        transform: translateX(5px);
    }
    
    /* Added for clear content type indication */
    .selected-type {
        background: linear-gradient(135deg, #e8f0fe 0%, #d1ddff 100%);
        border-left: 3px solid #4B61D1;
        padding-left: 12px;
        font-weight: 500;
    }
    
    /* Content type cards */
    .type-card {
        text-align: center;
        background: white;
        border-radius: 12px;
        padding: 20px 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.4s;
        height: 100%;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .type-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 25px rgba(75, 97, 209, 0.18);
        border-color: #4B61D1;
    }
    
    .type-card h3 {
        font-size: 20px;
        margin-bottom: 10px;
        color: #1E3A8A;
    }
    
    .type-card p {
        font-size: 14px;
        color: #555;
    }
    
    .type-card .icon {
        font-size: 36px;
        margin-bottom: 15px;
        color: #4B61D1;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 1.5s infinite ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'selected_content_type' not in st.session_state:
    st.session_state.selected_content_type = None
if 'selected_history_index' not in st.session_state:
    st.session_state.selected_history_index = None
if 'current_script' not in st.session_state:
    st.session_state.current_script = None
if 'script_history' not in st.session_state:
    st.session_state.script_history = []
if 'nav_option' not in st.session_state:
    st.session_state.nav_option = "Create Script"

# Sidebar for navigation and settings
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    # Logo area
    st.markdown("# 🎬 ScriptCraft AI")
    st.markdown("#### Content Creator Studio")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 📍 Navigation")
    
    nav_options = ["Create Script", "My Scripts", "Tips & Templates"]
    for nav in nav_options:
        is_selected = st.session_state.nav_option == nav
        style_class = "sidebar-item selected-type" if is_selected else "sidebar-item"
        
        st.markdown(f"<div class='{style_class}'>", unsafe_allow_html=True)
        if st.button(f"{'✓ ' if is_selected else ''}{nav}", key=f"nav_{nav}"):
            st.session_state.nav_option = nav
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Settings section for Create Script
    if st.session_state.nav_option == "Create Script":
        st.markdown("### ⚙️ Script Settings")
        
        # Show content type selection if it exists
        if st.session_state.selected_content_type:
            content_type_labels = {
                "instagram": "📱 Instagram Reel",
                "youtube": "🎬 YouTube Video",
                "podcast": "🎙️ Podcast Q&A"
            }
            st.markdown(f"<div class='selected-type'>**Selected type:** {content_type_labels.get(st.session_state.selected_content_type)}</div>", unsafe_allow_html=True)
        
        # Advanced settings
        with st.expander("Advanced Options", expanded=False):
            tone_options = ["casual", "professional", "humorous", "inspirational", "educational"]
            st.session_state.selected_tone = st.select_slider(
                "Tone", 
                options=tone_options, 
                value=st.session_state.get('selected_tone', 'casual')
            )
            
            duration_mapping = {
                "instagram": ["15 seconds", "30 seconds", "60 seconds"],
                "youtube": ["3-5 minutes", "5-10 minutes", "10-15 minutes", "15+ minutes"],
                "podcast": ["20-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"]
            }
            
            if st.session_state.selected_content_type:
                durations = duration_mapping.get(st.session_state.selected_content_type, ["Short", "Medium", "Long"])
                st.session_state.duration_selection = st.selectbox(
                    "Duration", 
                    durations,
                    index=durations.index(st.session_state.get('duration_selection', durations[0])) if st.session_state.get('duration_selection') in durations else 0
                )
            else:
                st.session_state.duration_selection = st.selectbox(
                    "Duration", 
                    ["Short", "Medium", "Long"],
                    index=["Short", "Medium", "Long"].index(st.session_state.get('duration_selection', "Medium")) if st.session_state.get('duration_selection') in ["Short", "Medium", "Long"] else 1
                )
            
            st.session_state.target_audience = st.text_input(
                "Target Audience", 
                value=st.session_state.get('target_audience', 'general')
            )
    
    # Recent scripts quick access
    if len(st.session_state.script_history) > 0:
        st.markdown("### 🕒 Recent Scripts")
        for i, item in enumerate(st.session_state.script_history[-3:]):  # Show last 3
            st.markdown(f"<div class='sidebar-item'>", unsafe_allow_html=True)
            if st.button(f"{item['title'][:15]}...", key=f"recent_{i}"):
                st.session_state.selected_history_index = len(st.session_state.script_history) - 3 + i
                st.session_state.nav_option = "My Scripts"
            st.markdown(f"<div style='font-size:11px;color:#666;'>{item['content_type'].title()} • {item['timestamp']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Main content area based on navigation selection
if st.session_state.nav_option == "Create Script":
    # Header section with animations and gradients
    st.markdown("<div style='text-align:center;padding:20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:48px;background:linear-gradient(90deg, #1E3A8A, #4B61D1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>ScriptCraft AI Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px;color:#555;margin-bottom:30px;'>Transform your ideas into engaging scripts in seconds with AI-powered creativity</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input container
    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        # Title input with character count
        title_col1, title_col2 = st.columns([3, 1])
        with title_col1:
            title_input = st.text_input("What's your content about?", 
                                       placeholder="Enter a title or topic for your content...",
                                       value=st.session_state.get('title_input', ''))
            if title_input:
                st.session_state.title_input = title_input
        with title_col2:
            if title_input:
                st.markdown(f"<div class='stat-box'>{len(title_input)} characters</div>", unsafe_allow_html=True)
        
        # Content Type Selector - Visual buttons with icons
        st.write("##### Choose your content type:")
        col1, col2, col3 = st.columns(3)
        
        # Content types with enhanced visual appeal
        content_types = {
            "instagram": {
                "icon": "📱",
                "name": "Instagram Reel",
                "desc": "Short, engaging content for Instagram reels/stories"
            },
            "youtube": {
                "icon": "🎬",
                "name": "YouTube Video",
                "desc": "Structured scripts for long-form YouTube videos"
            },
            "podcast": {
                "icon": "🎙️",
                "name": "Podcast Q&A",
                "desc": "Insightful Q&A for engaging podcast episodes"
            }
        }
        
        # Create the buttons for each content type with enhanced UI
        with col1:
            is_selected = st.session_state.selected_content_type == "instagram"
            border_style = "border-color: #4B61D1;" if is_selected else ""
            bg_style = "background: linear-gradient(135deg, #e8f0fe 0%, #d1ddff 100%);" if is_selected else ""
            
            st.markdown(f"""
            <div class="type-card" style="{border_style}{bg_style}" onclick="document.getElementById('instagram_btn').click();">
                <div class="icon">{content_types["instagram"]["icon"]}</div>
                <h3>{content_types["instagram"]["name"]}</h3>
                <p>{content_types["instagram"]["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle the click
            if st.button(content_types["instagram"]["name"], key="instagram_btn", help="Create content for Instagram reels and stories"):
                st.session_state.selected_content_type = "instagram"
                st.rerun()
            
        with col2:
            is_selected = st.session_state.selected_content_type == "youtube"
            border_style = "border-color: #4B61D1;" if is_selected else ""
            bg_style = "background: linear-gradient(135deg, #e8f0fe 0%, #d1ddff 100%);" if is_selected else ""
            
            st.markdown(f"""
            <div class="type-card" style="{border_style}{bg_style}" onclick="document.getElementById('youtube_btn').click();">
                <div class="icon">{content_types["youtube"]["icon"]}</div>
                <h3>{content_types["youtube"]["name"]}</h3>
                <p>{content_types["youtube"]["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle the click
            if st.button(content_types["youtube"]["name"], key="youtube_btn", help="Create scripted content for YouTube videos"):
                st.session_state.selected_content_type = "youtube"
                st.rerun()
            
        with col3:
            is_selected = st.session_state.selected_content_type == "podcast"
            border_style = "border-color: #4B61D1;" if is_selected else ""
            bg_style = "background: linear-gradient(135deg, #e8f0fe 0%, #d1ddff 100%);" if is_selected else ""
            
            st.markdown(f"""
            <div class="type-card" style="{border_style}{bg_style}" onclick="document.getElementById('podcast_btn').click();">
                <div class="icon">{content_types["podcast"]["icon"]}</div>
                <h3>{content_types["podcast"]["name"]}</h3>
                <p>{content_types["podcast"]["desc"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button to handle the click
            if st.button(content_types["podcast"]["name"], key="podcast_btn", help="Create Q&A content for podcast episodes"):
                st.session_state.selected_content_type = "podcast"
                st.rerun()
        
        # Show selected type with animation
        if st.session_state.selected_content_type:
            st.success(f"Selected: {content_types[st.session_state.selected_content_type]['name']}")
        
        # Generate button (only active when both title and content type are selected)
        generate_disabled = not (title_input and st.session_state.selected_content_type)
        
        st.markdown("<div style='text-align:center;margin-top:20px;'>", unsafe_allow_html=True)
        if st.button("✨ Generate My Script", disabled=generate_disabled, help="Generate your content script"):
            if not generate_disabled:
                # Get advanced settings if available
                tone = st.session_state.get('selected_tone', "casual")
                duration = st.session_state.get('duration_selection', "medium")
                target_audience = st.session_state.get('target_audience', "general")
                    
                # Generate the script
                st.session_state.current_script = generate_script(
                    st.session_state.selected_content_type,
                    title_input,
                    tone,
                    duration,
                    target_audience
                )
                
                # Save to history
                save_to_history(
                    st.session_state.selected_content_type,
                    title_input,
                    st.session_state.current_script
                )
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Output section
    if st.session_state.current_script:
        st.markdown("<h3 style='margin-top:30px;'>Your Generated Script</h3>", unsafe_allow_html=True)
        
        # Script display with enhanced formatting
        st.markdown('<div class="script-container">', unsafe_allow_html=True)
        st.markdown(st.session_state.current_script)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons for the script
        st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copy to Clipboard", help="Copy the script to clipboard"):
                st.success("Script copied to clipboard!")
        with col2:
            if st.button("💾 Download as Text", help="Download the script as a text file"):
                st.info("Download started...")
        with col3:
            if st.button("🔄 Regenerate", help="Generate a new version of the script"):
                st.info("Regenerating script...")
                # Get advanced settings if available
                tone = st.session_state.get('selected_tone', "casual")
                duration = st.session_state.get('duration_selection', "medium")
                target_audience = st.session_state.get('target_audience', "general")
                
                # Regenerate the script
                st.session_state.current_script = generate_script(
                    st.session_state.selected_content_type,
                    title_input,
                    tone,
                    duration,
                    target_audience
                )
                
                # Update history with new version
                save_to_history(
                    st.session_state.selected_content_type,
                    title_input,
                    st.session_state.current_script
                )
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Script evaluation with improved UI
        st.markdown("<h4 style='margin-top:30px;'>How was this script?</h4>", unsafe_allow_html=True)
        feedback = st.slider("Rate this script", 1, 5, 3)
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Submit Feedback", help="Tell us what you think"):
                st.balloons()
                st.success("Thank you for your feedback! We'll use it to improve future scripts.")

elif st.session_state.nav_option == "My Scripts":
    st.markdown("<h2>Your Saved Scripts</h2>", unsafe_allow_html=True)
    if st.session_state.script_history:
        for item in reversed(st.session_state.script_history):
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"**{item['title']}**  •  {item['content_type'].title()}  •  {item['timestamp']}")
            st.markdown(item['script'])
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No scripts saved yet.")

elif st.session_state.nav_option == "Tips & Templates":
    st.markdown("<h2>Tips & Templates</h2>", unsafe_allow_html=True)
    
    # Section: Creating Engaging Interview Questions
    st.markdown("""
### Creating Engaging Interview Questions

Great podcast interviews come from thoughtful questions that:

- **Start broad, then go deep** - Begin with context-setting questions before diving into specifics
- **Use the "curiosity ladder"** - Each question should build on the previous answer
- **Ask "why" not just "what"** - Get to motivations and feelings, not just facts
- **Prepare follow-ups** - Anticipate responses and have thoughtful follow-ups ready

### Podcast Episode Structure

1. **Intro (2-3 minutes)** - Welcome, guest introduction, episode overview
2. **Background (5-10 minutes)** - Establish guest credibility and journey
3. **Main discussion (15-30 minutes)** - Core topic exploration through prepared questions
4. **Lightning round (5 minutes)** - Quick, fun questions to end on a high note
5. **Outro (2 minutes)** - Thank guest, summarize insights, call-to-action

### Creating a Comfortable Interview Environment

- Send questions to guests in advance (but keep a few surprises)
- Begin with softball questions to build rapport
- Use "Yes, and..." technique to build on guest responses
- Include personal stories or experiences to make the conversation relatable
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Example template section
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🌟 Podcast Interview Template")
    
    st.code("""
# PODCAST INTERVIEW TEMPLATE

## INTRO (2-3 minutes)
HOST: "Welcome to [Podcast Name], the show where we [podcast mission]. I'm your host [Name], and today I'm thrilled to be joined by [Guest Name], who is [brief credential]. [Guest], welcome to the show!"

GUEST: [Response]

HOST: "For our listeners who might not be familiar with your work, could you share a bit about who you are and what you do?"

GUEST: [Response]

HOST: "On today's episode, we'll be diving into [episode topic]. Here's what we'll cover..."

## BACKGROUND QUESTIONS (5-10 minutes)
1. "What first drew you to [field/area of expertise]?"
   * Follow-up: "Was there a specific moment when you knew this was your path?"

2. "You've accomplished [notable achievement]. Can you walk us through that journey?"
   * Follow-up: "What obstacles did you face along the way?"

3. "How has your approach to [topic] evolved over time?"
   * Follow-up: "What caused that shift in perspective?"

## MAIN TOPIC QUESTIONS (15-30 minutes)
4. "What's the biggest misconception people have about [topic]?"
   * Follow-up: "Why do you think this misconception persists?"

5. "In your [book/article/talk], you mentioned [specific point]. Could you elaborate on that?"
   * Follow-up: "How have you applied this principle in your own work?"

6. "What's a counterintuitive truth about [topic] that most people don't realize?"
   * Follow-up: "How did you discover this?"

7. "How do you think [recent development] will impact [industry/field]?"
   * Follow-up: "What should people be doing to prepare for this change?"

8. "If someone wanted to get started with [topic], what would be your advice?"
   * Follow-up: "What resources would you recommend?"

## LIGHTNING ROUND (5 minutes)
9. "What's one tool or resource you couldn't live without?"
10. "What's a book that changed your perspective?"
11. "What's your favorite failure?" (lesson learned from a setback)
12. "What's a small habit that has had a big impact on your success?"
13. "Fill in the blank: 'Most people would be better at [topic] if they just _____.'"

## OUTRO (2 minutes)
HOST: "Before we wrap up, where can our listeners find you and learn more about your work?"

GUEST: [Response]

HOST: "Any final thoughts or advice for our listeners interested in [topic]?"

GUEST: [Response]

HOST: "Thank you so much for sharing your insights with us today. To our listeners, if you enjoyed this episode, please subscribe and leave a review. Join us next week when we'll be talking with [Next Guest] about [Topic]. Until then, [Signature Sign-off]."

[NOTES FOR HOST]
- Research guest thoroughly before interview
- Listen actively and be willing to go off-script for interesting tangents
- Have water available for guest
- Monitor time to ensure all key questions are covered
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use This Template", key="use_podcast_template"):
            st.session_state.nav_option = "Create Script"
            st.session_state.selected_content_type = "podcast"
            st.session_state.title_input = "Expert Interview Series"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer section for Tips & Templates
    st.markdown("""
<div style="margin-top: 50px; padding: 20px; background: linear-gradient(135deg, #f5f7f9 0%, #e8f0fe 100%); border-radius: 10px; text-align: center;">
    <p style="margin-bottom: 10px; font-weight: 500;">ScriptCraft AI | Craft. Create. Connect.</p>
    <p style="font-size: 12px; color: #666;">© 2023 ScriptCraft AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

# Global Footer (if needed in all nav sections)
st.markdown("""
<div style="margin-top: 50px; padding: 20px; text-align: center; font-size: 12px; color: #666;">
    © 2023 ScriptCraft AI. All rights reserved.
</div>
""", unsafe_allow_html=True)
