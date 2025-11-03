import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.markdown(
    """
    <h1 style='text-align:center; color:#1DB954;'>🎧 Spotify Song Insights</h1>
    <p style='text-align:center; color:gray;'>Search and visualize a song’s key audio features</p>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("📂 Upload your Spotify dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# Required columns
required_cols = ['track_name', 'artists', 'album_name', 'track_genre', 'danceability', 'energy', 'valence', 'tempo', 'popularity', 'duration_ms']
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column in CSV: {col}")
        st.stop()

# ----------------------------
# SEARCH BAR
# ----------------------------
query = st.text_input("🔍 Search for a song")

if query:
    results = df[df['track_name'].str.contains(query, case=False, na=False)]

    if not results.empty:
        selected_row = st.selectbox(
            "Select a track:",
            results['track_name'] + " - " + results['artists']
        )

        track_info = results.loc[
            (results['track_name'] + " - " + results['artists']) == selected_row
        ].iloc[0]

        st.markdown("---")

        col1, col2 = st.columns([1, 1], gap="large")

        # ----------------------------
        # LEFT SIDE: TRACK DETAILS
        # ----------------------------
        with col1:
            st.markdown(
                f"""
                <div style='background-color:#181818; padding:20px; border-radius:15px; color:white;'>
                    <h2>{track_info['track_name']}</h2>
                    <p><strong>Artist:</strong> {track_info['artists']}</p>
                    <p><strong>Album:</strong> {track_info['album_name']}</p>
                    <p><strong>Genre:</strong> {track_info['track_genre']}</p>
                    <p><strong>Popularity:</strong> {track_info['popularity']}/100</p>
                    <p><strong>Tempo:</strong> {track_info['tempo']:.1f} BPM</p>
                    <p><strong>Duration:</strong> {round(track_info['duration_ms']/60000,2)} min</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------
        # RIGHT SIDE: COMPACT AUDIO GRAPH
        # ----------------------------
        with col2:
            st.markdown("<h3 style='color:#1DB954'>🎚️ Audio Attributes (0–100)</h3>", unsafe_allow_html=True)

            numeric_features = ['danceability', 'energy', 'valence', 'tempo']
            data = {}
            for f in numeric_features:
                val = track_info[f]
                if f == 'tempo':
                    val = min(val / 2, 100)  # scale tempo to 0-100
                else:
                    val = val * 100
                data[f.capitalize()] = round(val, 2)

            fig, ax = plt.subplots(figsize=(5, 2.5))
            bars = ax.bar(data.keys(), data.values(), color=['#1DB954', '#20C997', '#FFB347', '#69B3E7'])
            ax.set_ylim(0, 100)
            ax.set_ylabel("Value (0–100)", fontsize=10)
            ax.set_xlabel("Attributes", fontsize=10)
            ax.set_title("Audio Feature Comparison", fontsize=12, color="#1DB954", pad=10)

            # Add value labels
            for bar in bars:
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 2,
                    f"{bar.get_height():.0f}",
                    ha='center',
                    fontsize=9,
                    color='white'
                )

            ax.tick_params(colors='white')
            ax.set_facecolor("#121212")
            fig.patch.set_facecolor("#121212")
            for spine in ax.spines.values():
                spine.set_visible(False)

            st.pyplot(fig, use_container_width=False)

    else:
        st.warning("No songs found for that search.")
else:
    st.info("Type a song name above to begin.")
