from Speedtest import splogging
logger = splogging.getlogger()
from datetime import datetime as dt
from Speedtest import database, speedtest, influx
from time import sleep
from yaml import load, Loader

def main():

    # Get the speeds from the API
    download, upload, server = speedtest.get_results()
    
    # Record the speeds in the SQLite DB
    if 'sqlite' in config.keys():
        database.record_speed(
            download=download,
            upload=upload
        )

    # Record the speeds in the InfluxDB
    if 'influxdb' in config.keys():
        influx.record_speed(
            download=download,
            upload=upload,
            server=server,
            datetime=dt.utcnow()
        )
            
if __name__ == '__main__':

    with open('config.yml', 'r') as f:
        config = load(f.read(), Loader=Loader)

    # Configure the DB ready for inserting into
    if 'sqlite' in config.keys():
        database.initialise_db()

    main()
