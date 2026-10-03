# Shelf Stock Checker 📦🔍

Shelf Stock Checker is an AI-powered vision chatbot that helps analyze shelf images for inventory information.

## What the app does

* 📸 Upload a clear shelf image
* 🔍 Detect visible products or items
* 📦 Identify visible quantities when possible
* ⚠️ Find items that appear to be low in stock
* ⬜ Identify empty shelf spaces
* 📍 Detect possible misplaced items
* 💬 Ask questions about the uploaded shelf
* 📧 Send a stock summary to Gmail

## Technologies Used

* Python
* Streamlit
* Google GenAI
* Gmail SMTP

## How to run locally

1. Clone or download this repository.

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create `.streamlit/secrets.toml` and add your own API credentials.

4. Run the Streamlit app:

```bash
python -m streamlit run app.py2.py
```

5. Open the local Streamlit URL shown in the terminal.

## Important

Never upload your real `.streamlit/secrets.toml` file or expose API keys and Gmail App Passwords publicly.

Use `.streamlit/secrets.toml.example` as a template for the required secrets.
