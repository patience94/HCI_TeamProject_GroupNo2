import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="Radius":
            if param.createdBy.name=="Fillet1":
                param.expression = 'param_D/2 * 0.1'
        if param.role=="AlongDistance":
            if param.createdBy.name=="PinOneOffset":
                param.expression = 'param_A'
            if param.createdBy.name=="PinOne":
                param.expression = 'param_D/2 * -0.1' 
            if param.createdBy.name=="Terminal":
                param.expression = '-1.2 * board_thickness -' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.0002)) #need convert the value to default unit

def create_fillet(root_comp, ext, distance):
    fillets = root_comp.features.filletFeatures
    edgeBottom = adsk.core.ObjectCollection.create()
    bottomEdges = ext.bodies.item(0).edges
    for edgeI  in bottomEdges:
        edgeBottom.add(edgeI)

    radius1 = adsk.core.ValueInput.createByReal(distance)
    input2 = fillets.createInput()
    input2.addConstantRadiusEdgeSet(edgeBottom, radius1, True)
    input2.isG2 = False
    input2.isRollingBallCorner = True
    fillet2 = fillets.add(input2)


def radial_inductor(params, design = None, target_comp = None):

    D = params.get('D') or 1.00 #Body diameter
    A = params.get('A') or 1.10 #Body height(A)
    b = params.get('b') or 0.065 #Pin width(b)
    e = params.get('e') or 0.508 #Pin pitch(e)
    board_thickness = params.get('boardThickness') or 0.16 #Board thickness

    polarityMarker = params['isPolarized'] if 'isPolarized' in params else 0 #Polarity marker
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

    fillet_amount = D/2 * 0.1
    lead_length = 1.2 * board_thickness
    L = A/4

    color_r = params.get('color_r')
    if color_r == None: color_r = 10
    color_g = params.get('color_g')
    if color_g == None: color_g = 10
    color_b = params.get('color_b')
    if color_b == None: color_b = 10

    if not design:
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

    # Get the root component of the active design
    root_comp = design.rootComponent
    if target_comp:
        root_comp = target_comp

    # get default system unit.
    default_unit = design.unitsManager.defaultLengthUnits

    if is_parametric:
        isUpdate = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyDiameter", "body diameter"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("PinWidth", "pin width"))
        is_update = model_3d_utility.process_user_param(design, 'board_thickness', board_thickness, default_unit, _LCLZ("BoardThickness", "board thickness"))
        if isUpdate:
            rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
            body_color = model_3d_utility.get_appearance(app, design, model_3d_utility.COLOR_NAME_RADIAL_INDUCTOR_BODY)
            prop = body_color.appearanceProperties.itemById(model_3d_utility.COLOR_PROP_ID_DEFAULT)
            if prop :
                color_prop = adsk.core.ColorProperty.cast(prop)
                color_prop.value = rgb

            marker = root_comp.features.itemByName('PinOne')
            if polarityMarker:
                marker.isSuppressed = False
            else:
                marker.isSuppressed = True

            return

    # Create body.
    sketches = root_comp.sketches
    xzPlane = root_comp.xZConstructionPlane
    body_sketch = sketches.add(xzPlane)

    rect = model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(D/4, -A/2, 0), 'param_D/4', 'param_A/2',
                                                 adsk.core.Point3D.create(D/2, -A , 0), 'param_D/2', 'param_A', is_parametric)

    body_sketch.isComputeDeferred = True
    lines = body_sketch.sketchCurves.sketchLines;
    constraints = body_sketch.geometricConstraints

    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(D/2, 0, 0))
    line2 = lines.addByTwoPoints(adsk.core.Point3D.create(D/2, 0, 0), adsk.core.Point3D.create(D/2, -L , 0))
    line3 = lines.addByTwoPoints(adsk.core.Point3D.create(D/2, -L, 0), adsk.core.Point3D.create(D/2 * 0.95, -L, 0))
    line4 = lines.addByTwoPoints(adsk.core.Point3D.create(D/2 * 0.95, -L, 0), adsk.core.Point3D.create(D/2 * 0.95, -A + L, 0))
    line5 = lines.addByTwoPoints(adsk.core.Point3D.create(D/2 * 0.95, -A + L, 0), adsk.core.Point3D.create(D/2, -A + L , 0))
    line1.isConstruction = True
    line2.isConstruction = True

    #Applying constraints
    line1.startSketchPoint.isFixed = True
    constraints.addCoincident(line1.endSketchPoint, line2.startSketchPoint)
    constraints.addCoincident(line2.endSketchPoint, line3.startSketchPoint)
    constraints.addCoincident(line3.endSketchPoint, line4.startSketchPoint)
    constraints.addCoincident(line4.endSketchPoint, line5.startSketchPoint)

    constraints.addHorizontal(line1)
    constraints.addPerpendicular(line1, line2)
    constraints.addPerpendicular(line2, line3)
    constraints.addPerpendicular(line3, line4)
    constraints.addPerpendicular(line4, line5)

    if is_parametric:
        body_sketch.sketchDimensions.addDistanceDimension(body_sketch.originPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D/2'
        body_sketch.sketchDimensions.addDistanceDimension(line1.endSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/2, -A/8, 0)).parameter.expression = 'param_A/4'
        body_sketch.sketchDimensions.addDistanceDimension(line2.endSketchPoint, line3.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/2, -A/4, 0)).parameter.expression = '0.05 * param_D/2 '
        body_sketch.sketchDimensions.addDistanceDimension(line3.endSketchPoint, line4.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/2, -A/2, 0)).parameter.expression = 'param_A/2 '
        body_sketch.sketchDimensions.addDistanceDimension(line4.endSketchPoint, line5.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/2, -3 * A/4, 0)).parameter.expression = '0.05 * param_D/2 '

    #Revolving the body
    bodyprof = body_sketch.profiles.item(1)
    revolves = root_comp.features.revolveFeatures
    rev_input = revolves.createInput(bodyprof, rect.item(1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(math.pi * 2)
    rev_input.setAngleExtent(False, angle)
    ext_body = revolves.add(rev_input)
    create_fillet(root_comp, ext_body, fillet_amount)

    #Give color to the body
    body = ext_body.bodies.item(0)
    body.name = 'Inductor'
    model_3d_utility.apply_material(app, design, body, model_3d_utility.MATERIAL_ID_BODY_DEFAULT)
    model_3d_utility.apply_rgb_appearance(app, design, body, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_INDUCTOR_BODY)

    #Create terminals
    xyPlane = root_comp.xYConstructionPlane
    sketch_terminal = sketches.add(xyPlane)
    sketch_terminal.name = 'TerminalSketch'
    centerPoint = adsk.core.Point3D.create(e/2, 0, 0)
    model_3d_sketch.create_center_point_circle(sketch_terminal, centerPoint, 'param_e/2', '', b, 'param_b', is_parametric)
    term = sketch_terminal.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp, term, -lead_length - 0.0002, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    terminal.name = 'Terminal'
    # assign the pysical material to pin.
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
    # assign the apparance to pin
    model_3d_utility.apply_appearance(app, design, terminal.bodies.item(0), model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)

    model_3d_feature.create_mirror(root_comp, terminal, root_comp.yZConstructionPlane)

    #Draw pin marker
    pin_one_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    pin_one_offset.name = 'PinOneOffset'
    sketch_pin_one = sketches.add(pin_one_offset)
    sketch_pin_one.name ='PinOneSketch'
    centerPoint = adsk.core.Point3D.create(-D/2 + 2 * fillet_amount + 0.01 * D, 0, 0)
    model_3d_sketch.create_center_point_circle(sketch_pin_one, centerPoint, 'param_D/2 - param_D * 0.2', '',  0.01 * D, '0.1 * param_D', is_parametric)
    pin = sketch_pin_one.profiles.item(0)
    pin_one = model_3d_feature.create_extrude(root_comp, pin, -D/2 * 0.1, adsk.fusion.FeatureOperations.CutFeatureOperation)
    pin_one.name = 'PinOne'

    if not polarityMarker:
        pin_one.isSuppressed = True

    if is_parametric:
        map_model_parameters(root_comp)

def run(context):
    ui = app.userInterface

    try:
        runWithInput(context)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def runWithInput(params, design = None, targetComponent = None):
    radial_inductor(params, design, targetComponent)
