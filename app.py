import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Embedded Site Viewer", layout="wide")

st.title("Embedded Site Viewer")
st.caption("Embed an external site in an iframe.")

with st.sidebar:
    st.header("Iframe Settings")
    target_url = st.text_input("Target URL", value="", placeholder="https://example.com")
    height = st.slider("Iframe height", min_value=400, max_value=1400, value=800, step=50)
    scrolling = st.toggle("Enable scrolling", value=True)

    st.header("Popup Test")
    popup_url = st.text_input(
        "Popup URL",
        value=target_url or "https://target-app.com",
        placeholder="https://target-app.com",
    )

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

st.divider()
st.subheader("window.open() Popup Test")
st.caption("Use this to verify popup behavior from Streamlit in your browser.")

if popup_url.startswith(("http://", "https://")):
    popup_url_js = json.dumps(popup_url)
    components.html(
        f"""
        <div style=\"font-family: sans-serif;\">
            <button id=\"open-btn\" style=\"padding: 0.5rem 0.8rem; cursor: pointer;\">Open target in new tab</button>
            <div id=\"status\" style=\"margin-top: 0.6rem; color: #444;\">Click the button to run window.open(...).</div>
        </div>
        <script>
            const btn = document.getElementById("open-btn");
            const status = document.getElementById("status");
            btn.addEventListener("click", () => {{
                const opened = window.open({popup_url_js}, "_blank", "noopener,noreferrer");
                if (opened) {{
                    status.textContent = "Popup opened successfully (or handed off to a new tab).";
                }} else {{
                    status.textContent = "Popup blocked by browser settings.";
                }}
            }});
        </script>
        """,
        height=120,
    )
else:
    st.error("Popup URL must start with http:// or https://")
