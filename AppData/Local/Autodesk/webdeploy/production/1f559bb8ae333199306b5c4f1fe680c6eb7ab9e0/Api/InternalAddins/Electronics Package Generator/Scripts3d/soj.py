import adsk.core,traceback, adsk.fusion, math
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
            if param.createdBy.name=="PinPathPlaneXz":
                param.expression = '((param_DPins/2 - 1)*param_e)/2'
            if param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            if param.createdBy.name=="PinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="PinBodyBottom":
                param.expression = 'param_b/2'
        if param.role=="AgainstDistance":
            if param.createdBy.name=="PinBodySide":
                param.expression = 'param_b'
            if param.createdBy.name=="PinBodyBottom":
                param.expression = 'param_b/2'

        if param.role=="uSpaceDistance":
            param.expression = '-param_e'

        if param.role=="countU":
            if param.createdBy.name=="PinPattern":
                param.expression = 'param_DPins/2'
            else:
                param.expression = 'param_DPins/2-2'

        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '(param_A - param_A1 - '+str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)) + ')/2'
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '0.2*(param_A - param_A1 - '+str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)) + ')'

        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A - param_A1 - '+str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD))+')/2'
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '0.2*(param_A - param_A1 - '+str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)) + ')'

        if param.role == 'Diameter Dimension-3' and param.createdBy.name=="PinPathSketch":
                param.expression = 'param_E - param_E2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD*2))

        if param.role == 'Linear Dimension-5' and param.createdBy.name=="PinPathSketch":
                param.expression = 'param_A/2 + param_A1/2 +' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, model_3d_sketch.TERMINAL_THICKNESS_J_LEAD/2))

def soj(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits


    A = params.get('A') or 0.356    # body height(A)
    A1 = params.get('A1') or 0.101  # body offset from seating plane (A1)
    b = params.get('b') or 0.0435   # terminal width (b)
    D = params.get('D') or 1.28     # body length (D)
    E = params.get('E') or 0.866    # terminal span (E)
    E1 = params.get('E1') or 0.752  # body width (E1)
    E2 = params.get('E2') or 0.68   # body width (E2)
    e = params.get('e') or 0.127    # pin pitch (e)
    DPins = params.get('EPins') or 20 # Total pins amount
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    if is_parametric:
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", 'body offset'))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_E2', E2, default_unit, _LCLZ("PinWidth", "pin width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("Pins", "pins"))

        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    sketches = root_comp.sketches
    # Step1 create pin plane and sketches
    pin_path_plane_xz = model_3d_utility.create_offset_plane(root_comp, root_comp.xZConstructionPlane, ((DPins/2 - 1)*e)/2 )
    pin_path_plane_xz.name = 'PinPathPlaneXz'
    pin_path_sketch = sketches.add(pin_path_plane_xz)
    pin_path_sketch.name = 'PinPathSketch'

    #create J lead profile
    model_3d_sketch.create_j_lead(pin_path_sketch, E1, 'param_E1', E, 'param_E', E2, 'param_E2', A, 'param_A', A1, 'param_A1', is_parametric)
    bottom_profile = pin_path_sketch.profiles.item(0)
    side_profile = pin_path_sketch.profiles.item(1)

    # Step2 create the pin body
    extrudes = root_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(side_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    extent_distance_1 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b))
    extent_distance_2 = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(b/2))
    extrude_input.setTwoSidesExtent(extent_distance_1,extent_distance_1)
    extru_side_body = extrudes.add(extrude_input)
    extru_side_body.name = 'PinBodySide'

    extrude_input = extrudes.createInput(bottom_profile, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    extrude_input.setTwoSidesExtent(extent_distance_2,extent_distance_2)
    extru_bottom_body = extrudes.add(extrude_input)
    extru_bottom_body.name = 'PinBodyBottom'

    # apply the pin material.
    model_3d_utility.apply_material(app, design, extru_bottom_body.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, extru_bottom_body.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    #step3 create construction plane to generate the body sketch
    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    body_sketch = sketches.add(body_plane_xy)
    body_sketch.name = 'BodySketch'

    #step4  create the body
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0,0,0), '', '', adsk.core.Point3D.create(E1/2,D/2,0), 'param_E1', 'param_D', is_parametric)
    ext_body = model_3d_feature.create_extrude(root_comp,body_sketch.profiles.item(0), A-A1 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    ext_body.name = 'Body'
    model_3d_utility.apply_material(app, design, ext_body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer of base body
    chamfer_distance = (A - A1 - model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)/2
    chamfer_distance1 = 0.2*(A - A1 - model_3d_sketch.TERMINAL_THICKNESS_J_LEAD)
    model_3d_feature.create_start_end_face_chamfer(root_comp, ext_body, chamfer_distance1, chamfer_distance)


    # Step5 create pin mirror and Pattern
    pattern_pins = model_3d_feature.create_mirror_and_pattern(root_comp, extru_bottom_body.bodies.item(0), e, DPins/2, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pins.name = 'PinPattern'

    # step6 create the pin one mark.
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

def runWithInput(params, design = None, target_comp = None):
    soj(params, design, target_comp)
