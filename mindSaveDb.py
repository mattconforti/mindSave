"""
mindSaveDb.py - the main mindSave file
By: Matt Conforti
6/13/19
"""


# imports -----------------------------
import sqlite3
from sqlite3 import Error

from docsAPIConnect import DOCUMENT_ID
from docsAPIConnect import getCredentials
from docsAPIConnect import extractContents

from googleapiclient.discovery import build


# functions -----------------------------
def main():
    dbConnection = createConnection('/Users/mattconforti/Desktop/CSC/Python/mindSave/mindSaveDb.sql')
    if dbConnection is not None:
        with dbConnection:
            createTable(dbConnection)
            insertData = getData(DOCUMENT_ID)
            for item in insertData:
                if item != '':  # skip any potential blank lines
                    dbWrite(dbConnection, item)  # write each line of the doc to our database table
        closeConnection(dbConnection)


def createConnection(dbFile):
    """
    Creates an sqlite3 database connection using the given dbFile
    :param dbFile: the database file to be connected to
    :return connection: a connection object
    """
    try:
        print('\n*****************************')
        print('\nEstablishing connection...')
        connection = sqlite3.connect(dbFile)
        print('\nDatabase connection established!')
        print('\n*****************************')
        return connection
    except Error as e:
        print('Error: ', e)
    return None


def closeConnection(dbConnection):
    print('\nClosing connection...')
    dbConnection.close()
    print('\nConnection closed!')
    print('\n*****************************')


def createTable(dbConnection):
    sqlCreateTable = 'CREATE TABLE IF NOT EXISTS thoughts ( thought text PRIMARY KEY, datetime text NOT NULL );'
    try:
        cursor = dbConnection.cursor()
        cursor.execute(sqlCreateTable)
        print('\nTable created successfully!')
        print('\n*****************************')
    except Error as e:
        print('Error: ', e)


def getData(docID):
    creds = getCredentials()
    service = build('docs', 'v1', credentials=creds)
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=docID).execute()
    thoughtList = extractContents(document).split("\n")
    return thoughtList


def dbWrite(dbConnection, Data):
    sqlDataInsert = 'INSERT INTO thoughts values ( \'' + Data + '\', datetime(\'now\', \'localtime\') );'
    try:
        cursor = dbConnection.cursor()
        cursor.execute(sqlDataInsert)
        print('\nDatabase write successful!')
        print('\n*****************************')
    except Error as e:
        print('Error: ', e)


# main code -----------------------------
if __name__ == '__main__':
    main()
