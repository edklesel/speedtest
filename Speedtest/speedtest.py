import speedtest
import logging

logger = logging.getLogger('speedtest')

def get_results():

    sptest = speedtest.Speedtest()

    # Get the best server
    logger.info('Getting best server...')
    sptest.get_best_server()
    logger.debug(f'Server found: f{sptest.results.server["sponsor"]} ({sptest.results.server["name"]})')

    # Get download speed
    logger.info('Getting download speed.')
    download = sptest.download()
    logger.debug(f'Download speed acquired: {download}')

    # Get upload speed
    logger.info('Getting upload speed.')
    upload = sptest.upload()
    logger.debug(f'Upload speed acquired: {upload}')

    return download, upload