from influxdb import InfluxDBClient
import logging
from datetime import datetime as dt
from yaml import load, Loader

logger = logging.getLogger('speedtest')

class Error(Exception):
    pass


# Custom call used to raise exception when bad config is detected
class ConfigError(Error):

    def __init__(self,message):
        logger.exception(message)


# Connection context manager
class Connection():

    # Load config from config.yml
    def __init__(self, database=None):

        with open('config.yml') as f:
            config = load(f.read(), Loader=Loader)

        if 'influxdb' not in config.keys():
            raise ConfigError(logger.error('InfluxDB config not found in config.yml, please make sure all required InfluxDB config is included.'))
        
        # Set default values if they are not present in the config
        self.host = 'localhost' if 'host' not in config['influxdb'].keys() else config['influxdb']['host']
        self.port = 8086 if 'port' not in config['influxdb'].keys() else config['influxdb']['port']
        self.username = None if 'username' not in config['influxdb'].keys() else config['influxdb']['username']
        self.password = None if 'password' not in config['influxdb'].keys() else config['influxdb']['password']
        self.database = database


    # Context manager for opening the connection
    def __enter__(self):
        if self.username:
            logger.debug(f'Opening database connection to InfluxDB host {self.username}@{self.host}:{self.port}.')
        else:
            logger.debug(f'Opening database connection to InfluxDB host {self.host}:{self.port}.')
        
        try:
            if self.username is None and self.password is None:
                self.client = InfluxDBClient(
                    host=self.host,
                    port=self.port,
                    database=self.database
                )
            else:
                self.client = InfluxDBClient(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    database=self.database
                )
        except:
            logger.error(f'Unable to open connection to {self.host}:{self.port}')
            raise

        if self.database:
            self.client.create_database(self.database)
        return self.client


    # Close the connection
    def __exit__(self, exception_type, exception_value, traceback):
        logger.debug(f'Closing connection to {self.host}:{self.port}')
        self.client.close()


# Record a speed to the InfluxDB instance
def record_speed(download, upload, server, datetime=dt.utcnow()):
    
    logger.debug('Writing data to InfluxDB.')
    json_body = [
        {
            "measurement": "speed",
            "tags": {
                "server": server
            },
            "time": datetime,
            "fields": {
                "download_speed": download,
                "upload_speed": upload
            }
        }
    ]

    with Connection(database='speedtest') as client:
        client.write_points(json_body)
        client.close()
