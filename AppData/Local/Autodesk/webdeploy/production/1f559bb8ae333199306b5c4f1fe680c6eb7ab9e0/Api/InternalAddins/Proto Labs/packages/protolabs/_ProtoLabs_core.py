# encoding: utf-8
#Author-Proto Labs, Inc.
#Description-Protolabs Core
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

from ._ProtoLabs_logging import getRootLogger
logger = getRootLogger().getChild('_ProtoLabs_core')

# Python 3.3 doesn't have builtin enum support
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ConnectionStatus = enum("SUCCESS", "BAD_COUNTRY", "BAD_CONNECTION", "TIMEOUT", "ERROR")

def TestMethod(arg):
    return arg

def removeDisallowedFilenameChars(filename):
    import re

    badchars = re.compile(r'[^A-Za-z0-9_. ]+|^\.|\.$|^ | $|^$')
    badnames = re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')

    cleanedFilename = badchars.sub('_', filename)
    if badnames.match(cleanedFilename):
        cleanedFilename = '_' + cleanedFilename

    logger.debug('removeDisallowedFilenameChars: Cleaned Filename = {0}'.format(cleanedFilename))
    return cleanedFilename

def getBaseUrl():
    return getCustomSetting("baseUrl")

def buildURL(tail):
    url = getBaseUrl()
    if not tail is None and len(tail) > 0:
        if not tail[0] == '/':
            url += '/'
        url += tail
    return url

def getCertAuthorityStore():
    import os

    certPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cert', 'cert.pem')
    if os.path.exists(certPath):
        return certPath

    return None

def getCustomSetting(setting):
    import json
    import os

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')) as json_data:
        value = None
        data = json.load(json_data)

        value = data[setting]

        json_data.close()

        logger.debug('getCustomSetting: setting-{0}, data-{1}, value-{2}.'.format(setting, str(data), str(value)))

        if value is not None:
            return value
        else:
            raise KeyError('Configuration Error:  {0} missing from configuration file.'.format(setting))

isValidCountry = None

def isValidCountryUsage():
    import json
    from .packages import requests

    global isValidCountry
    if isValidCountry is not None:
        return isValidCountry

    try:
        url = buildURL('PluginSettings')
        certAuthorityStore = getCertAuthorityStore()

        logger.debug('isValidCountryUsage: {0}'.format({'url':url, 'certAuthorityStore':certAuthorityStore}))
        response = requests.get(url, verify = certAuthorityStore)
        logger.debug('isValidCountryUsage: {0}'.format({'response.statusCode':response.status_code}))

        response.raise_for_status()

        data = response.json()
        logger.debug('isValidCountryUsage: {0}'.format({'data':data}))

        enable = data['Enable']

        if not enable:
            logger.info('Invalid country detected.')

        isValidCountry = ConnectionStatus.SUCCESS if enable else ConnectionStatus.BAD_COUNTRY
        return isValidCountry
    # If we got a request related error then reset - it could be a connectivity issue
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        logger.debug('isValidCountryUsage had a connectivity error while trying to determine the value for a valid country.')
        logger.exception('Failure determining country.')
        isValidCountry = None
        return ConnectionStatus.BAD_CONNECTION
    except requests.exceptions.Timeout:
        logger.debug('isValidCountryUsage timed out while trying to determine the value for a valid country.')
        logger.exception('Failure determining country.')
        isValidCountry = None
        return ConnectionStatus.TIMEOUT
    # There was a problem with the request - it was missing 'Enable' in the response
    except KeyError:
        logger.debug("'Enable' not found in server response")
        logger.exception('Failure determining country.')
        isValidCountry = None
        return ConnectionStatus.BAD_CONNECTION
    # If anything else goes wrong
    except:
        logger.debug('isValidCountryUsage encountered an error')
        logger.exception('Failure determining country.')
        isValidCountry = None
        return ConnectionStatus.ERROR

def testInternetConnection(address = None, timeout = 10):
    from .packages import requests

    if address is None:
        address = getBaseUrl()

    try:
        response = requests.head(address, timeout=timeout, verify=getCertAuthorityStore())
        response.raise_for_status()
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        logger.exception('No internet connection.')
        return ConnectionStatus.BAD_CONNECTION
    else:
        # If we get any sort of response then we have some sort of internet connection
        logger.debug("Successfully connected to {} in less than {}s".format(address, timeout))
        return ConnectionStatus.SUCCESS
