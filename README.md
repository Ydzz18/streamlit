# Song Search - Lyrics Finder

A Streamlit application that searches for songs and displays their lyrics using the LRClib API.

## Features

- 🎵 Search for songs by title or artist
- 📝 Display song lyrics with synced or plain text
- 🎨 Clean, user-friendly interface
- ⚡ Real-time results

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd streamlit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment on Vercel

### Prerequisites
- Vercel account (sign up at https://vercel.com)
- Git repository with your code

### Steps

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New..." → "Project"
4. Import your repository
5. Select the project root (the `streamlit` folder)
6. Click "Deploy"

Vercel will automatically detect the `vercel.json` configuration and deploy your Streamlit app.

## Project Structure

```
streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## API Used

- [LRClib](https://lrclib.net/) - Free lyrics API

## License

MIT License
