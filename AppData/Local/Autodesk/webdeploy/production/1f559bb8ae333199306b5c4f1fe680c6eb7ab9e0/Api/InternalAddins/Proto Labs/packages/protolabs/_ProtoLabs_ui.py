#Author-Proto Labs, Inc.
#Description-Protolabs UI
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

try:
    import adsk.core

    from ._ProtoLabs_text import UserVisibleText as plText
    from . import _ProtoLabs_core as plCore
    from . import _ProtoLabs_ADCore as plADCore
    from . import _ProtoLabs_ADFusion as plADFusion
    from ._ProtoLabs_logging import getRootLogger
except:
    import traceback

    app = adsk.core.Application.get()
    ui = app.userInterface
    ui.messageBox('Failed to load imports for Protolabs Add-In: {0}\r\n\r\n{1}'.format(traceback.format_exc(), plText.errorSupportStatement))

logger = getRootLogger().getChild('_ProtoLabs_ui')

handlers = []
forcedShutdown = None

PL_COMMAND_ID = 'ProtoLabsGetAnEstimate'
SOLID_WORKSPACE_ID = 'FusionSolidEnvironment'
SOLID_PANEL_ID = 'SolidMakePanel'
SOLID_PANEL_ID_FALLBACK = 'SolidScriptsAddinsPanel'
SURFACE_WORKSPACE_ID = 'FusionSurfaceEnvironment'
SURFACE_PANEL_ID = 'SurfaceMakePanel'
SURFACE_PANEL_ID_FALLBACK = 'SurfaceScriptsAddinsPanel'

def handleError(message):
    _handleError(message, False)

def handleException(message):
    _handleError(message, True)

def _handleError(message, exception):

    if exception:
        logger.exception(message)
    else:
        logger.error(message)

    ui = plADCore.getUI()
    if ui:
        ui.messageBox('{0}\r\n\r\n{1}'.format(message, plText.errorSupportStatement))


class ProtoLabsMainCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):

    def __init__(self):
        super().__init__()

        try:
            import adsk.fusion
        except:
            handleException('Failed to load imports for Protolabs Add-In.')

        self.design = None

        logger.debug('Initialized ProtoLabsMainCommandCreatedEventHandler')

    def notify(self, args):

        try:
            logger.debug('ProtoLabsMainCommandCreatedEventHandler Started.')

            if not testAvailableCountry():
                logger.info('Disabling Protolabs Add-In.')
                return

            app = adsk.core.Application.get()
            self.design = app.activeProduct
            if not isinstance(self.design, adsk.fusion.Design):
                handleError('Active document is not a design.')
                return

            cmd = args.command

            # Prevent files from being uploaded when the dialog is automatically destroyed.
            cmd.isExecutedWhenPreEmpted = False

            cmd.setDialogInitialSize(520, 370)
            cmd.setDialogMinimumSize(520, 370)

            cmd.okButtonText = 'Continue'
            cmd.cancelButtonText = 'Cancel'


            # Add the Protolabs logo to the dialog.
            # Apparently a non-empty name paired with full-width results in a left-justified image.
            logo = cmd.commandInputs.addImageCommandInput('ProtoLabsLogo', ' ', "./Resources/Logo.png")
            logo.isFullWidth = True


            self.addDesignContent(cmd)

            logger.debug('ProtoLabsMainCommandCreatedEventHandler Completed.')
        except:
            handleException('Failed to load Protolabs dialog.')

    def addDesignContent(self, cmd):

        # Validate design requirements
        designValidator = ValidateDesignHandler(self.design)
        cmd.validateInputs.add(designValidator)
        handlers.append(designValidator)

        if not designValidator.isDesignValid():
            self.addNothingToEstimateMessage(cmd)
        else:
            inputs = cmd.commandInputs

            # marketing and legal message only added if there is something to estimate.
            inputs.addTextBoxCommandInput('marketingMessage', '', plText.marketingText, 1, True)

            # Create the execution handler.
            executeHandler = SubmitEstimateRequestCommandEventHandler(self.design)
            handlers.append(executeHandler)

            if not self.requiresComponentSelection():
                self.addSingleBodyMessage(cmd)
            else:
                self.addComponentSelectionInputs(cmd, executeHandler)

            inputs.addTextBoxCommandInput('legalMessage', '', plText.legalText, 4, True)

            # Set the execution handler. Do this last. Otherwise it will still execute if an exception
            # is thrown and the validators (if any) pass.
            cmd.execute.add(executeHandler)


    def addNothingToEstimateMessage(self, cmd):

        cmd.commandInputs.addTextBoxCommandInput('nothingToEstimateMessage', '', plText.nothingToEstimateText, 4, True)

    def addSingleBodyMessage(self, cmd):

        cmd.commandInputs.addTextBoxCommandInput('singleBodyMessage', '', plText.singleBodyText, 1, True)
        cmd.commandInputs.addTextBoxCommandInput('documentNameMessage', '', 'Design: {0}'.format(self.design.parentDocument.name), 1, True)

    def addComponentSelectionInputs(self, cmd, executeHandler):

        try:
            cmdInputs = cmd.commandInputs

            if self.requiresComponentSelection():

                cmdInputs.addTextBoxCommandInput("SelectionInstructionsID", "", plText.componentSelectionText, 1, True)

                componentSelector = cmdInputs.addSelectionInput('ComponentSelectorID', 'Select components', 'Select components')
                componentSelector.setSelectionLimits(1, 0)
                componentSelector.addSelectionFilter('Occurrences')
                executeHandler.componentSelector = componentSelector

                componentList = cmdInputs.addTextBoxCommandInput('SelectedComponentList', '', '', 5, True)
                componentList.isFullWidth = False

                selectionInputValidator = ValidateComponentSelectionInputsHandler(self.design, componentSelector)
                cmd.validateInputs.add(selectionInputValidator)
                handlers.append(selectionInputValidator)

                onFilterSelection = FilterSelectionEventHandler(componentSelector)
                cmd.selectionEvent.add(onFilterSelection)
                handlers.append(onFilterSelection)

                onSelectionChanged = SelectionInputChangedHandler(self.design, componentSelector, componentList)
                cmd.inputChanged.add(onSelectionChanged)
                handlers.append(onSelectionChanged)

        except:
            handleException('Failed to generate component selection inputs.')
            raise # propagate failure

    def requiresComponentSelection(self):
        allBodiesCount = plADFusion.getAllBodiesCount(self.design.rootComponent)
        if plADFusion.generatorWorkaround:
            return any([(component.bRepBodies.count > 0 and component.bRepBodies.count != allBodiesCount) for component in self.design.allComponents])
        else:
            return any((component.bRepBodies.count > 0 and component.bRepBodies.count != allBodiesCount) for component in self.design.allComponents)



class FilterSelectionEventHandler(adsk.core.SelectionEventHandler):
    def __init__(self, componentSelector):
        super().__init__()
        self.componentSelector = componentSelector

    def notify(self, args):

        try:
            selectionEvent = args.firingEvent
            selectionInput = selectionEvent.activeInput

            if selectionInput == self.componentSelector:

                # Prevent selection of empty components.
                component = plADFusion.getComponent(args.selection.entity)
                if plADFusion.getAllBodiesCount(component) < 1:
                    args.isSelectable = False

                # This has no effect because args.additionalEntities has apparently not been implemented.
                # Once implemented, SelectionInputChangedHandler.syncOccurrences can be removed and
                # replaced by this functionality. This will also give us highlights for the related occurrences
                # when mousing over any occurrence.
                #if args.isSelectable:
                #   matchingOccurrences = plADFusion.getOccurrences(component)
                #   matchingOccurrences.remove(args.selection.entity)
                #   if len(matchingOccurrences) > 0:
                #       for other in matchingOccurrences:
                #           args.additionalEntities.add(other)

        except:
            args.isSelectable = False
            handleException('Failure filtering selection.')

class SelectionInputChangedHandler(adsk.core.InputChangedEventHandler):

    syncOccurrences = True

    def __init__(self, design, componentSelector, componentList):
        super().__init__()
        self.design = design
        self.componentSelector = componentSelector
        self.componentList = componentList
        self.currentSelections = []

    def notify(self, args):

        try:
            changedInput = args.input

            logger.debug('SelectionInputChangedHandler: {0}'.format(changedInput.id))

            if changedInput == self.componentSelector:

                previousSelections = self.currentSelections

                self.currentSelections = [self.componentSelector.selection(index).entity for index in range(self.componentSelector.selectionCount)]
                addingSelection = len(self.currentSelections) > len(previousSelections)

                # Find the toggled entity (it could be an occurrence or the root component).
                toggledSelection = None
                if addingSelection:
                    toggledSelection = next(selection for selection in self.currentSelections if not selection in previousSelections)
                else:
                    toggledSelection = next(selection for selection in previousSelections if not selection in self.currentSelections)

                logger.debug('toggled selection of: {0}'.format(toggledSelection.name))

                if addingSelection:
                    logger.debug('added selection: {0}'.format(toggledSelection.name))

                    if self.syncOccurrences:
                        for occurrence in plADFusion.getOccurrences(plADFusion.getComponent(toggledSelection)):
                            if not occurrence in self.currentSelections:
                                self.componentSelector.addSelection(occurrence)
                                self.currentSelections.append(occurrence)

                else:
                    logger.debug('removed selection: {0}'.format(toggledSelection.name))

                    if self.syncOccurrences:
                        matchingOccurrences = plADFusion.getOccurrences(plADFusion.getComponent(toggledSelection))

                        desiredSelections = [selection for selection in self.currentSelections if selection not in matchingOccurrences]
                        if self.currentSelections != desiredSelections:
                            self.componentSelector.clearSelection()
                            for selection in desiredSelections:
                                self.componentSelector.addSelection(selection)
                            self.currentSelections = desiredSelections


                self.updateComponentText()
        except:
            handleException('Failure processing selection.')

    def updateComponentText(self):

        allComponents = [plADFusion.getComponent(selection) for selection in self.currentSelections]
        uniqueComponents = plADFusion.getUniqueEntities(allComponents)
        newSelectionText = '<br/>'.join(self.getComponentText(component, allComponents) for component in reversed(uniqueComponents))
        self.componentList.formattedText = newSelectionText

        logger.debug('Selection count: {0}'.format(len(self.currentSelections)))
        logger.debug('Selected components: [{0}]{{{1}}}'.format(len(uniqueComponents), newSelectionText))

    def getComponentText(self, component, allComponents):
        if allComponents.count(component) > 1:
            return component.name + ' ({0} occurrences)'.format(allComponents.count(component))
        else:
            return component.name


class ValidateDesignHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self, design):
        super().__init__()
        self.design = design

    def isDesignValid(self):

        isValid = False

        try:
            if plADFusion.containsAnyBodies(self.design):
                isValid = True

        except:
            handleException('Design validation failed.')

        return isValid

    def notify(self, args):

        try:
            if not self.isDesignValid():
                args.areInputsValid = False

        except:
            args.areInputsValid = False
            handleException('Design validation failed.')


class ValidateComponentSelectionInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self, design, componentSelector):
        super().__init__()
        self.design = design
        self.componentSelector = componentSelector

    def notify(self, args):

        try:
            cmd = args.firingEvent.sender

            if self.componentSelector.selectionCount < 1:
                args.areInputsValid = False

        except:
            args.areInputsValid = False
            handleException('Selection validation failure.')


class SubmitEstimateRequestCommandEventHandler(adsk.core.CommandEventHandler):
    def __init__(self, design):
        super().__init__()
        self.design = design
        self.componentSelector = None

    def notify(self, args):

        originalComponentCount = self.design.allComponents.count
        try:
            logger.debug('SubmitEstimateRequestCommandEventHandler Started.')

            if not testInternetConnection():
                return

            selectedComponents = self.getSelectedComponents()
            mergedComponents = self.mergeComponents(selectedComponents)
            problemComponents = self.getProblemComponents(mergedComponents)

            if len(problemComponents) > 0:
                self.showMergeFailure(problemComponents)
            else:
                self.uploadComponents(mergedComponents)

            logger.debug('SubmitEstimateRequestCommandEventHandler Completed.')

        except:
            handleException('Failed to upload files.')

        finally:
            if self.design.allComponents.count != originalComponentCount:
                # Revert any modifications that were made to the design.
                # This will leave the design unchanged, but will (unfortunately)
                # still leave the design in a modified state.

                logger.info('Reverting design modifications.')

                undoCmd = plADCore.getUI().commandDefinitions.itemById('UndoCommand')
                undoCmd.execute()

    def getSelectedComponents(self):
        selectedComponents = []

        if self.componentSelector is not None:
            selectedComponents = [plADFusion.getComponent(self.componentSelector.selection(index).entity) for index in range(self.componentSelector.selectionCount)]
            selectedComponents = plADFusion.getUniqueEntities(selectedComponents)

        else:
            # No user selection required. Will use the entire design.
            selectedComponents.append(self.design.rootComponent)

        return selectedComponents


    def mergeComponents(self, selectedComponents):

        # Any component with multiple bodies must first have the bodies merged.
        progress = plADCore.getUI().createProgressDialog()
        progress.isCancelButtonShown = False
        progress.isBackgroundTranslucent = False
        baseMessage = plText.mergeProgress + ' %p%'

        # The progress dialog will display if things are 0% complete.
        # However, it will not display if the current value is 0.
        # As a workaround, make the minimum value 1 so 0% will be shown.
        progress.show('Protolabs', baseMessage, 1, 1 + len(selectedComponents), 0)

        baseMessage += '<br/><br/>'

        mergedComponents = []
        for number, component in enumerate(selectedComponents, start = 0):
            progress.message = baseMessage + component.name
            progress.progressValue = progress.minimumValue + number

            mergedComponent = None
            try:
                mergedComponent = plADFusion.createComponentWithMergedBodies(component)
            except:
                logger.exception('Failure merging component bodies.')

            if mergedComponent is None:
                mergedComponent = component

            mergedComponent.originalName = component.name # store the original name for uploading
            mergedComponents.append(mergedComponent)

            progress.progressValue = progress.minimumValue + number + 1

        progress.hide()

        return mergedComponents


    def getProblemComponents(self, components):
        return [component for component in components if plADFusion.getAllBodiesCount(component) != 1]


    def uploadComponents(self, components):
        from ._ProtoLabs_upload import requestEstimate
        requestEstimate(self.design, components, plADCore.getUI())


    def showMergeFailure(self, problemComponents):
        logger.error('Unable to merge components: ' + ','.join(component.originalName for component in problemComponents))

        message =  plText.mergeFailure
        message += '<br/>'.join('&nbsp;&nbsp;&nbsp;&nbsp;' + component.originalName for component in problemComponents)
        plADCore.getUI().messageBox(message)





def createCommand(ui, commandID):

    # First, clean up any previous commands or UI elements.
    # This could happen if the add-in crashed and didn't properly unload.
    cleanUpCommand(ui, PL_COMMAND_ID)

    # Create command.
    plCommandDef = ui.commandDefinitions.addButtonDefinition(commandID, plText.commandName, "", "./Resources/ProtoLabsCommand")
    plCommandDef.toolClipFilename = "./Resources/ProtoLabsCommand/ToolClip.png"

    # Add command handler to the command.
    plMainCommandHandler = ProtoLabsMainCommandCreatedEventHandler()
    plCommandDef.commandCreated.add(plMainCommandHandler)
    handlers.append(plMainCommandHandler)

    # Add command to the UI.
    addAddInUIElement(ui, SOLID_WORKSPACE_ID, SOLID_PANEL_ID, SOLID_PANEL_ID_FALLBACK, plCommandDef)
    addAddInUIElement(ui, SURFACE_WORKSPACE_ID, SURFACE_PANEL_ID, SURFACE_PANEL_ID_FALLBACK, plCommandDef)

def addAddInUIElement(ui, workspaceID, panelID, backupPanelID, commandDef):

    panel = plADCore.getPanel(ui, workspaceID, panelID, backupPanelID)
    if panel:
        panelControls = panel.controls

        plEstimateMenuItem = panelControls.itemById(PL_COMMAND_ID)
        if not plEstimateMenuItem:
            # Insert after the built-in Autodesk 3D print command
            firstCommandID = panelControls.item(0).id
            plEstimateMenuItem = panelControls.addCommand(commandDef, firstCommandID, False)
            plEstimateMenuItem.isVisible = True

            logger.info('Loaded add-in into: Workspace: {0}, Menu: {1}.'.format(workspaceID, panel.id))

    logger.debug('addAddInUIElement finished')

def cleanUpCommand(ui, commandID):
    cleanUpDefinitions(ui, commandID)
    cleanUpUIElements(ui, commandID)
    handlers.clear()

def cleanUpUIElements(ui, commandID):
    cleanUpAddInUIElement(ui, SOLID_WORKSPACE_ID, SOLID_PANEL_ID, SOLID_PANEL_ID_FALLBACK, commandID)
    cleanUpAddInUIElement(ui, SURFACE_WORKSPACE_ID, SURFACE_PANEL_ID, SURFACE_PANEL_ID_FALLBACK, commandID)

    logger.debug('cleanUpUIElements finished')

def cleanUpAddInUIElement(ui, workspaceID, panelID, backupPanelID, commandID):

    panel = plADCore.getPanel(ui, workspaceID, panelID, backupPanelID)
    if panel:
        panelControls = panel.controls

        plEstimateMenuItem = panelControls.itemById(commandID)
        if plEstimateMenuItem:
            plEstimateMenuItem.deleteMe()
            logger.info('Removed add-in from: Workspace: {0}, Menu: {1}.'.format(workspaceID, panel.id))

    logger.debug('cleanUpAddInUIElement finished')

def cleanUpDefinitions(ui, commandID):
    if ui.commandDefinitions.itemById(commandID):
        ui.commandDefinitions.itemById(commandID).deleteMe()

    logger.debug('cleanUpDefinitions finished')

def setForceShutdown(value):
    global forcedShutdown
    forcedShutdown = value

    logger.debug('setForceShutdown: {0}.'.format(str(forcedShutdown)))

def testAvailableCountry():
    return _testInternet(plCore.isValidCountryUsage)

def testInternetConnection():
    return _testInternet(plCore.testInternetConnection)

def _testInternet(callback):
    result = callback()
    if result is not plCore.ConnectionStatus.SUCCESS:
        # These messages intentionally do not use handleError().
        plADCore.getUI().messageBox(plText.ConnectionStatusResponseMessages[result])

        setForceShutdown(True)
        return False
    return True

def run(context):
    try:
        from ._ProtoLabs_logging import setupLogging
        setupLogging()

        logger.info('Starting Up Protolabs Add-In.')

        adsk.autoTerminate(False)

        # Now that everything is clean, register the command.
        createCommand(plADCore.getUI(), PL_COMMAND_ID)

        logger.info('Protolabs Add-In loaded.')

    except:
        logger.exception('Failed to load Protolabs Add-In.')

        setForceShutdown(True)
        adsk.autoTerminate(True)

        logger.critical('Forced shutdown of Protolabs Add-In.')
        return

def stop(context):

    from ._ProtoLabs_logging import shutdownLogging

    try:
        logger.info('Shutting down Protolabs Add-In.')

        # Clean up commands and UI.
        cleanUpCommand(plADCore.getUI(), PL_COMMAND_ID)

        setForceShutdown(False)

        logger.info('Protolabs Add-In shutdown complete.')

        shutdownLogging()

    except:
        logger.exception('Failure during shutdown.')
        shutdownLogging()