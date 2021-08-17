import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="LowBody":
                param.expression = 'param_A/4'
            if param.createdBy.name=="TopBodyOffset":
                param.expression = 'param_A/4'
            if param.createdBy.name=="SideBody":
                param.expression = 'param_A * 3/4 * 0.1'
            if param.createdBy.name=="MidBody":
                param.expression = 'param_A* 3/4'


def create_fillet(root_comp, ext, distance):
    fillets = root_comp.features.filletFeatures
    edgeTop = adsk.core.ObjectCollection.create()
    topFace = ext.endFaces[0];
    topEdges = topFace.edges
    for edgeI  in topEdges:
            edgeTop.add(edgeI)

    radius = adsk.core.ValueInput.createByReal(distance)
    input1 = fillets.createInput()
    input1.addConstantRadiusEdgeSet(edgeTop, radius, True)
    input1.isG2 = False
    input1.isRollingBallCorner = True
    fillet1 = fillets.add(input1)

def crystal(params, design = None, target_comp = None):

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    b = params.get('b') or 0.079 #TerminalWidth(b)
    L = params.get('L') or 0.416  #Terminal length(L)[optional]
    #D = params.get('D') or 1.32 #Terminal span(D)[optional]
    D2 = params.get('D2') or 0.488 #Terminal gap(D2)[optional]
    E = params.get('E') or 0.5 #Body width(E)
    D1 = params.get('D1') or 1.17 #Body length(D1)
    A = params.get('A') or 0.45 #Body height
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    A1 = 1/4 * A
    terminal_thickness = 0.03

    if is_parametric:
        unitsMgr = design.unitsManager
        mm = unitsMgr.defaultLengthUnits
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("TerminalWidth", "terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("TerminalLength", "terminal length"))
        #isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("TerminalSpan", "terminal span"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D2', D2, default_unit, _LCLZ("TerminalGap", "terminal gap"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D1', D1, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        if isUpdate: return

    #Create body
    sketches = root_comp.sketches
    xyPlane = root_comp.xYConstructionPlane
    low_body_offset =  model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, 0.0001)
    low_body_sketch = sketches.add(low_body_offset)
    low_body_sketch.name = 'LowBodySketch'

    model_3d_sketch.create_center_point_rectangle(low_body_sketch, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(D1/2, E/2, 0), 'param_D1', 'param_E', is_parametric)
    ext_low_body = low_body_sketch.profiles.item(0)
    low_body = model_3d_feature.create_extrude(root_comp,ext_low_body, A1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    low_body.name = 'LowBody'
    
    # assign the pysical material and appearance to body
    model_3d_utility.apply_material(app, design, low_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
    model_3d_utility.apply_appearance(app, design, low_body.bodies.item(0), model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)


    top_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    top_body_offset.name = 'TopBodyOffset'
    top_body_sketch = sketches.add(top_body_offset)
    top_body_sketch.name = 'TopBodySketch'

    top_body = model_3d_sketch.create_center_point_rectangle(top_body_sketch, adsk.core.Point3D.create(0, 0, 0),'', '',
                                                            adsk.core.Point3D.create(0.45 * D1 - 0.4 * E, 0.45 * E, 0), 'param_D1 * 0.9 - param_E * 0.8', 'param_E * 0.9', is_parametric)

    lines = top_body_sketch.sketchCurves.sketchLines;
    constraints = top_body_sketch.geometricConstraints
    line_odd = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0.45 * D1 - 0.4 * E, 0, 0))
    line_even = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-0.45 * D1 + 0.4 * E, 0, 0))
    line_odd.startSketchPoint.isFixed = True
    line_even.startSketchPoint.isFixed = True
    constraints.addHorizontal(line_odd)
    constraints.addHorizontal(line_even)
    line_odd.isConstruction = True
    line_even.isConstruction = True

    arcs = top_body_sketch.sketchCurves.sketchArcs;
    arcs_odd = arcs.addByCenterStartSweep(adsk.core.Point3D.create(0.45 * D1 - 0.4 * E, 0 , 0), adsk.core.Point3D.create(0.45 * D1 - 0.4 * E, 0.45 * E, 0), -math.pi)
    arcs_even = arcs.addByCenterStartSweep(adsk.core.Point3D.create(-0.45 * D1 + 0.4 * E, 0 , 0), adsk.core.Point3D.create(-0.45 * D1 + 0.4 * E, 0.45 * E, 0), math.pi)
    constraints.addCoincident(arcs_odd.centerSketchPoint, line_odd.endSketchPoint)
    constraints.addCoincident(arcs_even.centerSketchPoint, line_even.endSketchPoint)

    if is_parametric:

        top_body_sketch.sketchDimensions.addDistanceDimension(line_odd.startSketchPoint, line_odd.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D1/4, 0, 0)).parameter.expression = '0.45 * param_D1 - 0.4 * param_E'
        top_body_sketch.sketchDimensions.addDistanceDimension(line_even.startSketchPoint, line_even.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(-D1/4, 0, 0)).parameter.expression = '0.45 * param_D1 - 0.4 * param_E'
        top_body_sketch.sketchDimensions.addRadialDimension(arcs_odd, adsk.core.Point3D.create((D2 + L * 2)/2, 0, 0)).parameter.expression = 'param_E * 0.45'
        top_body_sketch.sketchDimensions.addRadialDimension(arcs_even, adsk.core.Point3D.create(-(D2 + L * 2)/2, 0, 0)).parameter.expression = 'param_E * 0.45'

    constraints.addCoincident(arcs_odd.endSketchPoint, top_body.item(0).startSketchPoint)

    #Create offset
    entities = adsk.core.ObjectCollection.create()
    entities.add(arcs_odd)
    entities.add(arcs_even)
    entities.add(top_body.item(0))
    entities.add(top_body.item(2))
    dir_point = adsk.core.Point3D.create(0, 0, 0)
    offset_curves = top_body_sketch.offset(entities, dir_point, -0.005)

    #Create extrusion
    profile = adsk.core.ObjectCollection.create()
    profile.add(top_body_sketch.profiles.item(0))
    profile.add(top_body_sketch.profiles.item(1))
    profile.add(top_body_sketch.profiles.item(3))

    mid_body = model_3d_feature.create_extrude(root_comp, profile, (A - A1) , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    mid_body.name = 'MidBody'

    prof = top_body_sketch.profiles.item(2)    
    side_body = model_3d_feature.create_extrude(root_comp,prof, (A - A1) * 0.1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    side_body.name = 'SideBody'
    
    #Create fillet o the top face edges
    create_fillet(root_comp, mid_body, 0.03)

    # assign the pysical material to body.
    model_3d_utility.apply_material(app, design, mid_body.bodies.item(0), model_3d_utility.MATERIAL_ID_ALUMINUM)
    model_3d_utility.apply_material(app, design, side_body.bodies.item(0), model_3d_utility.MATERIAL_ID_ALUMINUM)

    #Draw terminals
    terminal_sketch = sketches.add(xyPlane)
    terminal_sketch.name = 'TerminalSketch'
    model_3d_sketch.create_center_point_rectangle(terminal_sketch, adsk.core.Point3D.create(D2/2  + L/2 , 0, 0), 'param_D2/2 + param_L/2' , '', adsk.core.Point3D.create(D2/2+ L, b/2, 0), 'param_L', 'param_b', is_parametric)
    ext_terminal = terminal_sketch.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp,ext_terminal, terminal_thickness, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'Terminal'
    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    #mirroe the terminal
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
    crystal(params, design, target_comp)
