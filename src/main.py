# File: main.py
import streamlit as st
from pages.simulation import simulation_page
from translations import get_text

def initialize_session_state():
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 'level_1'
    

def main():
    # Initialize session state before anything else
    initialize_session_state()
    
    st.set_page_config(
        page_title=get_text('title', st.session_state.language),
        page_icon="📦",
        layout="wide"
    )
    
    # Language selector in sidebar
    lang_names = {
        'en': 'English',
        'es': 'Español',
        'pt': 'Português'
    }
    
    selected_lang = st.sidebar.selectbox(
        "Language / Idioma",
        options=list(lang_names.keys()),
        format_func=lambda x: lang_names[x],
        key='language'
    )
    
    
    simulation_page()

if __name__ == "__main__":
    main()