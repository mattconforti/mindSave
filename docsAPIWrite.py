"""
docsAPIWrite.py - write to the Google Docs file 'mindQuery.docx' using the batchUpdate method
By: Matt Conforti (with code from https://developers.google.com/docs/api/quickstart/python **check out Apache License)
6/20/19
"""


# imports -------
from docsAPIConnect import getCredentials

from googleapiclient.discovery import build


# global vars
DOCUMENT_ID_QUERY = '1MdJ4btEMOOOeLpcWT3-Vah826EnutaoodvHlJvISXpI'


# functions -------
def getWriteData(dataDict):
    """
    Gets the data to write to the Google Doc by parsing the PATTERN_MATCH_DICT
    and formulating responses to output
    :param dataDict: the key value pairings of patterns to thoughts they match
    :return dictVals: the values to write out as a result of
    seeing which question was asked and what the answer is (parsing PATTERN_MATCH_DICT)
    """
    # update this to form a more natural response, not just return the original thought
    dictVals = dataDict.values()
    return list(dictVals)


def writeToDoc(offset, writeString):
    """
    Uses the Google Docs API to send write requests to the doc.
    Must use the 'BatchUpdate' method to send list of requests and return the results
    :param offset: the amt of characters to offset the insert location (size of query we are answering)
    :param writeString: the text we are inserting - the answer to our query
    :return result: the result list from the 'batchUpdate' method
    """
    # give the list of requests
    requests = [
        {
            'insertText': {
                'location': {
                    'index': offset,  # the location to insert - amt of chars offset
                 },
                'text': writeString  # the data to write out
            }
        },
    ]
    # set up doc connection
    credentials = getCredentials()
    service = build('docs', 'v1', credentials=credentials)
    # get result from batchUpdate
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID_QUERY, body={'requests': requests}).execute()
    return result
