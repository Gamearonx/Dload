
import streamlit as st
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip

st.title("🎬 YouTube Video Downloader & Converter")

url = st.text_input("Paste YouTube video URL here")

if url:
    try:
        yt = YouTube(url)
        st.video(yt.watch_url)
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Length:** {yt.length // 60} min {yt.length % 60} sec")

        # Filter for progressive streams (video + audio)
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        # Create a list of unique resolutions for the dropdown
        resolutions = [stream.resolution for stream in streams]
        selected_res = st.selectbox("Choose resolution:", resolutions)

        # Get the stream that matches the selected resolution
        selected_stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_res).first()

        filename = f"{yt.title}.mp4"

        if st.button("Download Video"):
            with st.spinner("Downloading video..."):
                selected_stream.download(filename=filename)
                st.success(f"Video downloaded: {filename}")

        if st.button("Convert to MP3"):
            with st.spinner("Downloading and converting to MP3..."):
                video_path = selected_stream.download(filename=filename)
                mp3_filename = f"{yt.title}.mp3"
                video_clip = VideoFileClip(video_path)
                video_clip.audio.write_audiofile(mp3_filename)
                video_clip.close()
                st.success(f"Conversion complete: {mp3_filename}")
    except Exception as e:
        st.error(f"Error: {e}")
