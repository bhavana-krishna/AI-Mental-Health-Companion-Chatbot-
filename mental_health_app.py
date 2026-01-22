import streamlit as st
from groq import Groq
import datetime

# Initialize Groq client
# 🔑 REPLACE 'YOUR_GROQ_API_KEY_HERE' with your actual API key from console.groq.com
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

# Page configuration
st.set_page_config(
    page_title="Mental Health Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [Copy the entire enhanced CSS and rest of the code from the artifact above]
```

4. Click **Commit new file**

### Step 5: Add README.md
1. Click on the existing **README.md** file
2. Click the **pencil icon** (Edit)
3. Replace content with the README from my artifact above
4. Click **Commit changes**

### Step 6: Add requirements.txt
1. Click **Add file → Create new file**
2. Name: `requirements.txt`
3. Add:
```
streamlit==1.28.0
groq==0.4.1
pyngrok==7.0.0
```
4. Click **Commit new file**

---

## 🎯 Method 2: Use GitHub Desktop (If you prefer GUI)

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Sign in** with your GitHub account
3. **Create new repository** (File → New repository)
4. **Add files** from your computer
5. **Publish** to GitHub

---

## 🎯 Method 3: Try Saving to Different Repo

The error might be because `bhavana-krishna/bhavana-krishna` is a special profile README repo. Try:

1. In Colab: **File → Save a copy in GitHub**
2. When prompted, choose **"Create new repository"**
3. Name it: `mental-health-companion`
4. This should work better!

---

## ✅ What Your Final Repo Should Look Like:
```
mental-health-companion/
├── AI_Mental_Health_Companion_Chatbot.ipynb
├── mental_health_app.py
├── README.md
├── requirements.txt
└── .gitignore (optional)
