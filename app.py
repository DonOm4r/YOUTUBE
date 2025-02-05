import streamlit as st
from pytubefix import YouTube
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Descargar Audio de YouTube", page_icon="🎵", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_audio(url):
    buffer = BytesIO()
    video = YouTube(url)
    # Ordenar los flujos de audio por tasa de bits en orden descendente y seleccionar el de mayor calidad
    audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
    audio_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return video.title, audio_stream.abr, audio_stream.mime_type, buffer

def main():
    st.title("Descargar Audio de YouTube")
    url = st.text_input("Introduce la URL del video de YouTube:")
    if url:
        with st.spinner("Descargando audio..."):
            titulo, bitrate, mime_type, buffer = descargar_audio(url)
        st.subheader("Título del Video")
        st.write(titulo)
        st.subheader("Calidad del Audio")
        st.write(f"Tasa de bits: {bitrate}")
        st.write(f"Tipo MIME: {mime_type}")
        nombre_archivo = Path(titulo).with_suffix(".mp3").name
        st.subheader("Escuchar Audio")
        st.audio(buffer, format='audio/mpeg')
        st.subheader("Descargar Archivo de Audio")
        st.download_button(
            label="Descargar MP3",
            data=buffer,
            file_name=nombre_archivo,
            mime="audio/mpeg"
        )

if __name__ == "__main__":
    main()
