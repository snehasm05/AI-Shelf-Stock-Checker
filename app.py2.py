from google import genai 
from google.genai import types
import streamlit as st
from prompt import system_prompt,welcome_message_prompt,summary_request_prompt
import smtplib
from email.mime.text import MIMEText

GEMINI_API_KEY=st.secrets["GEMINI_API_KEY"]
genai.Client(api_key=GEMINI_API_KEY)
Model_Name = "gemini-3.5-flash"

st.set_page_config(page_title="Shelf Stock Checker", page_icon="📦🔍")
 
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]
 
 
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)
gemini_client = get_gemini_client()

 



def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])
 

def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"
 
 
 
 
def send_email(to_address, subject, body):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(message)
 

def send_email(to_address, subject, body):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(message)

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = GEMINI_API_KEY)
gemini_client = get_gemini_client()

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# step 1: onbroading(username and phone)

if not st.session_state.onboarded:

    st.title("Stock Checker 📦🔍")
    st.caption("Snap it. Scan it. Know your stock. Make smarter inventory decisions. 📸🔍📦🚀")

    with st.form("onboarding_form"):

        name = st.text_input("Your Name")

        email_address = st.text_input(
             "Email Address",
              placeholder="example@gmail.com",
              help="This is the email address where Stock Checker will send the summary"
        )
        

        submitted = st.form_submit_button("Let's Go!!")

    if submitted:
        
        if not name.strip() or not email_address.strip():
            st.warning("Please Fill Your Name and Email Address")
        else:
            st.session_state.name = name.strip()
            st.session_state.email_address = email_address.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=Model_Name,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
            )

            st.session_state.messages = []
            st.session_state.onboarded = True

            st.rerun()

    st.stop()
# create chat interface 
header_col, button_col = st.columns([5, 2], vertical_alignment="center")
 
with header_col:
    st.title("Shelf Stock Checker 📦🔍")
 

with button_col:
    send_disabled = len(st.session_state.messages) <= 2

    if st.button("📧 Send to Gmail", disabled=send_disabled, use_container_width=True):
        with st.spinner("Preparing your stock summary..."):
            summary = ask_gemini([summary_request_prompt])

        try:
            send_email(
                st.session_state.email_address,
                "Shelf Stock Checker - Stock Summary",
                summary
            )
            st.success("Sent! Check your Gmail 📧")
        except Exception as error:
            st.error(f"Couldn't send the email: {error}")
st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.email_address}")


if not st.session_state.messages:
    add_message("assistant", "text", welcome_message_prompt.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)
user_input = st.chat_input(
    "Ask a question, or attach a photo of your Shelf ",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)
if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []
 
    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("What is this Shelf Stock? ")
 
    with st.spinner("Crunching the numbers..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)
 

