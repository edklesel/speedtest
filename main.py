from Speedtest import splogging
logger = splogging.getlogger()
from Speedtest import database, speedtest
from time import sleep

def main():
    # Get the speeds from the API
    download, upload = speedtest.get_results()
    
    # Record the speeds in the DB
    database.record_speed(
        download=download,
        upload=upload
    )
            
if __name__ == '__main__':

    # Configure the DB ready for inserting into
    database.initialise_db()

    # Main routine
    while True:

        try:
            main()

        except KeyboardInterrupt:
            print('Stopping')
            exit(1)

        except:
            logger.exception('Error collecting data.')
            
        finally:

            try:
                sleep(10)
            except KeyboardInterrupt:
                print('Stopping')
                exit(1)

