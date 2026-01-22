import subprocess
from pyngrok import ngrok
import time

ngrok.set_auth_token("YOUR_AUTH_TOKEN")

print("🚀 Starting Streamlit server on different port...")

# Use port 8502 instead of 8501
subprocess.Popen(['streamlit', 'run', 'mental_health_app.py',
                  '--server.port=8502', '--server.headless=true'],
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL)

time.sleep(5)
print("🌐 Creating public URL...")

public_url = ngrok.connect(8502)

print("\n" + "="*60)
print("✨ YOUR MENTAL HEALTH COMPANION IS READY! ✨")
print("="*60)
print(f"\n🔗 Click here to open: {public_url}\n")
print("\n" + "="*60)
