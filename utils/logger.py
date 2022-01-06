import logging, time, os
from globaldata.data import G


# we can use log_cli in pytest.ini instead of this class
# discard, and implement in pytest.ini
class Logger():

    def __init__(self):
        self.logname = os.path.join(G.LOG_PATH, "{}.log".format(time.strftime("%Y%m%d_%H%M%S")))
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s %(funcName)s][%(levelname)s]: %(message)s')

        self.filelogger = logging.FileHandler(self.logname, mode='a', encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.filelogger.setLevel(logging.DEBUG)
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)


logger = Logger().logger

if __name__ == '__main__':
    logger.info('test starting')
    logger.debug('test finished')
