#!/usr/bin/env python3
"""
Test script to verify sidebar works on Streamlit Cloud
"""

import streamlit as st

st.set_page_config(
    page_title="Sidebar Cloud Test",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("☁️ Streamlit Cloud Sidebar Test")

# Test sidebar
st.sidebar.markdown("## 🧪 Sidebar Test")
st.sidebar.success("If you can see this on Streamlit Cloud, the sidebar is working!")

st.sidebar.markdown("---")

input_type = st.sidebar.radio(
    "Choose input type:",
    ["📝 Text Input", "📷 Image Upload"],
    help="Test radio button"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Tips:")
st.sidebar.markdown("- This is a test for Streamlit Cloud")
st.sidebar.markdown("- Sidebar should be visible")
st.sidebar.markdown("- Radio button should work")

# Main content
st.markdown("### Main Content")
st.info(f"You selected: {input_type}")

if input_type == "📝 Text Input":
    st.text_area("Enter text:", placeholder="Type something here...")
elif input_type == "📷 Image Upload":
    st.file_uploader("Upload image:", type=['png', 'jpg', 'jpeg'])

st.success("✅ Test completed! If you can see the sidebar and interact with it, everything is working on Streamlit Cloud.")
