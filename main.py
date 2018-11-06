import speedtest
import logging
import os
import datetime
import mysql.connector
import sys
from json import loads

# Load the config
with open('config.json', 'r') as f:
    config = loads(f.read())

# Set up the logging config
logger = logging.getLogger('speedtest')
if config["logging"]["level"] == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif config["logging"]["level"] == "INFO":
    logger.setLevel(logging.INFO)
logDir = config["logging"]["location"]
logDate = str(datetime.datetime.now().date())
#logFile = f'speedtest_log_{logDate}.log'
logFile = config["logging"]["filename"].format(str(datetime.datetime.now().date()))

if not os.path.exists(logDir):
    os.makedirs(logDir)

fh = logging.FileHandler(logDir + logFile)
fh.setFormatter(logging.Formatter(config["logging"]["format"]))
logger.addHandler(fh)
logger.addHandler(logging.StreamHandler())

sptest = speedtest.Speedtest()

datetimenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logger.info('******************************************')
logger.info(f"Beginning speedcheck run - {datetimenow}")

# Create the .csv if it doesn't exist

csvfile = config["csv"]["location"] + config["csv"]["filename"]

if not os.path.exists(config["csv"]["location"] + config["csv"]["filename"]):
    with open(config["csv"]["filename"], 'w') as f:
        f.write('datetime,download,upload\n')

# Get the server used for testing
logger.debug('Getting server...')
try:
    sptest.get_best_server()
    speedtest_server = f'{sptest.results.server["sponsor"]} ({sptest.results.server["name"]})'
    logger.info(f'Using {speedtest_server}')
except:
    logger.error('Unable to get server information, check internet connection!')
    sys.exit()

# Get the download speed
logger.debug('Getting download speed...')
try:
    speedtest_dl = round(sptest.download() / 1000000, 4)
    logger.info(f'Download speed: {speedtest_dl}')
except:
    logger.error('Unable to get download speed. Check internet connection!')
    sys.exit()

# Get the upload speed
logger.debug('Getting upload speed...')
try:
    speedtest_up = round(sptest.upload() / 1000000, 4)
    logger.info(f'Upload speed: {speedtest_up}')
except:
    logger.error('Unable to get upload speed. Check internet connection!')
    sys.exit()

if config["storage"]["csv"] == 1:
    with open(config["csv"]["location"], 'a') as f:
        f.write(f'{str(datetimenow)},{speedtest_dl},{speedtest_up}\n')

if config["storage"]["database"] == 1:
    # Write the results to DB
    host = config["database"]["host"]
    user = config["database"]["user"]
    passwd = config["database"]["password"]
    db = config["database"]["database"]

    try:
        logger.info('Inserting results into the database...')
        logger.debug(f'Connecting to DB: host={host} user={user} passwd={passwd} db={db}')
        conn = mysql.connector.connect( host=host,
                                        user=user,
                                        passwd=passwd,
                                        db=db)
        logger.debug('Connection established.')
        cursor = conn.cursor()

        query1 = "INSERT INTO speedtest (TestDateTime, Download, Upload) "
        query2 = f"VALUES ('{str(datetimenow)}',{speedtest_dl},{speedtest_up});"
        query = query1 + query2
        logger.debug(f'Executing query: {query}')
        cursor.execute(query)

        logger.debug('Committing DB insert.')
        conn.commit()

        logger.debug(f'Closing connection to {host}.')
        conn.close()

        logger.info('Run finished.')
    except:
        logger.error('Unable to insert results into DB. Please run insert manually.')
        logger.error(query)

# This does nothing v2
