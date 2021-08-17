import adsk.core, adsk.fusion, traceback
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
            if param.createdBy.name=="MiddlePinPlaneYz":
                param.expression = '-param_E1/2'
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            elif param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            elif param.createdBy.name=="PinBottom":
                param.expression = '-param_L'

        if param.role=="uSpaceDistance":
            param.expression = 'param_e'

        if param.role=="countU":
            if param.createdBy.name=="PinPattern1":
                param.expression = 'param_DPins/2'
            else:
                param.expression = 'param_DPins/2-2'

        if param.role=="rightDistance":
            if param.createdBy.name=="BodyChamferBottom":
                param.expression = '(param_A - param_A1 - param_c)/2'
            elif param.createdBy.name=="BodyChamferTop":
                param.expression = 'param_A/10'
            else:
                param.expression = 'param_b*2/3'
        if param.role=="leftDistance":
            if param.createdBy.name=="BodyChamferTop":
                param.expression = '(param_A - param_A1 - param_c)/2'
            elif param.createdBy.name=="BodyChamferBottom":
                param.expression = 'param_A/10'
            else:
                param.expression = 'param_b/3'
        #offset center dimension from origin
        if param.role=="Linear Dimension-2":
            if param.createdBy.name=="SketchPinBottom":
                param.expression = 'param_E/2'
        if param.role=="Linear Dimension-3":
            if param.createdBy.name=="SketchMiddlePinTop":
                param.expression = 'param_e/2*((param_DPins/2+1)%2)'
            if param.createdBy.name=="SketchSidePinTop":
                param.expression = 'param_e/2*(param_DPins/2-1)-param_b/2'
            if param.createdBy.name=="SketchPinBottom":
                param.expression = 'param_e/2*(param_DPins/2-1)'

def dip(params, design = None, targetComponent = None):
    # body height(A)
    A = params.get('A') or 0.508
    # body offset from seating plane (A1)
    A1 = A1 = params['A1'] if 'A1' in params else 0.038
    # terminal width (b)
    b = params.get('b') or 0.053
    # body length (D)
    D = params.get('D') or 1.969
    # terminal span (E)
    E = params.get('E') or 0.762
    # body width (E1)
    E1 = params.get('E1') or 0.66
    # pin pitch (e)
    e = params.get('e') or 0.254
    # Total pins amount
    DPins = params.get('DPins') or 16
    #terminalThickness
    c = params.get('c') or 0.02
    #terminal length from PCB top
    L = params.get('L') or 0.24
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    front_feet_num = DPins / 2
    terminal_length = (E - E1)/2
    total_pin_width = 3 * b
    pin_bend_r = min(c,terminal_length)

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    if is_parametric:
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span"))
        is_update = model_3d_utility.process_user_param(design, 'param_E1', E1, default_unit, _LCLZ("BodyWidth", "body width"))
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        is_update = model_3d_utility.process_user_param(design, 'param_c', c, default_unit, _LCLZ("TerminalThickness", "terminal thickness"))
        is_update = model_3d_utility.process_user_param(design, 'param_DPins', DPins, '', _LCLZ("Pins", "pins"))

        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update:
            middle_pin_top = root_comp.features.itemByName('MiddlePinTop')
            side_pin_top = root_comp.features.itemByName('SidePinTop')
            
            if (DPins==4):
                middle_pin_top.isSuppressed = True
            else:
                middle_pin_top.isSuppressed = False
            if (DPins==2):
                side_pin_top.isSuppressed = True
            else:
                side_pin_top.isSuppressed = False    

            return

    # Create a construction plane by offset
    sketches = root_comp.sketches

    body_plane_xy = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_xy.name = 'BodyPlaneXy'
    sketch_body = sketches.add(body_plane_xy)
    sketch_body.name = 'SketchBody'

    middle_pin_plane_yz = model_3d_utility.create_offset_plane(root_comp,root_comp.yZConstructionPlane, -E1/2)
    middle_pin_plane_yz.name = 'MiddlePinPlaneYz'
    sketch_middle_pin_top = sketches.add(middle_pin_plane_yz)
    sketch_middle_pin_top.name = 'SketchMiddlePinTop'

    sketch_side_pin_top = sketches.add(middle_pin_plane_yz)
    sketch_side_pin_top.name = 'SketchSidePinTop'

    pin_path_plane_xz = root_comp.xZConstructionPlane
    pin_path_plane_xz.name = 'PinPathPlaneXz'
    sketch_pin_path = sketches.add(pin_path_plane_xz)
    sketch_pin_path.name = 'SketchPinPath'

    pin_path_plane_xy = root_comp.xYConstructionPlane
    pin_path_plane_xy.name = 'PinPathPlaneXy'
    sketch_pin_bottom = sketches.add(pin_path_plane_xy)
    sketch_pin_bottom.name = 'SketchPinBottom'

    pin_one_mark_plane_XY = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    pin_one_mark_plane_XY.name = 'PinOneMarkPlaneXy'
    sketch_pin_one_mark = sketches.add(pin_one_mark_plane_XY)

    extrudes = root_comp.features.extrudeFeatures

    #create body and apply material
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(E1/2,D/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, '', '', end_point, 'param_E1', 'param_D', is_parametric)
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(A-A1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer
    chamfer_distance1 = (A - A1-c)/2
    chamfer_distance = A/10
    model_3d_feature.create_start_end_face_chamfer(root_comp, body, chamfer_distance1, chamfer_distance)


    ###################################
    #create pin and apply material
    body_center_z = (A+A1)/2
    #sweep path
    sketch_pin_path.isComputeDeferred = True
    sketchLines = sketch_pin_path.sketchCurves.sketchLines
    line1 = sketchLines.addByTwoPoints(adsk.core.Point3D.create(-E1/2, -body_center_z, 0), adsk.core.Point3D.create(-E1/2-terminal_length, -body_center_z, 0))
    line2 = sketchLines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-E1/2-terminal_length,0, 0))
    arc = sketch_pin_path.sketchCurves.sketchArcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, pin_bend_r)
    if is_parametric:
        sketch_pin_path.sketchDimensions.addRadialDimension(arc, adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_c'
        constraints = sketch_pin_path.geometricConstraints
        constraints.addPerpendicular(line1, line2)
        sketch_pin_path.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch_pin_path.originPoint,
                                                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = '(param_A+param_A1)/2'
        sketch_pin_path.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch_pin_path.originPoint,
                                                    adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_E1/2'
        sketch_pin_path.sketchDimensions.addDistanceDimension( line2.endSketchPoint, line1.startSketchPoint,
                                                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = '(param_A+param_A1)/2'
        sketch_pin_path.sketchDimensions.addDistanceDimension(line2.endSketchPoint, sketch_pin_path.originPoint,
                                                    adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                    adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_E/2'
    sketch_pin_path.isComputeDeferred = False
    path = root_comp.features.createPath(line1)

    #middle pin and side pin top
    center_point = adsk.core.Point3D.create(-body_center_z, -e/2*(DPins/2-3),0)
    end_point = adsk.core.Point3D.create(-body_center_z+c/2, -e/2*(DPins/2-3)+b*3/2, 0)
    model_3d_sketch.create_center_point_rectangle(sketch_middle_pin_top, center_point, '', '', end_point, 'param_c', 'param_b*3', is_parametric)
    # side pin top
    center_point = adsk.core.Point3D.create(-body_center_z, -e/2*(DPins/2-1)+b/2,0)
    end_point = adsk.core.Point3D.create(-body_center_z+c/2, -e/2*(DPins/2-1)-b/2, 0)
    model_3d_sketch.create_center_point_rectangle(sketch_side_pin_top, center_point, '', '', end_point, 'param_c', 'param_b*2', is_parametric)
    #add sketck dimensions 
    if is_parametric:
        for param in root_comp.modelParameters:
            if param.role=="Linear Dimension-2":
                if param.createdBy.name=="SketchMiddlePinTop":
                    param.expression = '(param_A+param_A1)/2'
                if param.createdBy.name=="SketchSidePinTop":
                    param.expression = '(param_A+param_A1)/2'

    #sweep middle pin and side pin top            
    sweep_prof1 = sketch_middle_pin_top.profiles[0]            
    sweeps = root_comp.features.sweepFeatures
    sweep_input = sweeps.createInput(sweep_prof1, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    middle_pin_top = sweeps.add(sweep_input)
    middle_pin_top.name = 'MiddlePinTop'
     # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, middle_pin_top.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, middle_pin_top.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    sweep_prof2 = sketch_side_pin_top.profiles[0]
    sweep_input = sweeps.createInput(sweep_prof2, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    side_pin_top = sweeps.add(sweep_input)
    side_pin_top.name = 'SidePinTop'
    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, side_pin_top.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, side_pin_top.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    #bottom of pin
    center_point = adsk.core.Point3D.create(-E1/2-terminal_length, -e/2*(DPins/2-1),0)
    end_point = adsk.core.Point3D.create(-E1/2-terminal_length+c/2, -e/2*(DPins/2-1)+b/2, 0)
    model_3d_sketch.create_center_point_rectangle(sketch_pin_bottom, center_point, '', '', end_point, 'param_c', 'param_b', is_parametric)
    prof = sketch_pin_bottom.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    pin_bottom = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(-L), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    pin_bottom.name = 'PinBottom'
    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, pin_bottom.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, pin_bottom.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    #chamfer pin bottom
    chamferFeats = root_comp.features.chamferFeatures
    edge_top = adsk.core.ObjectCollection.create()
    top_face = pin_bottom.endFaces[0]
    top_edges = top_face.edges
    edge_top.add(top_edges[1])
    edge_top.add(top_edges[3])
    chamfer_top_input = chamferFeats.createInput(edge_top, True)
    chamfer_top_input.setToTwoDistances(adsk.core.ValueInput.createByReal(b/3), adsk.core.ValueInput.createByReal(2*b/3))
    chamfered_bottom_pin = chamferFeats.add(chamfer_top_input)

    ###################################
    #pattern and mirror
    pattern_pin1 = model_3d_feature.create_mirror_and_pattern(root_comp, pin_bottom.bodies.item(0), -e, front_feet_num, root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pin1.name = 'PinPattern1'
    mirrored_side_pin = model_3d_feature.create_mirror(root_comp, side_pin_top, root_comp.xZConstructionPlane)
    model_3d_feature.create_mirror(root_comp, mirrored_side_pin, root_comp.yZConstructionPlane)
    model_3d_feature.create_mirror(root_comp, side_pin_top, root_comp.yZConstructionPlane)
    pattern_pin2 = model_3d_feature.create_mirror_and_pattern(root_comp, middle_pin_top, -e, (front_feet_num-2), root_comp.yConstructionAxis, root_comp.yZConstructionPlane)
    pattern_pin2.timelineObject.rollTo(True)
    pattern_pin2.isSymmetricInDirectionOne = True
    design.timeline.moveToEnd()
    pattern_pin2.name = 'PinPattern2'

    #pin one mark
    mark_radius = E1/7
    sketch_pin_one_mark.isComputeDeferred = True
    circle_origin = adsk.core.Point3D.create(0, D/2-0.03, 0)
    sketch_points = sketch_pin_one_mark.sketchPoints
    sk_center = sketch_points.add(circle_origin)
    sketch_pin_one_mark.sketchCurves.sketchCircles.addByCenterRadius(sk_center, mark_radius)
    if is_parametric:
        sketch_pin_one_mark.sketchDimensions.addRadialDimension(sketch_pin_one_mark.sketchCurves[0],
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_E1/7'

        sketch_pin_one_mark.sketchDimensions.addDistanceDimension(sk_center, sketch_pin_one_mark.originPoint,
                                                    adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                    adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_D/2 -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.03))
    sketch_pin_one_mark.isComputeDeferred = False
    prof = sketch_pin_one_mark.profiles[0]
    extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(-A/4), adsk.fusion.FeatureOperations.CutFeatureOperation)

    #map model param to user parameters
    if is_parametric:
        map_model_parameter(root_comp)

    if(DPins<=4):
        middle_pin_top.isSuppressed = True

def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, targetComponent = None):
    dip(params, design, targetComponent)
