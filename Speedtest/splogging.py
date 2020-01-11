import logging as pylogging
from yaml import load, Loader
from datetime import datetime
import os

class MyFormatter(pylogging.Formatter):

    converter = datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
        return t

def getlogger():

    logger = pylogging.getLogger('speedtest')
    
    with open('config.yml') as f:
        config = load(f.read(), Loader=Loader)
    
    logger.setLevel(pylogging.DEBUG)

    if (not os.path.exists('logs')) and (not os.path.isdir('logs')):
        os.mkdir('logs')

    filename = f"speedtest_{datetime.now().strftime('%Y%m%d')}.log"
    logformat = MyFormatter("%(asctime)s - %(levelname)-7s - %(message)s")
    fh = pylogging.FileHandler(os.path.join('logs', filename))
    if config['DEBUG']:
        fh.setLevel(pylogging.DEBUG)
    else:
        fh.setLevel(pylogging.INFO)
    fh.setFormatter(logformat)
    logger.addHandler(fh)

    sh = pylogging.StreamHandler()
    sh.setLevel(pylogging.ERROR)
    sh.setFormatter(logformat)
    logger.addHandler(sh)

    return logger
