
import os
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permission to send emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    creds = None

    # Reuse saved login permission if available
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    # Login to Google if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Connect to Gmail
    service = build("gmail", "v1", credentials=creds)
    print("Gmail connected successfully!")

    # Get email details
    receiver = input("Enter receiver Gmail: ").strip()
    subject = input("Enter email subject: ")
    body = input("Enter your message: ")

    # Prepare email
    message = EmailMessage()
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    # Encode email for Gmail API
    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    # Send email
    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()

    print("\nEmail sent successfully!")
    print("Message ID:", result["id"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
