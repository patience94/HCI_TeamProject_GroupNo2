#Author-Proto Labs, Inc.
#Description-Protolabs upload helpers
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

import adsk.core
import adsk.fusion

from . import _ProtoLabs_core as plCore
from ._ProtoLabs_text import UserVisibleText as plText
from . import _ProtoLabs_ADFusion as plADFusion
from ._ProtoLabs_logging import getRootLogger

logger = getRootLogger().getChild('_ProtoLabs_upload')

def requestEstimate(design, components, ui):

    import webbrowser
    import urllib.parse

    progress = ui.createProgressDialog()
    progress.isCancelButtonShown = False
    progress.isBackgroundTranslucent = False
    baseMessage = plText.uploadProgress + ' %p%'

    # The progress dialog will display if things are 0% complete.
    # However, it will not display if the current value is 0.
    # As a workaround, make the minimum value 1 so 0% will be shown.
    progress.show('Protolabs', baseMessage, 1, 1 + len(components), 0)

    sagaGUID = submitEstimateRequest(design, components)
    webbrowser.open_new(plCore.buildURL(sagaGUID))

    uploadModels(design, components, sagaGUID, progress)

def submitEstimateRequest(design, components):

    from .packages import requests
    import json

    url = plCore.buildURL('/EstimateRequest')
    certAuthorityStore = plCore.getCertAuthorityStore()
    jsonData = buildEstimateRequestJSON(components)

    logger.debug('submitEstimateRequest: {0}'.format({'url':url, 'certAuthorityStore':certAuthorityStore, 'data':json.dumps(jsonData)}))

    response = requests.post(url, json=jsonData, verify = certAuthorityStore)

    logger.debug('submitEstimateRequest: {0}'.format({'response.statusCode':response.status_code}))

    if not response.status_code == requests.codes.ok:
        response.raise_for_status()

    responseJSON = response.json()
    sagaGUID = responseJSON['SagaGuid']

    logger.info('Submitted estimate request. {0}'.format({'SagaGUID': sagaGUID, 'Count':len(components)}))

    return sagaGUID

def buildEstimateRequestJSON(components):

    models = []

    for number, component in enumerate(components, start = 0):
        name = component.originalName
        models.append({'SourceModelID': number,
                       'Name': name})

    data = {'Models': models}

    return data

def uploadModels(design, components, sagaGUID, progress):

    import tempfile
    tempFolder = tempfile.gettempdir()

    baseMessage = progress.message + '<br/><br/>'

    for number, component in enumerate(components, start = 0):
        progress.message = baseMessage + component.originalName
        progress.progressValue = progress.minimumValue + number

        uploadModel(design, component, number, tempFolder, sagaGUID)

        progress.progressValue = progress.minimumValue + number + 1

    progress.hide()

    logger.info('Posted all files. {0}'.format({'SagaGUID': sagaGUID, 'Count': len(components)}))

def uploadModel(design, component, number, tempFolder, sagaGUID):

    name = component.originalName
    fileName = plCore.removeDisallowedFilenameChars(name)

    outputFileName = saveTempFile(design.exportManager, tempFolder, fileName, component)



    import ntpath
    from .packages import requests

    url = plCore.buildURL('/Model')
    certAuthorityStore = plCore.getCertAuthorityStore()

    fileNameOnly = ntpath.basename(outputFileName)

    logger.debug('uploadModel: {0}'.format({'url':url, 'SagaGUID': sagaGUID, 'SourceModelID': number, 'Name': name, 'certAuthorityStore':certAuthorityStore}))

    with open(outputFileName, 'rb') as f:
        response = requests.post(url,
                                 files={'SagaGuid': (None, sagaGUID),
                                        'SourceModelID': (None, str(number)),
                                        'Name': (None, name),
                                        'File': (fileNameOnly, f, 'application/step')},
                                 verify = certAuthorityStore)

    logger.debug('uploadModel: {0}'.format({'response.statusCode':response.status_code}))

    if not response.status_code == requests.codes.ok:
        response.raise_for_status()



    deleteTempFile(outputFileName)

    logger.info('Posted file. {0}'.format({'SagaGUID': sagaGUID, 'SourceModelID': number, 'Name': name}))

def saveTempFile(exportMgr, tempFolder, fileName, component):
    import os

    outputFileName = os.path.join(tempFolder, (fileName + '.step'))

    stepOptions = None
    if component:
        stepOptions = exportMgr.createSTEPExportOptions(outputFileName, component)
    else:
        stepOptions = exportMgr.createSTEPExportOptions(outputFileName)

    exportSuccessful = exportMgr.execute(stepOptions)

    logger.debug('saveTempFile: tempFolder: {0}, fileName: {1}, component: {2}, outputFileName: {3}, exportSuccessful: {4}.'.format(tempFolder, fileName, component.name, outputFileName, str(exportSuccessful)))

    if exportSuccessful:
        return outputFileName
    else:
        raise OSError('Unable to export the project.')

def deleteTempFile(outputFileName):
    import os

    try:
        os.remove(outputFileName)
        logger.debug('deleteTempFile: outputFileName-{0}.'.format(outputFileName))
    except:
        logger.debug('deleteTempFile Exception thrown: outputFileName: {0}; Exception: {1}.'.format(outputFileName, traceback.format_exc()))
