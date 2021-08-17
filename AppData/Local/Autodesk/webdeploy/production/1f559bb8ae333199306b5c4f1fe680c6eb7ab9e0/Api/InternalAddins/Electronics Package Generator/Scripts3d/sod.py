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
            if param.createdBy.name=="PinOneMarkPlaneXy":
                param.expression = 'param_A'
            elif param.createdBy.name=="Body":
                param.expression = 'param_A - param_A1'
            elif param.createdBy.name=="Pin1":
                param.expression = 'param_b'


        if param.createdBy.name== "Chamfer2":
            if param.role == "rightDistance":
                param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
            else:
                    param.expression = 'param_A/10'
        if param.createdBy.name== "Chamfer1":
            if param.role == "rightDistance":
                param.expression = 'param_A/10'
            else:
                    param.expression = '(param_A - param_A1 - param_terminalThickness)/2'
def sod(params, design = None, targetComponent = None):
    A = params.get('A') or 0.127 #Body Height
    A1 = params['A1'] if 'A1' in params else 0.02 #Body offset
    D = params.get('D') or 0.375 #Lead Span
    D1 = params.get('D1') or 0.27 #Body length
    E = params.get('E') or 0.16 #Body width
    b = params.get('b') or 0.065 #Terminal width
    L = params.get('L') or 0.0285 #Terminal length
    c = params.get('c') or 0.015 #Terminal thickness
    deg = params.get('deg') or 8
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    p = min(D1/6,1) # Polarity band size

    if('terminalThickness' not in params):
        terminal_thickness = c
    else:
        if(params['terminalThickness']<0):
            terminal_thickness = c
        else:
            terminal_thickness = min(params['terminalThickness'],c)

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design.
    root_comp = design.rootComponent

    if targetComponent:
        root_comp = targetComponent

    if is_parametric:
        units = design.unitsManager
        default_unit = units.defaultLengthUnits
        is_update = False
        is_update = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        is_update = model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        is_update = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("Span", "span") + "1")
        is_update = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        is_update = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("Span", "span") + "2")
        is_update = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        is_update = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalLength", "terminal length"))
        is_update = model_3d_utility.process_user_param(design, 'param_terminalThickness', terminal_thickness, default_unit, _LCLZ("TerminalThickness", "terminal thickness"))
        # the paramters are already there, just update the models with the paramters. will skip the model creation process.
        if is_update: return

    # Create a construction plane by offset
    sketches = root_comp.sketches
    body_plane_XY = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    body_plane_XY.name = 'BodyPlaneXy'
    sketch_body = sketches.add(body_plane_XY)

    pin_plane_XZ = root_comp.xZConstructionPlane
    pin_plane_XZ.name = 'PinPlaneXz'
    sketch_pin = sketches.add(pin_plane_XZ)

    pin_one_mark_plane_XY = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    pin_one_mark_plane_XY.name = 'PinOneMarkPlaneXy'
    sketch_pin_one_mark = sketches.add(pin_one_mark_plane_XY)

    extrudes = root_comp.features.extrudeFeatures

    #create body and apply material
    center_point = adsk.core.Point3D.create(0,0,0)
    end_point = adsk.core.Point3D.create(D1/2,E/2,0)
    model_3d_sketch.create_center_point_rectangle(sketch_body, center_point, '', '', end_point, 'param_D1', 'param_E', is_parametric)
    prof = sketch_body.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(A-A1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)

    # create chamfer
    edge_bottom = adsk.core.ObjectCollection.create()
    bottom_face = body.endFaces[0]
    bottom_edges = bottom_face.edges
    edge_bottom.add(bottom_edges[0])
    edge_bottom.add(bottom_edges[2])

    edge_top = adsk.core.ObjectCollection.create()
    top_face = body.startFaces[0]
    top_edges = top_face.edges
    edge_top.add(top_edges[0])
    edge_top.add(top_edges[2])
    chamfer_distance = (A - A1-terminal_thickness)/2
    chamfer_distance1 = math.tan((deg / 180) * math.pi)* chamfer_distance

    chamfer_feats = root_comp.features.chamferFeatures
    chamfer_top = chamfer_feats.createInput(edge_top, True)
    chamfer_bottom = chamfer_feats.createInput(edge_bottom, True)
    chamfer_top.setToTwoDistances(adsk.core.ValueInput.createByReal(chamfer_distance), adsk.core.ValueInput.createByReal(chamfer_distance1))
    chamfer_bottom.setToTwoDistances(adsk.core.ValueInput.createByReal(chamfer_distance1), adsk.core.ValueInput.createByReal(chamfer_distance))
    chamfer_feats.add(chamfer_top)
    chamfer_feats.add(chamfer_bottom)

    #polarity marking
    lines = sketch_pin_one_mark.sketchCurves.sketchLines
    start_point = adsk.core.Point3D.create(-D1/2+D1/6,-E/2,0)
    end_point = adsk.core.Point3D.create(-D1/2+D1/6+p,E/2,0)
    lines.addTwoPointRectangle(start_point, end_point)
    # Constrain the Rectangle to stay rectangular
    constraints = sketch_pin_one_mark.geometricConstraints
    constraints.addPerpendicular(lines.item(0), lines.item(1))
    constraints.addHorizontal(lines.item(0))
    constraints.addParallel(lines.item(0), lines.item(2))
    constraints.addParallel(lines.item(1), lines.item(3))

    center_point = adsk.core.Point3D.create(0,0,0)
    sketch_points = sketch_pin_one_mark.sketchPoints
    sk_center = sketch_points.add(center_point)
    center_point.isfixed = True

    # Dimension the rectangle with the user parameters
    if is_parametric:
        sketch_pin_one_mark.sketchDimensions.addDistanceDimension(lines.item(0).startSketchPoint, lines.item(0).endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(0, D1, 0)).parameter.expression = 'param_D1/6'
        sketch_pin_one_mark.sketchDimensions.addDistanceDimension(lines.item(1).startSketchPoint, lines.item(1).endSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(E, 0, 0)).parameter.expression = 'param_E'
        line_c = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, 0.1, 0))
        line_c1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0.1, 0, 0))
        line_c.isConstruction = True
        line_c.isFixed = True
        line_c1.isConstruction = True
        line_c1.isFixed = True
        sketch_pin_one_mark.sketchDimensions.addDistanceDimension(line_c1.startSketchPoint, lines.item(0).startSketchPoint,
                                                        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_E/2'
        sketch_pin_one_mark.sketchDimensions.addDistanceDimension(line_c.startSketchPoint, lines.item(3).startSketchPoint,
                                                        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                        adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = 'param_D1/3'
    prof = sketch_pin_one_mark.profiles[0]

    polarity_mark = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(0.0002), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    #pins
    body_center_z = (A+A1)/2
    lead_slope =  math.tan(math.pi/20) * (A/2-terminal_thickness/2)
    model_3d_sketch.create_gull_wing_lead(sketch_pin, D, 'param_D/2', D1, 'param_D1/2', body_center_z, terminal_thickness, L, lead_slope, is_parametric)
    prof = sketch_pin.profiles[0]
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(b)
    ext_input.setSymmetricExtent(distance, True)
    pin1 = extrudes.add(ext_input)
    pin1.name = 'Pin1'
    # apply the pin material.
    model_3d_utility.apply_material(app, design, pin1.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)
    #mirror
    model_3d_feature.create_mirror(root_comp, pin1.bodies[0], root_comp.yZConstructionPlane)

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
    sod(params, design, targetComponent)
