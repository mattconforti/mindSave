"""
docsAPIWrite.py - write to the Google Docs file 'mindQuery.docx' using the batchUpdate method
By: Matt Conforti (with code from https://developers.google.com/docs/api/quickstart/python **check out Apache License)
6/20/19
"""


# imports -------


# functions -------

def getWriteData(dataDict):
    """
    Gets the data to write to the Google Doc by parsing the PATTERN_MATCH_DICT
    and formulating responses to output
    :param dataDict: the key value pairings of patterns to thoughts they match
    :return returnString: the response to write out as a result of
    seeing which question was asked and what the answer is (parsing PATTERN_MATCH_DICT)
    """
    # update this to form a more natural response, not just return the original thought
    dictVals = dataDict.values()
    return dictVals


def writeToDoc(document):
    pass

