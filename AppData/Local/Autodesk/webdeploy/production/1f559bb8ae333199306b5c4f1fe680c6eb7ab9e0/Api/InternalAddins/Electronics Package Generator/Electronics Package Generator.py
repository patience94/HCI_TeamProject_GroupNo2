#Author-Autodesk Inc.
#Description-Generate a 3D package with a 3D model and IPC compilant 2D footprint from parameters.

import adsk.core, adsk.fusion, traceback
import json
import time
import os
from .user_preference import _LCLZ, locale                   

app = adsk.core.Application.get()
ui  = app.userInterface

try:
    from .Packages import footprintHelper as FH
    from .Packages import model3DHelper as M3DH
except:
    ui.messageBox('Failed to load imports:\n{}'.format(traceback.format_exc()))

# global set of event handlers to keep them referenced for the duration of the command
handlers = {}

design = None

# global config to control drawing
enableFootprintGeneration = True
footprintName = None

# config
packageGeneratorPaletteWidth = 370
packageGeneratorPaletteHeight = 600
usePackageGeneratorPaletteNewBrowser = True
packageGeneratorPaletteIdPrefix = 'packageGeneratorPalette_' # DO NOT CHANGE the prefix - See FUS-58345
packageGeneratorButtonId = 'packageGeneratorButton_' + str(int(time.time()))
packageGeneratorButtonName = '3D Package Generator'
packageGeneratorButtonDescription = 'Generate a 3D package for PCB.\n'
packageGeneratorHTMLLocation = 'file:///' + os.path.dirname(__file__) + '/dist/fusion-package-generator/index_offline.html'
#packageGeneratorTargetToolbarPanel = 'SolidCreatePanel'
packageGeneratorTargetToolbarPanel = 'Package3DPanel'
packageGeneratorPalettesGroupName = 'packageGeneratorPalettesGroup'
packageGeneratorPackageInfoGroupName = 'packageGeneratorPackageInfoGroup'
packageGeneratorPackageTypeAttrName = 'PackageType'
packageGeneratorIsGeneratedAttrName = 'IsGenerated'
lastPackageGeneratorPaletteId = None
PackageGeneratorPaletteVisable = False

# component
model3DTargetComponent = None
model3DTargetComponentName = 'Model'

# config for saving
enableSavingPackage = False
timeoutForSaving3DModel = 120 # 2 mins

only3dModelGenerator = 0

def setDesignContext():
    global design
    design = adsk.fusion.Design.cast(app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    # set the proper target component
    global model3DTargetComponent 
    model3DTargetComponent = None
    for occur in design.rootComponent.occurrences:
        current_comp = occur.component
        if current_comp.name == model3DTargetComponentName:
            model3DTargetComponent = current_comp

def getNewComponent(name):
    occurrence = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occurrence.component.name = name
    return occurrence.component

# loop through list of occurances and deletes the occurances with name containing the target name
def removeComponentOccurancesByNameFromParent(name, parentComponent):
    removed = False

    for occurrence in parentComponent.occurrences:
        if occurrence.isValid and name in occurrence.name:
            occurrence.deleteMe()
            removed = True

    return removed

def removeUserParameters(design):
    paramCount = design.userParameters.count
    
    for i in range(paramCount - 1, -1, -1):
        uParam = design.userParameters.item(i)

        if uParam.isDeletable:
            uParam.deleteMe()

def setCamera():
    app.activeViewport.fit()

def getCurrentPalette():
    palettes = app.activeDocument.attributes.itemsByGroup(packageGeneratorPalettesGroupName)

    if palettes:
        return ui.palettes.itemById(palettes[0].value)

    return None

def generateFootprint(xmlData):
    global footprintName
    footprintName = FH.generate(design, design.rootComponent, xmlData)

def generate3DModel(modelInfo):
    try:
        global model3DTargetComponent
        
        # read package type
        packageTypeAttr = app.activeDocument.attributes.itemByName(packageGeneratorPackageInfoGroupName, packageGeneratorPackageTypeAttrName)
        
        # remove everything if the package type is not the same as type stored in the design
        if packageTypeAttr == None or modelInfo['type'] != packageTypeAttr.value:

            # delete all the previous features. 
            removeComponentOccurancesByNameFromParent(model3DTargetComponentName, design.rootComponent)
            
            # delete all the related user paramters.
            removeUserParameters(design)
            
            # delete the attribute if possibile
            if packageTypeAttr != None:
                packageTypeAttr.deleteMe()
            
            model3DTargetComponent = getNewComponent(model3DTargetComponentName)
        
        # get current palette reference
        currentPalette = getCurrentPalette()

        status = M3DH.generate(design, model3DTargetComponent, modelInfo)

        #add the document tag when the model generated successfully
        if status : 
            app.activeDocument.attributes.add(packageGeneratorPackageInfoGroupName, packageGeneratorPackageTypeAttrName, modelInfo['type'])

        if not status:
            ui.messageBox(modelInfo['type'].title() + _LCLZ("PackageNotSupported", " 3D package generator not supported yet."))
        elif enableSavingPackage:
            # send response to HTML for UI update (showing finish button)
            if currentPalette:
                data = {
                    "model3dGeneration": {
                        "success": status
                    }
                }
                currentPalette.sendInfoToHTML('send', json.dumps(data))
        elif currentPalette:
            if footprintName != None and only3dModelGenerator == 0:
                app.activeDocument.name = footprintName

        setCamera()

    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def handleAssetData(data):
    
    #terminate the active command if there is to create a clean env for package generator.
    app.userInterface.terminateActiveCommand()
    
    setDesignContext()

    if data['assetType'] == 'footprint' and enableFootprintGeneration and only3dModelGenerator == 0:
        generateFootprint(data['payload'])
    elif data['assetType'] == 'model':
        generate3DModel(data['payload'])

    app.activeViewport.refresh()

def getTargetDataFolderForSaving():
    data = app.data
    currentProject = data.activeProject
    return currentProject.rootFolder

# TODO: folder dialog, save progress dialog
def save3DModel(design, name):
    if not model3DTargetComponent.isValid:
        ui.messageBox(_LCLZ("ModelComponentNotFound", "Target 3D model component not found. Make sure it exists in the design."),
            _LCLZ("Upload", "Upload"),
            adsk.core.MessageBoxButtonTypes.OKButtonType,
            adsk.core.MessageBoxIconTypes.CriticalIconType
        )
        return

    # save locally
    exportMgr = design.exportManager
    scriptPath, scriptFilename = os.path.split(__file__)
    fileName = scriptPath + '/' + name + '.f3d'
    archOptions = exportMgr.createFusionArchiveExportOptions(fileName, model3DTargetComponent)
    stat = exportMgr.execute(archOptions)

    # upload to cloud
    dataFileFuture = getTargetDataFolderForSaving().uploadFile(fileName)

    # component can be directly uploaded to cloud but its not working (might be a bug in Fusion API)
    #dataFileFuture = model3DTargetComponent.saveCopyAs(name, getTargetDataFolderForSaving(), '', '')

    isUploaded = False
    startTime = time.time()

    while not isUploaded and dataFileFuture.isValid:
        adsk.doEvents()

        if time.time() - startTime > timeoutForSaving3DModel:
            ui.messageBox(_LCLZ("UploadOperationAborted", "Taking too long to upload generated 3D model to Fusion Project. Operation Aborted."),
                _LCLZ("Upload", "Upload"),
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.CriticalIconType
            )
            break

        if dataFileFuture.uploadState == adsk.core.UploadStates.UploadFailed:
            ui.messageBox(_LCLZ("FailedToUploadModel", "Failed to upload generated 3D model in Fusion Project."),
                _LCLZ("Upload", "Upload"),
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.CriticalIconType
            )
            break

        elif dataFileFuture.uploadState == adsk.core.UploadStates.UploadFinished:
            urn = dataFileFuture.dataFile.id
            ui.messageBox(_LCLZ("UploadedModel", "Uploaded 3D Model") + ' URN: ' + urn)
            isUploaded = True

    if isUploaded:
        if os.path.exists(fileName):
            os.remove(fileName)

# Currently saves only 3d model to the active project.
def savePackage(packageName):
    if design and design.isValid:
        save3DModel(design, packageName)
    else:
        ui.messageBox(_LCLZ("DesignNotFound", "Design is not found or valid."),
            _LCLZ("Save", "Save"),
            adsk.core.MessageBoxButtonTypes.OKButtonType,
            adsk.core.MessageBoxIconTypes.CriticalIconType
        )
 
def hideLastPaletteIfAny():
    if lastPackageGeneratorPaletteId:
        palette = ui.palettes.itemById(lastPackageGeneratorPaletteId)

        if palette:
            palette.isVisible = False

def deletePaletteFromDocumentIfAny(doc):
    palettesAttribute = doc.attributes.itemsByGroup(packageGeneratorPalettesGroupName)

    if palettesAttribute:
        # retrieve and delete the existing palette 
        palette = ui.palettes.itemById(palettesAttribute[0].value)

        if palette:
            palette.deleteMe()

        # remove attribute from document
        palettesAttribute[0].deleteMe()

def getDefaultUnitAsString():
    defaultDistanceDisplayUnits = design.fusionUnitsManager.distanceDisplayUnits

    if defaultDistanceDisplayUnits == adsk.fusion.DistanceUnits.CentimeterDistanceUnits:
        return 'cm'
    elif defaultDistanceDisplayUnits == adsk.fusion.DistanceUnits.FootDistanceUnits:
        return 'ft'
    elif defaultDistanceDisplayUnits == adsk.fusion.DistanceUnits.InchDistanceUnits:
        return 'in'
    elif defaultDistanceDisplayUnits == adsk.fusion.DistanceUnits.MeterDistanceUnits:
        return 'm'
    elif defaultDistanceDisplayUnits == adsk.fusion.DistanceUnits.MillimeterDistanceUnits:
        return 'mm'


class PackageGeneratorEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        try:
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)
            data = json.loads(htmlArgs.data)

            if htmlArgs.action == 'savePackage' and enableSavingPackage:
                savePackage(data['name'])
            elif htmlArgs.action == 'sendAssetData':
                handleAssetData(data)
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CreatePackageGeneratorCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            #terminate the active command if there is to create a clean env for package generator.
            app.userInterface.terminateActiveCommand() 

            # Load 3d package/model generator
            # if there is no footprint load package generator and add an temporary attribute to the document
            # the attribute helps to detect the mode when user switches tab (which deletes the palette in current document)
            # and comes back to the document to continue the generation
            # the attribute is removed before saving the document
            global only3dModelGenerator
            setDesignContext()

            if not FH.footprintExists(design):
                app.activeDocument.attributes.add(packageGeneratorPackageInfoGroupName, packageGeneratorIsGeneratedAttrName, 'true')
                only3dModelGenerator = 0
            else:
                isPackageGeneratedAttr = app.activeDocument.attributes.itemByName(packageGeneratorPackageInfoGroupName, packageGeneratorIsGeneratedAttrName)

                if isPackageGeneratedAttr == None:
                    only3dModelGenerator = 1
                else:
                    only3dModelGenerator = 0

            unitStr = getDefaultUnitAsString()
            loadGenerator(packageGeneratorHTMLLocation + '?only3dModelGenerator=' + str(only3dModelGenerator) + '&unit=' + unitStr + "&locale=" + locale)
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class DocumentCreatedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        hideLastPaletteIfAny()

class DocumentDeactivatingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)
        deletePaletteFromDocumentIfAny(eventArgs.document)

class DocumentClosingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)
        deletePaletteFromDocumentIfAny(eventArgs.document)

class DocumentSavingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)
        deletePaletteFromDocumentIfAny(eventArgs.document)

        # remove temporary attribute used for detecting generation mode
        isPackageGeneratedAttr = eventArgs.document.attributes.itemByName(packageGeneratorPackageInfoGroupName, packageGeneratorIsGeneratedAttrName)

        if isPackageGeneratedAttr:
            isPackageGeneratedAttr.deleteMe()

class WorkspacePreActivateHandler(adsk.core.WorkspaceEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.WorkspaceEventArgs.cast(args)

        # this prevents from deleting the palette when switching document since workspace event is fired during that time
        # delete palette if switching to workspace different than design
        if eventArgs.workspace.name.lower() != 'design':
            deletePaletteFromDocumentIfAny(app.activeDocument)

class CommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)

        if eventArgs.commandId == 'ResetToDefaultLayoutCommand':
            # Code to react to this Reset Event
            palette = ui.palettes.itemById(lastPackageGeneratorPaletteId)
            if palette != None:
                InitializePaletteLayout(palette)
                palette.isVisible = PackageGeneratorPaletteVisable

class CommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        eventArgs = adsk.core.ApplicationCommandEventArgs.cast(args)

        if eventArgs.commandId == 'ResetToDefaultLayoutCommand':
            # Code to react to this Reset Event
            global PackageGeneratorPaletteVisable
            palette = ui.palettes.itemById(lastPackageGeneratorPaletteId)
            if palette != None:
                PackageGeneratorPaletteVisable = palette.isVisible


def InitializePaletteLayout(palette):
    palette.width = packageGeneratorPaletteWidth
    palette.dockingOption = adsk.core.PaletteDockingOptions.PaletteDockOptionsNone
    palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateFloating
    
    position = app.activeViewport.viewToScreen(adsk.core.Point2D.create(0, 0))
    palette.setPosition(int(position.x + 2), int(position.y +2))
    palette.height = app.activeViewport.height - 32



def loadGenerator(htmlPath):
    # check for existing generator for current document
    palettesAttribute = app.activeDocument.attributes.itemsByGroup(packageGeneratorPalettesGroupName)
    paletteId = packageGeneratorPaletteIdPrefix + str(int(time.time()))

    # create new palette if package generator is opened for the first time for the current document
    if not palettesAttribute:
        paletteTitle = _LCLZ("PackageGenerator", "Package Generator")

        if only3dModelGenerator == 1:
            paletteTitle = _LCLZ("ModelGenerator", "Model Generator")

        palette = ui.palettes.add(paletteId, paletteTitle, htmlPath, False, True, True, packageGeneratorPaletteWidth, packageGeneratorPaletteHeight, usePackageGeneratorPaletteNewBrowser)
    
        # register handler
        onHTMLEvent = PackageGeneratorEventHandler()
        palette.incomingFromHTML.add(onHTMLEvent)
        handlers['paletteHtmlEventHandler_' + paletteId] = onHTMLEvent

        # initialize the palette layout
        InitializePaletteLayout(palette)
        # show palette
        palette.isVisible = True

        # store palette information in the document
        # helps to load existing palette with generator last state for the document
        app.activeDocument.attributes.add(packageGeneratorPalettesGroupName, paletteId, paletteId)
    else:
        # get palette reference
        paletteId = palettesAttribute[0].value
        palette = ui.palettes.itemById(paletteId)

        # show the existing palette
        if palette:
            palette.isVisible = True

    # store last palette id to be hidden on creating new document or switching to previous document
    global lastPackageGeneratorPaletteId
    lastPackageGeneratorPaletteId = paletteId

def run(context):
    try:
        resourceDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources')
        cmdDef = ui.commandDefinitions.addButtonDefinition(packageGeneratorButtonId, packageGeneratorButtonName, packageGeneratorButtonDescription, resourceDir)
        createPanel = ui.allToolbarPanels.itemById(packageGeneratorTargetToolbarPanel)
        
        if not createPanel:
            return

        cmdControl = createPanel.controls.addCommand(cmdDef)
        cmdControl.isPromoted = True
        cmdControl.isPromotedByDefault = True
        
        onCommandCreated = CreatePackageGeneratorCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers['CreateButtonEventHandler'] = onCommandCreated

        onCommandTerminated = CommandTerminatedHandler()
        ui.commandTerminated.add(onCommandTerminated)
        handlers['CommandTerminatedHandler'] = onCommandTerminated

        onCommandStarting = CommandStartingHandler()
        ui.commandStarting.add(onCommandStarting)
        handlers['CommandStartingHandler'] = onCommandStarting

        onDocumentCreated = DocumentCreatedHandler()
        app.documentCreated.add(onDocumentCreated)
        handlers['documentCreatedHandler'] = onDocumentCreated

        onDocumentClosing = DocumentClosingHandler()
        app.documentClosing.add(onDocumentClosing)
        handlers['documentClosingHandler'] = onDocumentClosing

        onDocumentDeactivating = DocumentDeactivatingHandler()
        app.documentDeactivating.add(onDocumentDeactivating)
        handlers['documentDeactivatingHandler'] = onDocumentDeactivating

        onDocumentSaving = DocumentSavingHandler()
        app.documentSaving.add(onDocumentSaving)
        handlers['documentSavingHandler'] = onDocumentSaving

        onWorkspacePreActivate = WorkspacePreActivateHandler()
        ui.workspacePreActivate.add(onWorkspacePreActivate)
        handlers['workspacePreActivateHandler'] = onWorkspacePreActivate
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        createPanel = ui.allToolbarPanels.itemById(packageGeneratorTargetToolbarPanel)

        if not createPanel:
            return

        packageGeneratorButton = createPanel.controls.itemById(packageGeneratorButtonId)
        
        if packageGeneratorButton:
            packageGeneratorButton.deleteMe()
        
        cmdDef = ui.commandDefinitions.itemById(packageGeneratorButtonId)

        if cmdDef:
            cmdDef.deleteMe()

        # delete all existing palettes and removed related attribute from document
        for doc in app.documents:
            deletePaletteFromDocumentIfAny(doc)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
