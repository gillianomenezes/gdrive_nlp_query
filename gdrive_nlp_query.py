import os
import sys

import spacy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up Google Drive API
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "secrets/credentials.json"  # Replace with your credentials file
AUTHORIZED_USER_FILE = "secrets/token.json"


def get_query():
    # Get the command-line arguments
    args = sys.argv[1:]

    # Check if there are any arguments
    if not args:
        print("Usage: python script.py [arg1] [arg2] ...")
        return

    return args


def get_user_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(AUTHORIZED_USER_FILE):
        creds = Credentials.from_authorized_user_file(AUTHORIZED_USER_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SERVICE_ACCOUNT_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(AUTHORIZED_USER_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def get_service(credentials):
    try:
        return build("drive", "v3", credentials=credentials)
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return


def get_user_files(service):
    try:
        # Set the MIME type to filter by
        mime_type = "application/vnd.google-apps.document"

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                pageSize=10,
                q=f"mimeType='{mime_type}'",
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        return results.get("files", [])
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


def download_document(file_id, destination_path, drive_service):
    request = drive_service.files().export_media(fileId=file_id, mimeType="text/plain")
    with open(destination_path, "wb") as file:
        file.write(request.execute())


def process_document(file_path, query):
    with open(file_path, "r", encoding="utf-8") as file:
        document_content = file.read()

    # Perform natural language query
    # Set up spaCy for natural language processing
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(document_content)

    for word in query:
        matches = [sent.text for sent in doc.sents if word in sent.text.lower()]

        if matches:
            print(f"Matches in document {file_path}:")
            for match in matches:
                print(match)
        else:
            print(f'No matches found in document {file_path} for word "{word}"')


def main():
    query = get_query()

    credentials = get_user_credentials()

    drive_service = get_service(credentials)

    documents = get_user_files(drive_service)

    for document in documents:
        document_id = document["id"]
        document_name = document["name"]
        document_path = f"temp/{document_name}.txt"

        # Download document
        download_document(document_id, document_path, drive_service)

        # Process document and print matches
        process_document(document_path, query)

        # Optionally, you can remove the downloaded document
        os.remove(document_path)


if __name__ == "__main__":
    main()
