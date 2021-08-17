#Author-Proto Labs, Inc.
#Description-Protolabs Fusion 360 Add-In
#Copyright (c) 2019 Proto Labs, Inc. All Rights Reserved.

try:
    import adsk.core
    import adsk.fusion
    import traceback

    from .packages.protolabs import _ProtoLabs_ui as plUI
except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    ui.messageBox('Failed to load imports:\n{}'.format(traceback.format_exc()))

def run(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        plUI.run(context)
    except:
        if ui:
           ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        plUI.stop(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
