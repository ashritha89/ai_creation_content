import streamlit as st
from datetime import datetime

def create_download_link(content: str, filename: str = None) -> str:
    if filename is None:
        filename = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    return st.download_button(
        label="⬇️ Download Content",
        data=content,
        file_name=filename,
        mime="text/plain"
    )
