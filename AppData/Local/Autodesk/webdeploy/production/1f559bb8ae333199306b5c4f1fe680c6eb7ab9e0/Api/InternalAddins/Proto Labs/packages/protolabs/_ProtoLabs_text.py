#Author-Proto Labs, Inc.
#Description-Protolabs Text
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

from ._ProtoLabs_core import ConnectionStatus


class UserVisibleText:

    errorSupportStatement =     'For more information or assistance please contact Protolabs customer service.\r\n\r\nhttp://www.protolabs.com/contact'

    commandName =               'Get A Quote From Protolabs®'

    marketingText =             """<p>Get an interactive quote within hours from Protolabs. </p>"""
    nothingToEstimateText =     """<p><b>There is no body to quote in the active design. <br/><br/>Click cancel and select a design with the desired body/bodies. </b></p>"""
    singleBodyText =            """<p><b>Click continue to receive an interactive quote. </b></p>"""
    componentSelectionText =    """<p><b>Select components and click continue to receive an interactive quote. </b></p>"""
    legalText =                 """<p>To get an interactive quote, your CAD model will be transferred to Protolabs where it will be subject to Protolabs' <a href='http://www.protolabs.com/privacy-policy'>privacy policy</a> and <a href='http://www.protolabs.com/conditions-of-use'>terms of use</a>.  With your submission, you agree to this transfer of information.</p>"""

    # Any Autodesk formatting should be kept local to the code dealing with the actual progress dialog.
    mergeProgress =             'Preparing components for upload...'
    mergeFailure =              'The selected components were unable to be uploaded as designed. The bodies in each component must be able to be merged to form a single body. <br/><br/>Please modify the following components. <br/><br/>'

    # Any Autodesk formatting should be kept local to the code dealing with the actual progress dialog.
    uploadProgress =            'Uploading components...'

    ConnectionStatusResponseMessages = {
        ConnectionStatus.BAD_COUNTRY:       'Protolabs\' interactive quote requests in Fusion 360 are currently unavailable in your region. Please visit <a href="http://www.protolabs.com/?utm_campaign=us-sos&utm_medium=display&utm_source=autodesk&utm_content=partnership-f360-ipblock">protolabs.com</a> to request a quote.',
        ConnectionStatus.BAD_CONNECTION:    'An active Internet connection is required to request an interactive quote from Protolabs. Please verify your connection and try again.',
        ConnectionStatus.TIMEOUT:           'The Protolabs® add-in has failed to load. Please try again or contact Protolabs customer service at customerservice@protolabs.com.',
        ConnectionStatus.ERROR:             'The Protolabs® add-in has failed to load. Please contact Protolabs customer service at customerservice@protolabs.com.'
    }


