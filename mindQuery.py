"""
mindQuery.py - query the mindSave database to get a list of
potential data to return to the user
By: Matt Conforti
6/14/19
"""


# imports -----------------------------
import string
import re
from mindSaveDb import getData
from mindSaveDb import createConnection


# global vars -----------------------------
DOCUMENT_ID_QUERY = '1MdJ4btEMOOOeLpcWT3-Vah826EnutaoodvHlJvISXpI'
NON_SEARCH_WORDS = ['the', 'is']
RETURN_PHRASE_BUILDERS = ['who', 'what', 'how', 'when', 'where', 'why', 'do', 'i', 'you', 'he', 'my',
                          'would', 'they']
RETURN_PHRASE_BUILDER_TYPES = {'who': 'string', 'when': 'datetime'}
PATTERN_MATCH_DICT = {}  # which thoughts match our patterns - need duplicate keys


# functions -----------------------------
def main():
    print('\n*****************************\n')
    queryList = getData(DOCUMENT_ID_QUERY)
    searchPatterns = []
    for query in queryList:
        if query != '':  # skip blank lines
            print('Query: ', query)
            searchPattern = createSearchPattern(query)
            print('Search Pattern: ', searchPattern, '\n')
            searchPatterns.append(searchPattern)
    dbConnection = createConnection('/Users/mattconforti/Desktop/CSC/Python/mindSave/mindSaveDb.sql')
    if dbConnection is not None:
        with dbConnection:
            thoughtList = dbRead(dbConnection)
            for thought in thoughtList:  # for every thought there is x amt of patterns to apply
                for pattern in searchPatterns:
                    # if the pattern is a match to the thought, return the thought
                    isMatch = searchInStoredString(pattern, thought)
                    if isMatch:
                        PATTERN_MATCH_DICT[pattern] = thought
            print('Search results:\n')
            print(PATTERN_MATCH_DICT)
    print('\n*****************************')


def dbRead(connection):
    """
    Reads the Db and extracts each thought
    :return thoughtList: the list of thoughts read
    """
    thoughtList = []
    selectThoughts = 'SELECT thought FROM thoughts ORDER BY datetime ASC'
    cursor = connection.cursor()
    cursor.execute(selectThoughts)
    print('\nDb read executed...\n')
    rows = cursor.fetchall()  # returns a list of tuples
    for row in rows:
        row = str(row).strip('(').strip(')').strip(',').strip('\'')
        thoughtList.append(row)
    return thoughtList


def createSearchPattern(queryString):
    """
    Creates a regular expression from a regular language string
    in order to search our data for 'key-word' matches
    :param queryString: the string from the queryList which will be used to pattern match
    :return regExPattern: the regular expression derived for the search
    """
    regExPattern = ''
    words = queryString.split(' ')
    searchWords = []
    for word in words:
        word = word.lower()  # clean each word for use in the search
        word = word.translate(str.maketrans('', '', string.punctuation))
        if word not in NON_SEARCH_WORDS:  # remove words not useful for searching
            if word not in RETURN_PHRASE_BUILDERS:
                searchWords.append(word)
    for w in searchWords:
        if w == searchWords[-1]:  # if the search word is the last in the list - no '|'
            regExPattern += w
        else:
            regExPattern += w + '|'
    return regExPattern


def searchInStoredString(pattern, storedString):  # do we need this or should we use the pattern above
    # in a selection statement before we even read the data in (call dbRead())
    """
    Uses regular expressions to tell us if a stored string matches a pattern
    :param pattern: the regular expression pattern
    :param storedString: the thoughts read from the database
    :return isMatch: a boolean which tells if the string matches the pattern
    """
    isMatch = re.search(pattern, storedString)
    return isMatch


# main code -----------------------------
if __name__ == '__main__':
    main()
