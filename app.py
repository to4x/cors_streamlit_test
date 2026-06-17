import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Embedded Site Viewer", layout="wide")

st.title("Embedded Site Viewer")
st.caption("Embed an external site in an iframe.")

with st.sidebar:
    st.header("Iframe Settings")
    target_url = st.text_input("Target URL", value="", placeholder="https://example.com")
    height = st.slider("Iframe height", min_value=400, max_value=1400, value=800, step=50)
    scrolling = st.toggle("Enable scrolling", value=True)

st.info(
    "Some websites cannot be embedded in an iframe because of security headers such as "
    "X-Frame-Options or Content-Security-Policy."
)

if not target_url:
    st.warning("Enter a target URL in the sidebar to render the iframe.")
else:
    if target_url.startswith(("http://", "https://")):
        components.iframe(target_url, height=height, scrolling=scrolling)
    else:
        st.error("Please enter a valid URL that starts with http:// or https://")
