import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameter(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneXy":
                param.expression = 'param_A1'
            if param.createdBy.name=="FrontPinPlaneXz":
                param.expression = '-(round((param_DPins - 1) / 2)-1)/2*param_e1'
            if param.createdBy.name=="BackPinPlaneXz":
                param.expression = '(param_DPins-round((param_DPins - 1) / 2)-1)/2*param_e'

            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            elif param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            elif param.createdBy.name=="front_pin" or param.createdBy.name=="back_pin":
                param.expression = '-param_b'
        if param.role=="countU":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'round((param_DPins - 1) / 2)'
            if param.createdBy.name=="PinPattern2":
                param.expression = 'param_DPins-round((param_DPins - 1) / 2)'
        if param.role=="uSpaceDistance":
            if param.createdBy.name=="PinPattern1":
                param.expression = '-param_e1'
            if param.createdBy.name=="PinPattern2":
                param.expression = '-param_e'

        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
            else:
                param.expression = 'param_A/10'
        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
            else:
                param.expression = 'param_A/10'

def sot23(params, design = None, targetComponent = None):
    A = params.get('A') or 0.117 #Body Height
    A1 = params['A1'] if 'A1' in params else 0.01 #Body offset
    D = params.get('D') or 0.29 #Lead Span
    E = params.get('E') or 0.24 #Body length
    E1 = params.get('E1') or 0.13 #Body width
    e = params.get('e') or 0.095 #Terminal width
    e1 = params.get('e1') or 0.095 #Terminal width
    L = params.get('L') or 0.05 #Terminal length
    b = params.get('b') or 0.044 #Terminal thickness
    DPins = params.get('DPins') or 6 #pins
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    #normal value of terminal thickness from JEDEC doc, or calculate avg(min,max)
    c = 0.013

    if('terminalThickness' not in params):
        terminal_thickness = c
    else:
        if(params['terminalThickness']<0):
            terminal_thickness = c
        else:
            terminal_thickness = min(params['terminalThickness'],c)

    front_feet_num = math.ceil((DPins - 1) / 2)
    print(front_feet_num)
    back_feet_num = DPins - front_feet_num

    if ('e1' not in params):
    	#e1 is used for placing front pins and e is used for back pins
        e1 = 2 * e if(front_feet_num == 2) else e

    #update back pin pitch if backpin number is 2
    if(back_feet_num == 2):
        e = 2 * e

    chamfer_distance = (A-A1-terminal_thickness)/2
    chamfer_distance1 = A/10

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

    if is_parametric:
        # get default system unit.
        default_unit = design.unitsManager.defaultLengthUnits
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_e1', e1, default_unit, _LCLZ("Pitch", "pitch")) #:todo need to verify requrement
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("Pins", "pins")) #:todo need to verify requrement
        is_update = model_3d_utility.process_user_param(design, 'param_terminalThickness', terminal_thickness, default_unit, _LCLZ("TerminalThickness", "terminal thickness"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    # Create a new sketch.
    sketches = root_comp.sketches
    # Create a construction plane by offset
    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    sketch_body = sketches.add(body_plane_xy)

    front_pin_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, e1*(front_feet_num - 1)/2)
    front_pin_plane_xz.name = 'FrontPinPlaneXz'
    sketch_front_pin = sketches.add(front_pin_plane_xz)

    back_pin_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, e*(back_feet_num - 1)/2)
    back_pin_plane_xz.name = 'BackPinPlaneXz'
    sketch_back_pin = sketches.add(back_pin_plane_xz)

    #pin_one_mark_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    #pin_one_mark_plane_xy.name = 'PinOneMarkPlaneXy'
    #sketch_pin_one_mark = sketches.add(pin_one_mark_plane_xy)

    extrudes = root_comp.features.extrudeFeatures

    #body
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(E1/2,D/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, '', '', end_point, 'param_E1', 'param_D', is_parametric)
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(A-A1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer
    chamfer_distance = (A - A1-terminal_thickness)/2
    chamfer_distance1 = 0.2*(A - A1-terminal_thickness)
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_distance, chamfer_distance1)

    #normal pins
    body_center_z = (A+A1)/2
    lead_slope =  0
    model_3d_sketch.create_gull_wing_lead(sketch_front_pin, E, 'param_E/2', E1, 'param_E1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_front_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    front_pin = extrudes.add(ext_input)
    front_pin.name = 'FrontPin'
    model_3d_utility.apply_material(app, design, front_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(front_pin.bodies.item(0))
    # Create a move feature
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(math.pi, adsk.core.Vector3D.create(0,0,1), adsk.core.Point3D.create(0,0,0))
    moveFeats = root_comp.features.moveFeatures
    moveFeatureInput = moveFeats.createInput(bodies, transform)
    movedFrontPin = moveFeats.add(moveFeatureInput)
    pattern_pins1 = model_3d_feature.create_one_direction_pattern(root_comp, front_pin.bodies.item(0), e1, front_feet_num, root_comp.yConstructionAxis)
    pattern_pins1.name = 'PinPattern1'

    model_3d_sketch.create_gull_wing_lead(sketch_back_pin, E, 'param_E/2', E1, 'param_E1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_back_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    back_pin = extrudes.add(ext_input)
    back_pin.name = 'BackPin'
    model_3d_utility.apply_material(app, design, back_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    pattern_pins2 = model_3d_feature.create_one_direction_pattern(root_comp, back_pin.bodies.item(0), -e, back_feet_num, root_comp.yConstructionAxis)
    pattern_pins2.name = 'PinPattern2'

    #pin one body marking
    #model_3d_utility.create_pin_one_mark(sketch_pin_one_mark, extrudes, A, D, E1, chamfer_distance1, 'param_D/2', is_parametric)
    model_3d_utility.create_pin_one_mark(root_comp, A, 'param_A', D, 'param_D', E1, 'param_E1', is_parametric)

    #map model param to user parameters
    if is_parametric:
        map_model_parameter(root_comp)

def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, targetComponent = None):
    sot23(params, design, targetComponent)
