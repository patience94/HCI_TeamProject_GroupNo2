# -*- coding: utf-8 -*-
# Author-MakeTime
# Description-Post files to MakeTime for quoting

import os
import tempfile
import uuid
import adsk.core, adsk.fusion, traceback
from .Packages import requests
from .Packages import sendpart

handlers = []
payload_data = dict()
init_values = dict()  # store text boxes entries

# Initialize to empty
init_values['company_name'] = ""
init_values['name'] = ""
init_values['email'] = ""
init_values['phone'] = ""
init_values['part_number'] = ""
init_values['part_count'] = "100-999"
init_values['material_type'] = ""
init_values['material_grade'] = ""

class SendDataEventHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui = []
        try:
            # Instantiate Fusion360 objects
            app = adsk.core.Application.get()
            ui = app.userInterface
            inputs = args.command.commandInputs

            # Create uuid
            transaction_id = str(uuid.uuid1())

            # Save initial values
            init_values['company_name'] = inputs.itemById('user_company_val').value
            init_values['name'] = inputs.itemById('user_name_val').value
            init_values['email'] = inputs.itemById('user_email_val').value
            init_values['phone'] = inputs.itemById('user_phone_val').value
            init_values['part_number'] = inputs.itemById('part_number_val').value
            init_values['part_count'] = inputs.itemById('part_count_val').selectedItem.name
            init_values['material_type'] = inputs.itemById('material_type_val').value
            init_values['material_grade'] = inputs.itemById('material_grade_val').value

            # Pack the Payload
            payload_data['uuid'] = transaction_id
            payload_data['user_email'] = inputs.itemById('user_email_val').value
            payload_data['user_name'] = inputs.itemById('user_name_val').value
            payload_data['user_company_name'] = inputs.itemById('user_company_val').value
            payload_data['user_phone'] = inputs.itemById('user_phone_val').value
            payload_data['part_number'] = inputs.itemById('part_number_val').value
            payload_data['material_type'] = inputs.itemById('material_type_val').value
            payload_data['material_grade'] = inputs.itemById('material_grade_val').value
            payload_data['part_count'] = inputs.itemById('part_count_val').selectedItem.name

            # Instantiate Export Manager
            current_design_context = app.activeProduct
            export_manager = current_design_context.exportManager

            # Select Part
            try:
                selected_part = inputs.itemById('upload_file').selection(0).entity
                if selected_part.objectType == adsk.fusion.Occurrence.classType():
                    selected_part = selected_part.component
            except:
                ui.messageBox('Unable to Process Selection:\n{}'.format(traceback.format_exc()))
                return

           # Export part into temp dir
            try:
                output_file_name = tempfile.mkdtemp()+'//'+ transaction_id +'.step'
                options = export_manager.createSTEPExportOptions(output_file_name, selected_part)
                export_manager.execute(options)
            except:
                ui.messageBox('Unable to Export Selection:\n{}'.format(traceback.format_exc()))
                return
            temp = {'file': open(output_file_name, 'rb')}

            # Send to platform
            response = sendpart.send('https://app.maketime.io/api/fusion360/v2/project', payload_data, temp, 30)
            ui.messageBox(response)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

        return


class MakeTimeCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui = []
        try:
            # Instantiate Fusion360 Objects
            app = adsk.core.Application.get()
            ui = app.userInterface
            cmd = args.command
            inputs = cmd.commandInputs
            cmd.isExecutedWhenPreEmpted = False

            # Instantiate SendDataEventHandler
            onSendData = SendDataEventHandler()
            cmd.execute.add(onSendData)
            handlers.append(onSendData)

            cmd.commandCategoryName = 'MakeTime Request'
            cmd.setDialogInitialSize(400, 700)
            cmd.setDialogMinimumSize(400, 700)

            # Logo here
            inputs.addTextBoxCommandInput('spacer_1', '', '', 1, True)
            inputs.addImageCommandInput('logo_image', '', './/Resources//MakeTime//MT_RevLogo1.png')
            inputs.addTextBoxCommandInput('spacer_2', '', '', 2, True)

            # Get user input
            inputs.addTextBoxCommandInput('Tell us a little about you', '', '<h3 style="color:#000000;">First, please tell us a little bit about you</h3>', 2, True)
            inputs.addStringValueInput('user_company_val', 'Company Name', init_values['company_name'])
            inputs.addStringValueInput('user_name_val', 'Your Name', init_values['name'])
            inputs.addStringValueInput('user_email_val', 'Your Email', init_values['email'])
            inputs.addStringValueInput('user_phone_val', 'Your Phone', init_values['phone'])

            inputs.addTextBoxCommandInput('spacer_3', '','<hr>', 1, True)

            inputs.addTextBoxCommandInput('Part Description', '', '<h3 style="color:#000000;">Next, please tell us about your part</h3>', 2, True)

            # Select the file to upload
            file_select = inputs.addSelectionInput('upload_file', 'Select for Upload', '')
            file_select.addSelectionFilter('Occurrences')
            file_select.addSelectionFilter('RootComponents')

            # Get user input about part
            inputs.addStringValueInput('part_number_val', 'Part Number', init_values['part_number'])

            dropdown = inputs.addDropDownCommandInput('part_count_val', '# of parts to make', adsk.core.DropDownStyles.LabeledIconDropDownStyle)
            dropdownItems = dropdown.listItems
            if 'part_count' in init_values:
                select_dropdown = init_values['part_count']
            else:
                select_dropdown = '100-999'
            if select_dropdown == '1-9':
                dropdownItems.add('1-9', True, '')
            else:
                dropdownItems.add('1-9', False, '')
            if select_dropdown == '10-99':
                dropdownItems.add('10-99', True, '')
            else:
                dropdownItems.add('10-99', False, '')
            if select_dropdown == '100-999':
                dropdownItems.add('100-999', True, '')
            else:
                dropdownItems.add('100-999', False, '')
            if select_dropdown == '1000+':
                dropdownItems.add('1000+', True, '')
            else:
                dropdownItems.add('1000+', False, '')

            inputs.addStringValueInput('material_type_val', 'Material Type', init_values['material_type'])

            inputs.addStringValueInput('material_grade_val', 'Material Grade', init_values['material_grade'])

            # Text for Disclosure
            inputs.addTextBoxCommandInput('Disclosure_Info', '', '<br />MakeTime only accepts files that are Designed For Manufacturability (DFM) ready. To begin production, we will require specific tolerances and material call outs in an associated 2D drawing. Any information you provide to MakeTime is subject to MakeTime’s <a href="https://www.maketime.io/privacy-policy/">Privacy Policy</a> and <a href="https://www.maketime.io/terms-of-use/">Terms of Use</a>, which may differ from those of Autodesk Fusion 360. Learn more at <a href="https://www.maketime.io/"> www.maketime.io</a>.', 8, True)

            # Make it button
            cmd.okButtonText = 'Make It!'

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # ui.messageBox('init new button interface')

        if ui.commandDefinitions.itemById('MakeTimeButton'):
            ui.commandDefinitions.itemById('MakeTimeButton').deleteMe()

        cmdDefs = ui.commandDefinitions

        buttonMakeTime = cmdDefs.addButtonDefinition('MakeTimeButton', 'Get parts made with MakeTime', '', './/Resources//MakeTime')
        buttonMakeTime.toolClipFilename = './/Resources//MakeTime//mt_tool_tip.png'
        MakeTimeCommandCreated = MakeTimeCommandCreatedEventHandler()
        buttonMakeTime.commandCreated.add(MakeTimeCommandCreated)
        handlers.append(MakeTimeCommandCreated)

        solidPanel = ui.allToolbarPanels.itemById('SolidMakePanel')
        surfacePanel = ui.allToolbarPanels.itemById('SurfaceMakePanel')
        buttonControl = solidPanel.controls.addCommand(buttonMakeTime, '', False)
        buttonControl = surfacePanel.controls.addCommand(buttonMakeTime, '', False)

    except:
        pass
        #if ui:
        #    ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #Cleanup
        if ui.commandDefinitions.itemById('MakeTimeButton'):
            ui.commandDefinitions.itemById('MakeTimeButton').deleteMe()

        solidPanel = ui.allToolbarPanels.itemById('SolidMakePanel')
        cntrl = solidPanel.controls.itemById('MakeTimeButton')
        if cntrl:
            cntrl.deleteMe()

        surfacePanel = ui.allToolbarPanels.itemById('SurfaceMakePanel')
        cntrl = surfacePanel.controls.itemById('MakeTimeButton')
        if cntrl:
            cntrl.deleteMe()

    except:
        pass
        #if ui:
        #    ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
