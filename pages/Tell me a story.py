import streamlit as st

def tell_story():
    st.audio("assets/example.mp3", format='audio/mp3')

tell_story()