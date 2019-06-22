"""
docsAPIConnect.py - connect to our Google Docs file 'mindSave.docx'
By: Matt Conforti (with code from https://developers.google.com/docs/api/quickstart/python **check out Apache License)
6/13/19
"""


# imports -----------------------------
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# global vars -----------------------------
# If modifying these authorization scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of the google doc.
DOCUMENT_ID = '1-UuXZI-n0p9bA_IZQlIqeQfMKlljudfuhzk_ha_APF8'


# functions -----------------------------
def main():
    creds = getCredentials()
    service = build('docs', 'v1', credentials=creds)
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    printContents(document)


def getCredentials():
    """
    Gets credentials using Google API Client Libraries and a pickle module
    :return creds: the credentials associated with the Google doc in question
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def printContents(document):
    """
    Prints the contents of the Google doc
    :param document: the document Object
    """
    print('\n*****************************')
    print('\nThe title of the document is: {}'.format(document.get('title')))
    print('\n*****************************')
    print('\nThe document reads: \n\n{}'.format(extractContents(document)))
    print('\n*****************************')


def readParagraphElem(element):
    """
    Extracts the text from a 'textRun' element
    :param element: the structural element of the bodyJsonString
    :return textRun.get('content'): the content of the textRun:
    """
    textRun = element.get('textRun')
    if not textRun:
        return ''
    return textRun.get('content')


def extractContents(document):
    """
    Parses recursively through a JSON string of structural elements to find the text of the document
    :param document: the Google Doc
    :return contents: the contents (text) of the document body
    """
    contents = ""
    bodyJsonString = document.get('body').get('content')
    for element in bodyJsonString:  # for each structural element
        if 'paragraph' in element:
            paragraphElements = element.get('paragraph').get('elements')
            for elem in paragraphElements:
                contents += readParagraphElem(elem)
    return contents.strip()  # rids of excess whitespace


# main code -----------------------------
if __name__ == '__main__':
    main()
