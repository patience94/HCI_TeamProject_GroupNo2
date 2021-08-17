#Author-Proto Labs, Inc.
#Description-Protolabs Autodesk Core (UI) helpers
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

import adsk.core

from ._ProtoLabs_logging import getRootLogger

logger = getRootLogger().getChild('_ProtoLabs_ADCore')

def getUI():
    app = adsk.core.Application.get()
    return app.userInterface

def getPanel(ui, workspaceID, panelID, backupPanelID):

    panel = None

    workspace = ui.workspaces.itemById(workspaceID)
    if workspace:
        panel = workspace.toolbarPanels.itemById(panelID)
        if panel is None:
            panel =  workspace.toolbarPanels.itemById(backupPanelID)

    return panel

