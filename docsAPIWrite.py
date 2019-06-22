"""
docsAPIWrite.py - write to the Google Docs file 'mindQuery.docx' using the batchUpdate method
By: Matt Conforti (with code from https://developers.google.com/docs/api/quickstart/python **check out Apache License)
6/20/19
"""


# imports -------
from docsAPIConnect import DOCUMENT_ID
from docsAPIConnect import getCredentials

from mindQuery import PATTERN_MATCH_DICT

from googleapiclient.discovery import build


# functions -------
def main():
    credentials = getCredentials()
    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    print()


def getWriteData(dataDict):
    """
    Gets the data to write to the Google Doc by parsing the PATTERN_MATCH_DICT
    and formulating responses to output
    :param dataDict: the key value pairings of patterns to thoughts they match
    :return returnString: the response to write out as a result of
    seeing which question was asked and what the answer is (parsing PATTERN_MATCH_DICT)
    """
    pass


def writeToDoc(document):
    pass


# main code -------
if __name__ == '__main__':
    main()
