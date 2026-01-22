import streamlit as st
from groq import Groq
import datetime
import random
import os

# Initialize Groq client with secrets management
# For Streamlit Cloud: Add GROQ_API_KEY in your app secrets
# For local: Add to .streamlit/secrets.toml or set as environment variable
try:
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("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", ""))
    if not api_key:
        st.error("⚠️ Please add your GROQ_API_KEY to Streamlit secrets or environment variables")
        st.stop()
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with beautiful design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }

    .block-container {
        background: white;
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Header Styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }

    .sub-header {
        text-align: center;
        color: #4a5568;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Chat Message Styles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: auto;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.4s ease-out;
    }

    .user-message strong {
        color: white !important;
        font-weight: 600;
    }

    .ai-message {
        background: #f7fafc;
        border-left: 4px solid #667eea;
        color: #2d3748;
        padding: 1.2rem 1.5rem;
        border-radius: 5px 20px 20px 20px;
        margin: 1rem 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInLeft 0.4s ease-out;
    }

    .ai-message strong {
        color: #667eea;
        font-weight: 600;
    }

    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(240, 147, 251, 0.4);
        animation: fadeIn 1s ease-out;
    }

    .welcome-card h3 {
        color: white;
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .welcome-card ul {
        list-style: none;
        padding-left: 0;
    }

    .welcome-card li {
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }

    .welcome-card li:before {
        content: "✨";
        position: absolute;
        left: 0;
    }

    /* Button Styles */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Section Headers */
    .section-header {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Exercise Cards */
    .exercise-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #2d3748;
    }

    .exercise-card h4 {
        color: #667eea;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'mood_log' not in st.session_state:
    st.session_state.mood_log = []

# System prompt for the AI
SYSTEM_PROMPT = """You are a compassionate and empathetic mental health companion. Your role is to:
- Listen actively and provide emotional support
- Offer coping strategies and mindfulness techniques
- Encourage positive thinking and self-care
- Validate feelings without judgment
- Suggest professional help when needed
- Be warm, understanding, and supportive

Remember: You are NOT a replacement for professional mental health care. Always encourage users to seek professional help for serious concerns."""

def get_ai_response(user_message, conversation_history):
    """Get response from Groq AI"""
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history (last 3 exchanges)
        for msg in conversation_history[-6:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}. Please try again."

# Header
st.markdown("<h1 class='main-header'>🌸 Mental Health Companion</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your safe space for emotional support and wellness ✨</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: white; text-align: center;'>🌟 Quick Tools</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Mood tracker
    st.markdown("<h3 style='color: white;'>💭 How are you feeling?</h3>", unsafe_allow_html=True)
    mood = st.select_slider(
        "",
        options=["😢 Very Bad", "😞 Bad", "😐 Okay", "🙂 Good", "😊 Great"],
        value="😐 Okay"
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📝 Log Mood"):
            st.session_state.mood_log.append({
                'mood': mood,
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("✅ Mood logged!")
    
    with col2:
        if st.button("📊 View Log"):
            if st.session_state.mood_log:
                st.markdown("<div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;'>", unsafe_allow_html=True)
                for entry in st.session_state.mood_log[-5:]:
                    st.write(f"**{entry['mood']}** - {entry['time']}")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No mood logs yet!")
    
    st.markdown("---")
    
    # Quick exercises
    st.markdown("<h3 style='color: white;'>🧘‍♀️ Quick Exercises</h3>", unsafe_allow_html=True)
    
    if st.button("🌬️ Breathing Exercise"):
        st.markdown("""
        <div class='exercise-card'>
            <h4>Box Breathing</h4>
            <p><strong>Follow these steps:</strong></p>
            <ol>
                <li>Breathe in for 4 seconds 💨</li>
                <li>Hold for 4 seconds ⏸️</li>
                <li>Breathe out for 4 seconds 🌊</li>
                <li>Hold for 4 seconds ⏸️</li>
            </ol>
            <p><em>Repeat 4 times for best results!</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎯 Grounding Technique"):
        st.markdown("""
        <div class='exercise-card'>
            <h4>5-4-3-2-1 Technique</h4>
            <p><strong>Name out loud:</strong></p>
            <ul>
                <li>👁️ 5 things you can <strong>see</strong></li>
                <li>✋ 4 things you can <strong>touch</strong></li>
                <li>👂 3 things you can <strong>hear</strong></li>
                <li>👃 2 things you can <strong>smell</strong></li>
                <li>👅 1 thing you can <strong>taste</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("✨ Positive Affirmation"):
        affirmations = [
            ("You are worthy of love and respect", "💜"),
            ("You are doing better than you think", "🌟"),
            ("It's okay to take things one day at a time", "🌅"),
            ("Your feelings are valid", "💙"),
            ("You have the strength to get through this", "💪"),
            ("Be kind to yourself today", "🌸"),
            ("Progress, not perfection", "🎯"),
            ("You are enough, just as you are", "🌈"),
            ("This too shall pass", "🌊"),
            ("You deserve happiness and peace", "☮️")
        ]
        affirmation, emoji = random.choice(affirmations)
        st.markdown(f"""
        <div class='exercise-card' style='text-align: center; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;'>
            <h2>{emoji}</h2>
            <h3 style='color: white;'>{affirmation}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Resources
    st.markdown("<h3 style='color: white;'>📞 Crisis Resources</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; color: white;'>
        <p><strong>🆘 National Crisis Line:</strong><br/>988</p>
        <p><strong>💬 Crisis Text Line:</strong><br/>Text HOME to 741741</p>
        <p><strong>🌐 International:</strong><br/>findahelpline.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat area
st.markdown("<h2 class='section-header'>💬 Let's Talk</h2>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class='user-message'>
            <strong>You:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='ai-message'>
            <strong>🌸 Companion:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("💭 Share what's on your mind... I'm here to listen")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner("🤔 Thinking..."):
        ai_response = get_ai_response(user_input, st.session_state.messages)
    
    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Rerun to update chat
    st.rerun()

# Welcome message if chat is empty
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class='welcome-card'>
        <h3>👋 Welcome! I'm here for you.</h3>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
            This is a safe, judgment-free space where you can share your thoughts and feelings.
            Whether you're having a tough day or just need someone to talk to, I'm here to listen and support you.
        </p>
        <br>
        <p style='font-size: 1.2rem; font-weight: 600;'>You can talk to me about:</p>
        <ul style='font-size: 1.05rem; line-height: 1.8;'>
            <li>Stress and anxiety management</li>
            <li>Understanding your mood and emotions</li>
            <li>Learning coping strategies</li>
            <li>Developing self-care routines</li>
            <li>Or anything else on your mind</li>
        </ul>
        <br>
        <div style='background: rgba(255,255,255,0.2); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;'>
            <p style='font-size: 1.1rem; margin: 0;'>
                <strong>⚠️ Important:</strong> I'm here to support you, but I'm not a replacement for professional mental health care.
                If you're in crisis or need immediate help, please reach out to a crisis helpline.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2rem 0; border-top: 2px solid #e2e8f0;'>
    <p style='font-size: 0.9rem;'>Made with 💜 for your mental wellness journey</p>
    <p style='font-size: 0.8rem;'>Remember: Taking care of your mental health is a sign of strength, not weakness.</p>
</div>
""", unsafe_allow_html=True)
print("\n" + "="*60)
print("✨ YOUR MENTAL HEALTH COMPANION IS READY! ✨")
print("="*60)
print(f"\n🔗 Click here to open: {public_url}\n")
print("\n" + "="*60)
