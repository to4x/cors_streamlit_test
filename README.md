# Streamlit Iframe Starter

This project is a minimal Streamlit app that embeds another website using an iframe.
It is prepared for deployment on Streamlit Community Cloud.
It also includes a browser popup test that executes `window.open(...)`.

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