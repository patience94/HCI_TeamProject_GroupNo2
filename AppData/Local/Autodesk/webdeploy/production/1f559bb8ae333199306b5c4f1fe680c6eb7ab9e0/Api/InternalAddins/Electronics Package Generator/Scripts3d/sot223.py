import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_feature
from .Utils import model_3d_sketch
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameter(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="BodyPlaneXy":
                param.expression = 'param_A1'
            if param.createdBy.name=="CommonPinPlaneXz":
                param.expression = 'param_e/2*(param_DPins-2)'
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            elif param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            elif param.createdBy.name=="CommonPin":
                param.expression = '-param_b'
            elif param.createdBy.name=="OddPin":
                param.expression = 'param_b1/2'
        if param.role=="AgainstDistance":
            param.expression = 'param_b1/2'
        if param.role=="uSpaceDistance":
            param.expression = '-param_e'
        if param.role=="countU":
            param.expression = 'param_DPins-1'
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

def sot223(params, design = None, targetComponent = None):
    A = params.get('A') or 0.1 #Body Height
    A1 = params['A1'] if 'A1' in params else 0.01
    D = params.get('D') or 0.65 #Lead Span
    E = params.get('E') or 0.7 #Body length
    E1 = params.get('E1') or 0.35 #Body width
    e = params.get('e') or 0.2 #Terminal width
    L = params.get('L') or 0.09 #Terminal length
    b = params.get('b') or 0.07 #Terminal thickness
    b1 = params.get('b1') or 0.3 #Terminal thickness
    DPins = params.get('DPins') or 4
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    #normal value of terminal thickness from JEDEC doc, or calculate avg(min,max)
    c = 0.013

    if('terminal_thickness' not in params):
        terminal_thickness = c
    else:
        if(params['terminal_thickness']<0):
            terminal_thickness = c
        else:
            terminal_thickness = min(params['terminal_thickness'],c)

    front_feet_num = DPins - 1

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

    if is_parametric:
        unitsMgr = design.unitsManager
        default_unit = unitsMgr.defaultLengthUnits
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_b1', b1, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TabWidth", "tab width"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("Pins", "pins"))
        is_update = model_3d_utility.process_user_param(design, 'param_terminalThickness', terminal_thickness, default_unit, _LCLZ("TerminalThickness", "terminal thickness"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    # Create a construction plane by offset
    sketches = root_comp.sketches
    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    sketch_body = sketches.add(body_plane_xy)

    common_pin_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, e/2 * (front_feet_num-1))
    common_pin_plane_xz.name = 'CommonPinPlaneXz'
    sketch_common_pin = sketches.add(common_pin_plane_xz)

    odd_pin_plane_xz = root_comp.xZConstructionPlane
    odd_pin_plane_xz.name = 'OddPinPlaneXz'
    sketch_odd_pin = sketches.add(odd_pin_plane_xz)

    #pin_one_mark_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    #pin_one_mark_plane_xy.name = 'PinOneMarkPlaneXy'
    #sketch_pin_one_mark = sketches.add(pin_one_mark_plane_xy)

    extrudes = root_comp.features.extrudeFeatures

    #create body
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(E1/2,D/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, '', '', end_point, 'param_E1', 'param_D', is_parametric)
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(A-A1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body.name = 'Body'
    # apply the body material.
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    #create chamfer
    chamfer_distance1 = (A - A1-terminal_thickness)/2
    chamfer_distance = 0.2*(A - A1-terminal_thickness)
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_distance1, chamfer_distance)

    #common pin
    lead_slope =  math.tan(math.pi/15) * (A/2-terminal_thickness/2)
    body_center_z = (A+A1)/2
    model_3d_sketch.create_gull_wing_lead(sketch_common_pin, E, 'param_E/2', E1, 'param_E1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_common_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    common_pin = extrudes.add(ext_input)
    common_pin.name = 'CommonPin'
    # apply the pin material.
    model_3d_utility.apply_material(app, design, common_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    model_3d_feature.create_one_direction_pattern(root_comp, common_pin, -e, front_feet_num, root_comp.yConstructionAxis)

    #odd pin
    model_3d_sketch.create_gull_wing_lead(sketch_odd_pin, E, 'param_E/2', E1, 'param_E1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_odd_pin.profiles[0]
    extent_distance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b1/2))
    extent_distance1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b1/2))
    extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setTwoSidesExtent(extent_distance, extent_distance1)
    odd_pin = extrudes.add(extrude_input)
    odd_pin.name = 'OddPin'
    # apply the pin material.
    model_3d_utility.apply_material(app, design, odd_pin.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
 
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(odd_pin.bodies.item(0))
    #Create a move feature
    transform_pin = adsk.core.Matrix3D.create()
    transform_pin.setToRotation(math.pi, adsk.core.Vector3D.create(0,0,1), adsk.core.Point3D.create(0,0,0))
    move_feats = root_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform_pin)
    moved_odd_pin = move_feats.add(move_feature_input)

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
    sot223(params, design, targetComponent)
