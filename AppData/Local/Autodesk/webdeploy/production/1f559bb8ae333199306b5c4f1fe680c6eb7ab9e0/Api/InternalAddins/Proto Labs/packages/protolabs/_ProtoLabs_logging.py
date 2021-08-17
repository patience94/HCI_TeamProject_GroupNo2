# encoding: utf-8
#Author-Proto Labs, Inc.
#Description-Protolabs logging
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

def getRootLogger():
    import logging
    import logging.config

    return logging.getLogger('protolabs')

def clearExistingLogHandlers():
    logger = getRootLogger()
    logger.handlers = []

logger = getRootLogger()

def setupLogging():
    import os
    import logging
    import logging.config
    from logging.handlers import TimedRotatingFileHandler

    try:
        global logger

        clearExistingLogHandlers()

        if not getIsCustomLogging():
            rootLogger = getRootLogger()
            level = getLoggingLevel()
            rootLogger.setLevel(level)

            logsPath = getDefaultLoggingLocation()

            if not os.path.exists(logsPath):
                os.makedirs(logsPath)

            logFile = os.path.join(logsPath, 'currentlog.txt')

            handler = TimedRotatingFileHandler(logFile,
                                               when='midnight',
                                               interval=1,
                                               backupCount=5)

            formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)s %(message)s')
            handler.setFormatter(formatter)

            rootLogger.addHandler(handler)

            logger = rootLogger.getChild('_ProtoLabs_logging')

            logger.info('Default Logging Enabled (Level {0}).'.format(level))
        else:
            logConfigFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logging.config')

            logging.config.fileConfig(logConfigFile)

            logger = getRootLogger().getChild('_ProtoLabs_logging')

            logger.info('Custom Logging Enabled.')

    except:
        raise Exception('Logging Setup Failed\n{0}.'.format(traceback.format_exc()))

def shutdownLogging():
    import logging
    import logging.config

    global logger

    logger.debug('Shutting logging down.')

    clearExistingLogHandlers()
    logger = getRootLogger()
    logging.shutdown()

def getDefaultLoggingLocation():
    import os
    import tempfile

    protoLabsTempDir = os.path.join(tempfile.gettempdir(), 'ProtoLabs')
    return os.path.join(protoLabsTempDir, 'Fusion360AddInLogs')

def getIsCustomLogging():
    from ._ProtoLabs_core import getCustomSetting
    return getCustomSetting("customLogging")

def getLoggingLevel():
    from ._ProtoLabs_core import getCustomSetting
    return getCustomSetting("loggingLevel")
