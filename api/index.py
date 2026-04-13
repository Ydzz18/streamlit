import subprocess
import sys

def handler(request):
    """Vercel serverless function handler for Streamlit"""
    # Run Streamlit as a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"],
        cwd="/tmp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return {
        "statusCode": 200,
        "body": "Streamlit app initialized"
    }
