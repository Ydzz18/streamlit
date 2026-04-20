import streamlit.web.cli as stcli
import sys
import os

# Configure Streamlit for production
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ENABLEXSRFPROTECTION'] = 'false'

def run_streamlit():
    """Run Streamlit app"""
    sys.argv = ["streamlit", "run", "app.py"]
    stcli.main()

if __name__ == "__main__":
    run_streamlit()
