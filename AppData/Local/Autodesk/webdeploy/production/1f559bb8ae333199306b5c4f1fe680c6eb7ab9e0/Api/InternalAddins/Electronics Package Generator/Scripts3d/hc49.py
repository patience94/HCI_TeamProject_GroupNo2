import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="SideBody":
                param.expression = 'param_E * 0.1'
            if param.createdBy.name=="MidBody":
                param.expression = 'param_A'
            if param.createdBy.name=="Terminal":
                param.expression = '-1.2 * board_thickness'

        if param.role=="Radius":
            param.expression = 'param_E * 0.05'

        if param.role=="Linear Dimension-8":
            if param.createdBy.name=="BodySketch":
                param.value = 0.02  #use internal unit cm

def create_fillet(root_comp, ext, distance):
    fillets = root_comp.features.filletFeatures
    edgeTop = adsk.core.ObjectCollection.create()
    topFace = ext.endFaces[0]
    topEdges = topFace.edges
    for edgeI  in topEdges:
            edgeTop.add(edgeI)

    radius = adsk.core.ValueInput.createByReal(distance)
    input1 = fillets.createInput()
    input1.addConstantRadiusEdgeSet(edgeTop, radius, True)
    input1.isG2 = False
    input1.isRollingBallCorner = True
    fillet1 = fillets.add(input1)

def hc49(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    #get the default unit of the system.  need consider to set the right unit. consider if user use the imperial unit.
    #define default value of the input paramters of diode. unit is mm
    b = params.get('b') or 0.06 #TerminalWidth(b)
    D = params.get('D') or 1.12 #Body length(D)
    E = params.get('E') or 0.485 #Body width(E)
    A = params.get('A') or 0.35 #Body height(A)
    e = params.get('e') or 0.488 #pitch
    board_thickness = params.get('boardThickness') or 0.16 #board thickness
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    #boardThickness = 0.16
    lead_length = 1.2 * board_thickness
    D1 = D - E * 0.2
    E1 = E * 0.8

    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("Pitch", "pitch"))
        is_update = model_3d_utility.process_user_param(design, 'board_thickness', board_thickness, default_unit, _LCLZ("BoardThickness", "board thickness"))
        if isUpdate: return

    # Create body
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    body_sketch = sketches.add(xyPlane)
    body_sketch.name = 'BodySketch'
    body = model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0, 0, 0),'', '',  adsk.core.Point3D.create(D/2 - E/2, E/2, 0), 'param_D - param_E', 'param_E', is_parametric)

    lines = body_sketch.sketchCurves.sketchLines;
    constraints = body_sketch.geometricConstraints
    line_odd = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(D/2, 0, 0))
    line_even = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-D/2, 0, 0))
    line_odd.startSketchPoint.isFixed = True
    line_even.startSketchPoint.isFixed = True
    constraints.addHorizontal(line_odd)
    constraints.addHorizontal(line_even)
    line_odd.isConstruction = True
    line_even.isConstruction = True

    arcs = body_sketch.sketchCurves.sketchArcs;
    arcs_odd = arcs.addByCenterStartSweep(adsk.core.Point3D.create(D/2 - E/2, 0 , 0), adsk.core.Point3D.create(D/2 - E/2, E/2, 0), -math.pi)
    arcs_even = arcs.addByCenterStartSweep(adsk.core.Point3D.create(-D/2 + E/2, 0 , 0), adsk.core.Point3D.create(-D/2 + E/2, E/2, 0), math.pi)
    constraints.addCoincident(arcs_odd.centerSketchPoint, line_odd.endSketchPoint)
    constraints.addCoincident(arcs_even.centerSketchPoint, line_even.endSketchPoint)

    if is_parametric:

        body_sketch.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, line_odd.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D/2 - param_E/2'
        body_sketch.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, line_even.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-D/4, 0, 0)).parameter.expression = 'param_D/2 - param_E/2'
        body_sketch.sketchDimensions.addRadialDimension(arcs_odd, adsk.core.Point3D.create(D/2, 0, 0)).parameter.expression = 'param_E/2'
        body_sketch.sketchDimensions.addRadialDimension(arcs_even, adsk.core.Point3D.create(-D/2, 0, 0)).parameter.expression = 'param_E/2'

    constraints.addCoincident(arcs_odd.endSketchPoint, body.item(0).startSketchPoint)

    #Create offset
    entities = adsk.core.ObjectCollection.create()
    entities.add(arcs_odd)
    entities.add(arcs_even)
    entities.add(body.item(0))
    entities.add(body.item(2))
    dir_point = adsk.core.Point3D.create(0, 0.5, 0)
    offset_curves = body_sketch.offset(entities, dir_point, 0.02)

    #Create extrusion
    profile = adsk.core.ObjectCollection.create()
    profile.add(body_sketch.profiles.item(0))
    profile.add(body_sketch.profiles.item(1))
    profile.add(body_sketch.profiles.item(3))

    mid_body = model_3d_feature.create_extrude(root_comp,profile, A, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    mid_body.name = 'MidBody'

    profile.add(body_sketch.profiles.item(2))
    side_body = model_3d_feature.create_extrude(root_comp,profile, E * 0.1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    side_body.name = 'SideBody'

    create_fillet(root_comp, side_body, E * 0.05)
    create_fillet(root_comp, mid_body, E * 0.05)

    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, mid_body.bodies.item(0), model_3d_utility.MATERIAL_ID_ALUMINUM)
    model_3d_utility.apply_material(app, design, side_body.bodies.item(0), model_3d_utility.MATERIAL_ID_ALUMINUM)

    #Create terminals
    xyPlane = root_comp.xYConstructionPlane
    sketch_term = sketches.add(xyPlane)
    sketch_term.name = 'TerminalSketch'
    centerPoint = adsk.core.Point3D.create(e/2, 0, 0)
    model_3d_sketch.create_center_point_circle(sketch_term, centerPoint, 'param_e/2', '', b, 'param_b', is_parametric)
    ext_term = sketch_term.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp, ext_term, -lead_length, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    terminal.name = 'Terminal'

    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    #mirror the terminal
    model_3d_feature.create_mirror(root_comp, terminal, root_comp.yZConstructionPlane)

    if is_parametric:
        map_model_parameters(root_comp)

def run(context):
    ui = app.userInterface
    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, target_comp = None):
    hc49(params, design, target_comp)
