import streamlit as st
import requests

st.title("Song Search")
st.write("Enter daw kanta tapos pindutin search button para lumabas lyrics sabi ni sir")

# Initialize session state for results
if "search_results" not in st.session_state:
    st.session_state.search_results = None

query = st.text_input("Search your song", placeholder="e.g., Dubidubidapdap Kuya Will")

if st.button("Search"):
    if not query.strip():
        st.warning("Try Again! Walang laman ang search box mo.")
    else:
        with st.spinner("Nagtatanong pa kay asset kung meron..."):
            try:
                url = "https://lrclib.net/api/search"  # ✅ Removed extra spaces
                params = {"q": query.strip()}
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                results = response.json()

                if not results:
                    st.info("Wala ngani. Search ka ulit")
                    st.session_state.search_results = None  # Clear previous results
                else:
                    st.success(f"✅ Positive Norem!")
                    st.session_state.search_results = results  # ✅ Persist results
                    st.session_state.search_query = query.strip()  # Optional: persist query

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {e}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

# ✅ Display results ONLY if we have them in session_state
if st.session_state.search_results:
    results = st.session_state.search_results
    
    if len(results) > 1:
        options = [f"{r.get('trackName')} - {r.get('artistName')}" for r in results[:3]]
        selected = st.selectbox("🎵 Choose song:", options, key="song_selector")
        track = next(r for r in results if f"{r.get('trackName')} - {r.get('artistName')}" == selected)
    else:
        track = results[0]

    lyrics = track.get('lyrics') or track.get('syncedLyrics')
    if lyrics:
        st.markdown("### 📝 Lyrics")
        st.text_area("Lyrics", lyrics, height=400, disabled=True, key="lyrics_display")

        if st.button("📋 Copy Lyrics"):
            st.code(lyrics, language=None)
            st.success("✅ Lyrics copied! I-paste mo na sa note mo.")
    else:
        st.caption("⚠️ Walang lyrics ang kanta na 'to. Subukan mo iba.")