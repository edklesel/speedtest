import os
from datetime import datetime as dt
from sqlite3 import connect
import logging

logger = logging.getLogger('speedtest')

class Connection():

    def __init__(self, database):
        self.database = database

    def __enter__(self):
        logger.debug(f'Opening database connection to {self.database}...')
        self.conn = connect(self.database)
        logger.debug('Connection established.')
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        logger.debug(f'Closing connection to {self.database}...')
        self.conn.close()
        logger.debug(f'Database connection closed.')

    def execute(self, query):
        logger.debug(f'Executing query: {query}')
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor

    def executescript(self, query):
        logger.debug(f'Executing script: {query}')
        self.cursor.executescript(query)
        self.conn.commit()
        return self.cursor

def initialise_db():
    if not os.path.exists('speedtest.db'):
        logger.debug('Inisialising database speedtest.db.')
        with Connection('speedtest.db') as c, open(os.path.join('Speedtest','Queries','table_speeds.sql')) as f:
            c.executescript(f.read())


def record_speed(download: float, upload: float, datetime=dt.now()):

    query = f"""
    INSERT INTO Speeds (dtDateTime, fUploadSpeed, fDownloadSpeed) VALUES
    ('{datetime}', {upload}, {download})
    """

    try:
        logger.debug('Inserting speeds into database.')
        with Connection('speedtest.db') as c:
            c.execute(query)
            logger.debug('Query executed successfully.')
    except :
        logger.exception('Error inserting speed data into the database.')