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