import speedtest
import logging

logger = logging.getLogger('speedtest')

def get_results():

    sptest = speedtest.Speedtest()

    # Get the best server
    logger.info('Getting best server...')
    sptest.get_best_server()
    logger.debug(f'Server found: {sptest.results.server["sponsor"]} ({sptest.results.server["name"]})')

    # Get download speed
    logger.info('Getting download speed.')
    try:
        download = sptest.download()
        logger.debug(f'Download speed acquired: {download}')
    except:
        logger.error('Unable to obtain download speed.')
        download = 0.0

    # Get upload speed
    logger.info('Getting upload speed.')
    try:
        upload = sptest.upload(pre_allocate=False)
        logger.debug(f'Upload speed acquired: {upload}')
    except:
        logger.error('Unable to obtain upload speed.')
        upload = 0.0

    return download, upload, f'{sptest.results.server["sponsor"]} ({sptest.results.server["name"]})'