import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="LowBodyOffset":
                param.expression = 'param_A1'
            if param.createdBy.name=="LowerBody":
                param.expression = 'param_A * 0.2'
            if param.createdBy.name=="MidBodyOffset":
                param.expression = 'param_A1 + 0.2 * param_A'            
            if param.createdBy.name=="LightSourceOffset":
                param.expression = 'param_A1 + 0.5 * param_A'
            if param.createdBy.name=="MidBody":
                param.expression = '0.8 * param_A - 0.9 * param_D/2'
            if param.createdBy.name=="TopBodyOffset":
                param.expression = 'param_A1 + param_A - 0.9 * param_D/2'
            if param.createdBy.name=="Terminal":
                param.expression = '-1.2 * board_thickness - param_A1'
            if param.createdBy.name=="TerminalOffset":
                param.expression = 'param_A1'

def create_terminals(root_comp, isRectangularTerminal, A1, is_parametric, lead_length, e, b, c):
        sketches = root_comp.sketches
        terminal_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
        terminal_offset.name = 'TerminalOffset'
        sketch_terminal = sketches.add(terminal_offset)
        sketch_terminal.name = 'TerminalSketch'
        if(isRectangularTerminal == 0):
            centerPoint = adsk.core.Point3D.create(e/2, 0, 0)
            model_3d_sketch.create_center_point_circle(sketch_terminal, centerPoint, '', '', b, 'param_b', is_parametric)
            prof_ter = sketch_terminal.profiles.item(0)
        else:
            centerPoint = adsk.core.Point3D.create(e/2, 0, 0)
            model_3d_sketch.create_center_point_rectangle(sketch_terminal, centerPoint, 'param_e/2', '', adsk.core.Point3D.create(e/2 + b/2, c/2, 0), 'param_b', 'param_c', is_parametric)
            prof_ter = sketch_terminal.profiles.item(0)
        terminal = model_3d_feature.create_extrude(root_comp, prof_ter, -lead_length, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        terminal.name = 'Terminal'
        term_body= terminal.bodies.item(0)
        model_3d_utility.apply_material(app, root_comp.parentDesign, term_body, model_3d_utility.MATERIAL_ID_COPPER_ALLOY)
        model_3d_utility.apply_appearance(app, root_comp.parentDesign, term_body, model_3d_utility.APPEARANCE_ID_NICKEL_POLISHED)
        mirror = model_3d_feature.create_mirror(root_comp, terminal, root_comp.yZConstructionPlane)
        mirror.name = 'Mirror'

def radial_led(params, design = None, target_comp = None):

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
    D = params.get('D') or 0.565 #Body diameter
    A = params.get('A') or 0.86 #Body height(A)
    A1 = params.get('A1') or 0 #Body offset(Not included in body height, A1)
    b = params.get('b') or 0.06 #Lead dia./width for rounded/rectangular lead(b)
    c = params.get('c') or 0.05 #lead thickness used only for rectangular lead(c)
    e = params.get('e') or 0.254 #Pin pitch(e)
    board_thickness = params.get('boardThickness') or 0.16 #Board thickness
    is_parametric = params['isParametric'] if 'isParametric' in params else 1
    isRectangularTerminal = params.get('isRectangularTerminal') or 0

    lead_length = 1.2 * board_thickness + A1

    color_r = params.get('color_r')
    if color_r == None: color_r = 220
    color_g = params.get('color_g')
    if color_g == None: color_g = 0
    color_b = params.get('color_b')
    if color_b == None: color_b = 0

    if is_parametric:
        isUpdate = False
        isUpdate =model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyDiameter", "body diameter"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_A', A, default_unit, _LCLZ("BodyHeight", "body height"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_A1', A1, default_unit, _LCLZ("BodyOffset", "body offset"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("LeadDiameter", "lead diameter"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_c', c, default_unit, _LCLZ("LeadThickness", "lead thickness"))
        isUpdate =model_3d_utility.process_user_param(design, 'param_e', e, default_unit, _LCLZ("PinPitch", "pin pitch"))
        is_update = model_3d_utility.process_user_param(design, 'board_thickness', board_thickness, default_unit, _LCLZ("BoardThickness", "board thickness"))
        if isUpdate:
            #update the color and luminance value
            model_3d_utility.update_emissive_appearance(app, design, 50000.0, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_LED_LIGHT)
            model_3d_utility.update_rgb_appearance(app, design, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_LED_BODY, model_3d_utility.COLOR_PROP_ID_SURFACE)
            model_3d_utility.update_rgb_appearance(app, design, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_LED_BODY, model_3d_utility.COLOR_PROP_ID_TRANSPARENT)
            terminal_ext = root_comp.features.itemByName('Terminal')
            mirror = root_comp.features.itemByName('Mirror')
            terminal_sketch = root_comp.sketches.itemByName('TerminalSketch')
            terminal_plane = root_comp.constructionPlanes.itemByName('TerminalOffset')
            mirror.deleteMe()
            terminal_ext.deleteMe()
            terminal_sketch.deleteMe()
            terminal_plane.deleteMe()

            create_terminals(root_comp, isRectangularTerminal, A1, is_parametric, lead_length, e, b, c)
            terminal = root_comp.features.itemByName('Terminal')
            terminal.timelineObject.rollTo(True)
            dist_def = adsk.fusion.DistanceExtentDefinition.cast(terminal.extentOne)
            dist = adsk.fusion.ModelParameter.cast(dist_def.distance)
            dist.expression = '-1.2 * board_thickness - param_A1'
            design.timeline.moveToEnd()
            return

    #Draw body
    sketches = root_comp.sketches
    low_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1)
    low_body_offset.name = 'LowBodyOffset'

    sketch_body_low = sketches.add(low_body_offset)
    model_3d_sketch.create_center_point_circle(sketch_body_low, adsk.core.Point3D.create(0, 0, 0),  '', '', D, 'param_D', is_parametric)

    lines = sketch_body_low.sketchCurves.sketchLines;
    constraints = sketch_body_low.geometricConstraints
    cut_line1 = lines.addByTwoPoints(sketch_body_low.originPoint, adsk.core.Point3D.create(D/2 * 0.9, 0, 0))
    cut_line1.isConstruction = True
    cut_line2 = lines.addByTwoPoints(cut_line1.endSketchPoint, adsk.core.Point3D.create(D/2 * 0.9, D/4 * 0.9, 0))
    cut_line3 = lines.addByTwoPoints(cut_line1.endSketchPoint, adsk.core.Point3D.create(D/2 * 0.9, -D/4 * 0.9, 0))
    constraints.addHorizontal(cut_line1)
    constraints.addVertical(cut_line2)
    constraints.addVertical(cut_line3)

    if is_parametric:
        sketch_body_low.sketchDimensions.addDistanceDimension(cut_line1.startSketchPoint, cut_line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D / 2  * 0.9'

        sketch_body_low.sketchDimensions.addDistanceDimension(cut_line2.startSketchPoint, cut_line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, D/6, 0)).parameter.expression = 'param_D / 4  * 0.9'

        sketch_body_low.sketchDimensions.addDistanceDimension(cut_line3.startSketchPoint, cut_line3.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, -D/6, 0)).parameter.expression = 'param_D / 4  * 0.9'

    ext_body_low = sketch_body_low.profiles.item(0)
    lower_body = model_3d_feature.create_extrude(root_comp, ext_body_low, 0.2 * A, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    lower_body.name ='LowerBody'

    mid_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1 + 0.2 * A)
    mid_body_offset.name = 'MidBodyOffset'
    sketch_body_mid = sketches.add(mid_body_offset)
    model_3d_sketch.create_center_point_circle(sketch_body_mid,adsk.core.Point3D.create(0, 0, 0), '', '', D * 0.9, 'param_D * 0.9', is_parametric)
    ext_body_mid = sketch_body_mid.profiles.item(0)
    mid_body = model_3d_feature.create_extrude(root_comp, ext_body_mid, 0.8 * A - 0.9 * D/2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    mid_body.name = 'MidBody'

    # create the internal light source
    light_source_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1 + 0.5 * A)
    light_source_offset.name = 'LightSourceOffset'
    sketch_light_source = sketches.add(light_source_offset)
    model_3d_sketch.create_center_point_circle(sketch_light_source,adsk.core.Point3D.create(0, 0, 0), '', '', D * 0.1, 'param_D * 0.1', is_parametric)
    lines = sketch_light_source.sketchCurves.sketchLines
    lineaxis = lines.addByTwoPoints(adsk.core.Point3D.create(0, D/2 * 0.1, 0), adsk.core.Point3D.create(0, -D/2 * 0.1, 0))
    sketch_light_source.geometricConstraints.addVertical(lineaxis)
    sketch_light_source.geometricConstraints.addMidPoint(sketch_light_source.originPoint, lineaxis)
    if is_parametric:
        sketch_light_source.sketchDimensions.addDistanceDimension(lineaxis.startSketchPoint, lineaxis.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, D/4, 0)).parameter.expression = 'param_D * 0.1'
    # Create light source body
    revolves = root_comp.features.revolveFeatures
    rev_input = revolves.createInput(sketch_light_source.profiles.item(0), lineaxis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(math.pi)
    rev_input.setAngleExtent(False, angle)
    light_source = revolves.add(rev_input)
    light_source.name = 'LightSource'
    model_3d_utility.apply_material(app, design, light_source.bodies.item(0),model_3d_utility.MATERIAL_ID_CERAMIC)
    model_3d_utility.apply_emissive_appearance(app, design,  light_source.bodies.item(0), 50000.0, color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_LED_LIGHT)

    # create the top body sketch
    top_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A1 + A - 0.9 * D/2)
    top_body_offset.name = 'TopBodyOffset'
    sketch_body_top = sketches.add(top_body_offset)
    model_3d_sketch.create_center_point_circle(sketch_body_top, adsk.core.Point3D.create(0, 0, 0), '',  '', D * 0.9, 'param_D * 0.9', is_parametric)
    lines = sketch_body_top.sketchCurves.sketchLines;
    lineaxis1 = lines.addByTwoPoints(sketch_body_top.originPoint, adsk.core.Point3D.create(0, D/2 * 0.9, 0))
    lineaxis2 = lines.addByTwoPoints(sketch_body_top.originPoint, adsk.core.Point3D.create(0, -D/2 * 0.9, 0))
    if is_parametric:
        sketch_body_top.sketchDimensions.addDistanceDimension(lineaxis1.startSketchPoint, lineaxis1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, D/4, 0)).parameter.expression = 'param_D / 2  * 0.9'
        sketch_body_top.sketchDimensions.addDistanceDimension(lineaxis2.startSketchPoint, lineaxis2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, -D/4, 0)).parameter.expression = 'param_D / 2  * 0.9'
    ext_body_top = sketch_body_top.profiles.item(0)
    # Create an revolution input
    rev_input = revolves.createInput(ext_body_top, lineaxis1, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(math.pi)
    rev_input.setAngleExtent(False, angle)
    ext_rev = revolves.add(rev_input)

    #Give color to the LED
    body = ext_rev.bodies.item(0)
    body.name = 'Led'
    
    model_3d_utility.apply_material(app, design, body,model_3d_utility.MATERIAL_ID_PLASTIC_TRANSP)
    model_3d_utility.apply_rgb_appearance(app, design, body,color_r, color_g, color_b, model_3d_utility.COLOR_NAME_RADIAL_LED_BODY)


    #Draw terminals
    create_terminals(root_comp, isRectangularTerminal, A1, is_parametric, lead_length, e, b, c)

    #activate the root component. make sure it is not activate the sub component which is lead by the creation of revolve feature. 
    design.activateRootComponent()

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
    radial_led(params, design, targetComponent)
