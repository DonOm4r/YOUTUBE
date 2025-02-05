import streamlit as st
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
from io import BytesIO
from pathlib import Path
import time

st.set_page_config(page_title="Descargar Audio de YouTube", page_icon="🎵", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def descargar_audio(url, clientes=None, espera_reintento=5):
    if clientes is None:
        clientes = ['WEB_CREATOR', 'TV', 'ANDROID', 'IOS', 'MWEB']
    buffer = BytesIO()
    for intento, cliente in enumerate(clientes, start=1):
        try:
            video = YouTube(url, client=cliente)
            audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
            audio_stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return video.title, audio_stream.abr, audio_stream.mime_type, buffer
        except VideoUnavailable:
            st.warning(f"El video no está disponible con el cliente '{cliente}'. Reintentando con otro cliente ({intento}/{len(clientes)})...")
            time.sleep(espera_reintento)
    st.error("No se pudo descargar el audio después de probar con todos los clientes disponibles.")
    return None, None, None, None

def main():
    st.title("Descargar Audio de YouTube")
    url = st.text_input("Introduce la URL del video de YouTube:")
    if url:
        with st.spinner("Descargando audio..."):
            titulo, bitrate, mime_type, buffer = descargar_audio(url)
        if titulo:
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
