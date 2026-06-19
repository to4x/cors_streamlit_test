# Streamlit CORS & WebSocket Security Testing Tool

This project is a comprehensive Streamlit app for testing iframe embedding, popup windows, cross-window messaging (postMessage), and WebSocket connections. It includes built-in validation and diagnostics to help identify CORS issues, security headers problems, and Cross-Site WebSocket Hijacking (CSWSH) vulnerabilities.

## Features

### postMessage Testing
- **Iframe Embedding**: Embed external websites with configurable height and scrolling
- **Popup Testing**: Test `window.open()` with configurable security settings
- **postMessage Testing**: Validate cross-window messaging with origin validation
- **Security Controls**: Toggle opener references and test XSS payloads

### WebSocket Testing (CSWSH)
- **WebSocket Connection Testing**: Test cross-origin WebSocket connections
- **CSWSH Vulnerability Detection**: Identify Cross-Site WebSocket Hijacking risks
- **Cookie Inclusion Validation**: Check if session cookies are sent in handshake
- **Origin Header Testing**: Verify server-side origin validation
- **Bidirectional Communication**: Test data send/receive capabilities
- **Persistent Connection Analysis**: Validate ongoing access vulnerabilities

### WebSocket Relay Attack (Advanced)
- **Popup-Proxied WebSocket**: Test if popup can establish WS using victim's session
- **Data Relay via postMessage**: Monitor WebSocket data relayed through popup
- **Command Injection**: Test if attacker can send commands through popup proxy
- **Session Hijacking**: Validate complete session takeover via popup channel
- **CORS Bypass**: Demonstrate how popup same-origin access bypasses protections

### Diagnostics & Validation
- **Real-time Validation**: Built-in diagnostics for both postMessage and WebSocket
- **Security Indicators**: Live status for connections, messages, and cookies
- **Troubleshooting Guide**: In-app help for common issues

## Files

- `app.py`: Streamlit app with configurable iframe URL and height.
- `app.py`: Streamlit app with configurable iframe URL/height and a `window.open(...)` popup test.
- `requirements.txt`: Python dependencies for local run and cloud deployment.

## Local Run

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Start the app:

	```bash
	streamlit run app.py
	```

## Deploy To Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to Streamlit Community Cloud and create a new app.
3. Select your repository, branch, and set the main file path to `app.py`.
4. Deploy.

## Important Iframe Limitation

Some websites cannot be embedded because they send security headers like:

- `X-Frame-Options: DENY` or `SAMEORIGIN`
- restrictive `Content-Security-Policy` (`frame-ancestors`)

If that happens, the iframe will be blocked by the browser even if the Streamlit code is correct.

## Popup Test Notes (`window.open`)

- The app includes a "Popup Test" section with a button that runs `window.open("https://...")`.
- Popup opening is browser-policy dependent and may be blocked unless triggered by a direct user click.
- If blocked, the UI shows a status message so you can quickly verify popup policy behavior.

## Validation & Testing Features

### Real-time Status Indicators
- **Iframe Status**: Detects if running in iframe or standalone mode
- **Popup Status**: Live tracking of popup window state (open/closed)
- **Message Counter**: Tracks number of postMessages received

### Validation Tests
The app includes comprehensive validation tests accessible via the "Run Validation" button:

1. **Iframe Context Detection**: Verifies execution environment
2. **Popup State**: Checks if popup window is accessible
3. **Opener Reference**: Validates window.opener relationship
4. **Message Reception**: Confirms postMessage communication
5. **Origin Validation**: Verifies expected vs actual message origins

### Testing Workflow

1. **Configure Settings** (in sidebar):
   - Set target URL for iframe
   - Set popup URL (can be same or different)
   - Configure target origin for postMessage
   - Toggle security settings (opener link, XSS test payload)

2. **Open Popup**:
   - Hover over the "Open popup" button
   - Check validation status for success/errors
   - Watch the log for detailed diagnostics

3. **Send Messages**:
   - Click "Send postMessage" button
   - Verify message appears in log
   - Check origin validation results

4. **Run Validation**:
   - Click "Run Validation" for comprehensive diagnostics
   - Review all test results in the log
   - Use troubleshooting guide for issues

### Troubleshooting Common Issues

**Popup Blocked**
- Browser may require explicit popup permission
- User interaction (hover) is required
- Check browser settings/permissions

**CORS Errors**
- Set target origin to `*` for initial testing
- Verify target site allows cross-origin messages
- Check browser console for specific CORS errors

**No Messages Received**
- Ensure target origin matches exactly (including protocol)
- Verify target site actually sends postMessage
- Use validation to check message listener setup

**Opener Reference Lost**
- Enable "Keep opener link" toggle
- Note: This is a security risk in production
- Some browsers may still block based on policy

### Log Indicators

The validation log uses symbols to indicate status:
- `✓` Success - Operation completed successfully
- `✗` Error - Operation failed
- `⚠` Warning - Potential issue detected
- `ℹ` Info - General information

Each log entry includes a timestamp for tracking event sequences.

## WebSocket (CSWSH) Testing

### What is CSWSH?

Cross-Site WebSocket Hijacking (CSWSH) is a vulnerability where an attacker can:
1. Open a WebSocket connection from a malicious site to a vulnerable target
2. Leverage the victim's session cookies sent automatically in the handshake
3. Establish a persistent bidirectional connection
4. Send commands and read sensitive real-time data

### Testing for CSWSH

1. **Configure WebSocket URL** (in sidebar):
   - Enter the WebSocket endpoint (e.g., `wss://target-app.com/api/stream`)
   - For Streamlit apps: `ws://localhost:8501/_stcore/stream`
   - Configure test message to send after connection

2. **Connect to WebSocket**:
   - Click "Connect WebSocket" button
   - Tool automatically checks for session cookies
   - Attempts connection from different origin
   - Monitors connection establishment

3. **Run CSWSH Validation**:
   - Click "Run CSWSH Tests" for comprehensive assessment
   - Checks 4 vulnerability indicators:
     - Origin header validation
     - Cookie inclusion in handshake
     - Bidirectional communication capability
     - Persistent connection maintenance

4. **Interpret Results**:
   - 🔴 **Vulnerable**: Connection established despite different origin
   - ✓ **Secure**: Connection rejected or origin validated
   - ⚠ **Warning**: Partial security measures detected

### Mitigation Recommendations

If CSWSH vulnerability is detected:
- **Validate Origin header** during WebSocket handshake
- **Require CSRF tokens** for WebSocket connections
- **Check authentication** before upgrading to WebSocket
- **Use SameSite=Strict cookies** to prevent cross-site inclusion
- **Implement custom authentication** beyond cookies

### Streamlit-Specific Notes

Streamlit uses WebSockets internally for app communication:
- Development: `ws://localhost:8501/_stcore/stream`
- Production: `wss://your-app.streamlit.app/_stcore/stream`

Testing your Streamlit app's WebSocket endpoint helps identify if it's vulnerable to CSWSH attacks.

## WebSocket Relay Attack (Advanced)

### What is WebSocket Relay Attack?

This is a **more sophisticated and dangerous** variant of CSWSH that combines popup-based session access with WebSocket hijacking.

**Attack Flow:**
```
Attacker Site (evil.com)
    ↓ window.open() with opener
Victim Site Popup (target-app.com)
    ↓ Establishes WebSocket
Target WebSocket Server (target-app.com/ws)
    ↑ All data relayed via postMessage
Attacker Site receives proxied data
```

### Why It's More Dangerous Than Direct CSWSH

| Direct CSWSH | Popup-Proxied WebSocket Relay |
|--------------|-------------------------------|
| Blocked if origin validated | **Bypasses origin check** (popup is same-origin) |
| Requires cookies from attacker's origin | **Uses victim's legitimate session** |
| Often detectable by monitoring | **Appears as legitimate traffic** |
| Limited by CORS restrictions | **No CORS restrictions** (same-origin popup) |
| Single attack attempt | **Persistent bidirectional channel** |

### Testing WebSocket Relay Attack

1. **Enable in Sidebar**:
   - Toggle "Enable WebSocket relay via popup"
   - Set popup URL (should be target application)
   - Set WebSocket URL for relay

2. **Execute Attack Simulation**:
   - Click "Open Relay Popup" → Opens victim site with opener reference
   - Click "Inject WS Relay Code" → Attempts to inject relay script
   - Monitor log for relayed WebSocket messages
   - Click "Send Command via Popup" → Test command injection

3. **Observe Attack Components**:
   - **Session Inheritance**: Popup shares victim's cookies
   - **WebSocket Establishment**: Popup connects using victim's session
   - **Data Exfiltration**: All WS messages relayed via postMessage
   - **Command Injection**: Attacker sends commands through popup proxy

4. **Interpret Results**:
   - 💀 **Critical Vulnerability**: If messages are relayed successfully
   - ✓ **Protected**: If opener reference blocked or injection fails
   - ⚠ **Partial Protection**: If some but not all attack steps succeed

### Real-World Impact

This attack is particularly dangerous for:
- **OAuth/OIDC flows**: Popup-based authentication with WebSocket callbacks
- **Real-time collaboration**: Shared documents, whiteboards, code editors
- **Financial platforms**: Trading terminals with live market data
- **Chat applications**: Messaging systems with WebSocket connections
- **Live dashboards**: Monitoring systems with real-time updates
- **Gaming platforms**: Multiplayer games with WebSocket state sync

### Mitigation Strategies

**Essential Protections:**
1. **Always use `noopener,noreferrer`** for all `window.open()` calls
2. **Validate WebSocket Origin header** during handshake
3. **Implement CSRF tokens** for WebSocket connections
4. **Use SameSite=Strict cookies** to prevent cross-site cookie inclusion
5. **Additional authentication** beyond cookies for sensitive WebSocket endpoints
6. **Monitor cross-window communication** patterns for anomalies

**Code Example:**
```javascript
// Safe popup opening
window.open(url, '_blank', 'noopener,noreferrer');

// WebSocket handshake validation (server-side)
if (origin !== expectedOrigin) {
  connection.close(1008, 'Origin not allowed');
  return;
}
```

### Cross-Origin Restrictions

**Note**: The relay attack demonstration may be blocked by cross-origin restrictions if:
- Popup URL is different origin than testing site
- Content Security Policy blocks script injection
- Browser security features prevent cross-window access

**The attack succeeds when:**
- Popup is same-origin as attacker site
- Or attacker controls both sites
- Or browser extension is used for injection

This tool demonstrates the **concept and detection** of the vulnerability. Real-world exploitation would work when attacker and victim origins align or attacker has code execution capability.