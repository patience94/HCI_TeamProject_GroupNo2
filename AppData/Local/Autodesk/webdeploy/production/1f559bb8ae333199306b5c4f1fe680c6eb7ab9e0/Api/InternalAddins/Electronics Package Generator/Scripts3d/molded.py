import adsk.core, adsk.fusion, traceback, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    offset_name = str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.015))
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="Body":
                param.expression = 'param_A -' + offset_name #need convert the value to default unit
            if param.createdBy.name=="OddTerminalVert":
                param.expression = 'param_A/2 +' + offset_name #need convert the value to default unit
            if param.createdBy.name=="EvenTerminalVert":
                param.expression = 'param_A/2 +' + offset_name #need convert the value to default unit
            if param.createdBy.name=="BandOffset":
                param.expression = 'param_A'
        if param.role=="leftDistance":
            if param.createdBy.name=="Chamfer1":
                param.expression = '0.05 * param_A'
        if param.role=="rightDistance":
            if param.createdBy.name=="Chamfer1":
                param.expression = 'param_A/2 -' + offset_name #need convert the value to default unit

def create_chamfer(root_comp, ext, dist1, dist2):
        edge_top = adsk.core.ObjectCollection.create()
        top_face = ext.endFaces[0]
        top_edges = top_face.edges
        for edgeI  in top_edges:
            edge_top.add(edgeI)

        chamfer_feats = root_comp.features.chamferFeatures
        chamfer_top = chamfer_feats.createInput(edge_top, True)
        chamfer_top.setToTwoDistances(adsk.core.ValueInput.createByReal(dist1), adsk.core.ValueInput.createByReal(dist2))
        chamfer_feats.add(chamfer_top)

def molded(params, design = None, target_comp = None):

    A = params.get('A') or 0.43 # body height(A)
    b = params.get('b') or 0.25 # Normal terminal width (b)
    b1 = params.get('b1') or 0.25 # Odd terminal width(b1)
    D = params.get('D') or 0.76 # body length (D)
    E = params.get('E') or 0.46 # body width (E)
    L = params.get('L') or 0.16 # Normal terminal length(L)
    L1 = params.get('L1') or 0.16 #Odd terminal length (L1)
    EPins = params.get('EPins') or 2 #Total pin count

    h = 1/2 * A #Terminal feet height(h)
    # Terminal thickness
    c = 0.015
    if ('terminalThickness' not in params):
        terminal_thickness = c
    else:
        if (params['terminalThickness'] < 0):
            terminal_thickness = c
        else:
            terminal_thickness = min(params['terminalThickness'] , c)

    polarityBand = params['isPolarized'] if 'isPolarized' in params else 0 # Polarity band
    is_parametric = params['isParametric'] if 'isParametric' in params else 1
    s = 0.05 * A

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
        isUpdate = model_3d_utility.process_user_param(design, 'param_b', b, default_unit, _LCLZ("NormalTerminalWidth", "normal terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_b1', b1, default_unit, _LCLZ("OddTerminalWidth", "odd terminal width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("NormalTerminalLength", "normal terminal length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L1', L1, default_unit, _LCLZ("OddTerminalLength", "odd terminal length"))
        if isUpdate:
            band = root_comp.features.itemByName('Band')
            if polarityBand:
                band.isSuppressed = False
            else:
                band.isSuppressed = True
            return

    #Create body
    sketches = root_comp.sketches
    body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, terminal_thickness)
    body_offset.name = 'BodyOffset'
    body_sketch = sketches.add(body_offset)
    body_sketch.name = 'BodySketch'
    model_3d_sketch.create_center_point_rectangle(body_sketch, adsk.core.Point3D.create(0, 0, 0), '', '', adsk.core.Point3D.create(D/2, E/2, 0), 'param_D', 'param_E', is_parametric)
    ext_body = body_sketch.profiles.item(0)
    body = model_3d_feature.create_extrude(root_comp,ext_body, A - terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    body.name = 'Body'
    model_3d_utility.apply_material(app, design, body.bodies.item(0), model_3d_utility.MATERIAL_ID_BODY_DEFAULT)
    create_chamfer(root_comp, body, A/2 - c, s)


    #Draw terminals
    xyPlane = root_comp.xYConstructionPlane
    odd_pin_sketch = sketches.add(xyPlane)
    offset_name = str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.015))
    model_3d_sketch.create_center_point_rectangle(odd_pin_sketch, adsk.core.Point3D.create(D/2 - L1/2 + terminal_thickness, 0, 0), 'param_D/2 - param_L1/2 +' + offset_name, '' ,
                                                adsk.core.Point3D.create(D/2 + terminal_thickness, b1/2, 0), 'param_L1', 'param_b1', is_parametric)
    lines = odd_pin_sketch.sketchCurves.sketchLines;
    line_odd1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(D/2 , 0, 0))
    constraints = odd_pin_sketch.geometricConstraints
    line_odd1.startSketchPoint.isfixed = True
    line_odd1.isConstruction = True
    constraints.addCoincident(line_odd1.startSketchPoint, odd_pin_sketch.originPoint)
    if is_parametric:
        odd_pin_sketch.sketchDimensions.addDistanceDimension(line_odd1.startSketchPoint, line_odd1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D/2 '

    line_odd2 = lines.addByTwoPoints(line_odd1.endSketchPoint, adsk.core.Point3D.create(D/2 , b1/2, 0))
    if is_parametric:
        odd_pin_sketch.sketchDimensions.addDistanceDimension(line_odd2.startSketchPoint, line_odd2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(D/2 , b1, 0)).parameter.expression = 'param_b1/2'

    line_odd3 = lines.addByTwoPoints(line_odd1.endSketchPoint, adsk.core.Point3D.create(D/2 , -b1/2, 0))
    if is_parametric:
        odd_pin_sketch.sketchDimensions.addDistanceDimension(line_odd3.startSketchPoint, line_odd3.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-D/2 , -b1, 0)).parameter.expression = 'param_b1/2'
    constraints.addHorizontal(line_odd1)
    constraints.addVertical(line_odd2)
    constraints.addVertical(line_odd3)

    ext_odd_ter_hori = odd_pin_sketch.profiles.item(0)
    odd_terminal_hori = model_3d_feature.create_extrude(root_comp,ext_odd_ter_hori, terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    odd_terminal_hori.name = 'OddTerminalHori'
    model_3d_utility.apply_material(app, design, odd_terminal_hori.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    ext_odd_ter = odd_pin_sketch.profiles.item(1)
    odd_terminal_vert = model_3d_feature.create_extrude(root_comp,ext_odd_ter, A/2 + terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    odd_terminal_vert.name = 'OddTerminalVert'
    model_3d_utility.apply_material(app, design, odd_terminal_vert.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    even_pin_sketch = sketches.add(xyPlane)
    model_3d_sketch.create_center_point_rectangle(even_pin_sketch, adsk.core.Point3D.create(-D/2 + L/2 - terminal_thickness, 0, 0), 'param_D/2 - param_L/2 +'+ offset_name, '' ,
                                                 adsk.core.Point3D.create(-D/2 - terminal_thickness, b/2, 0), 'param_L', 'param_b', is_parametric)
    lines = even_pin_sketch.sketchCurves.sketchLines;
    line_even1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-D/2 , 0, 0))
    constraints = even_pin_sketch.geometricConstraints
    line_even1.startSketchPoint.isfixed = True
    line_even1.isConstruction = True
    constraints.addCoincident(line_even1.startSketchPoint, even_pin_sketch.originPoint)
    if is_parametric:
        even_pin_sketch.sketchDimensions.addDistanceDimension(line_even1.startSketchPoint, line_even1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D/2 '

    line_even2 = lines.addByTwoPoints(line_even1.endSketchPoint, adsk.core.Point3D.create(-D/2 , b/2, 0))
    if is_parametric:
        even_pin_sketch.sketchDimensions.addDistanceDimension(line_even2.startSketchPoint, line_even2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(D/2 , b, 0)).parameter.expression = 'param_b/2'

    line_even3 = lines.addByTwoPoints(line_even1.endSketchPoint, adsk.core.Point3D.create(-D/2 , -b/2, 0))
    if is_parametric:
        even_pin_sketch.sketchDimensions.addDistanceDimension(line_even3.startSketchPoint, line_even3.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-D/2 , -b, 0)).parameter.expression = 'param_b/2'
    constraints.addHorizontal(line_even1)
    constraints.addVertical(line_even2)
    constraints.addVertical(line_even3)

    ext_even_ter_hori = even_pin_sketch.profiles.item(0)
    even_terminal_hori = model_3d_feature.create_extrude(root_comp,ext_even_ter_hori, terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    even_terminal_hori.name = 'EvenTerminalHori'
    model_3d_utility.apply_material(app, design, even_terminal_hori.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    ext_even_ter = even_pin_sketch.profiles.item(1)
    even_terminal_vert = model_3d_feature.create_extrude(root_comp,ext_even_ter, A/2 + terminal_thickness , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    even_terminal_vert.name = 'EvenTerminalVert'
    model_3d_utility.apply_material(app, design, even_terminal_vert.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    #draw polarity band
    band_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.xYConstructionPlane, A)
    band_offset.name = 'BandOffset'
    band_sketch = sketches.add(band_offset)
    band_sketch.name = 'BandSketch'
    model_3d_sketch.create_center_point_rectangle(band_sketch, adsk.core.Point3D.create(0, 0, 0), '' ,'' ,
                                             adsk.core.Point3D.create(D/2 + s, E/2 - s, 0), 'param_D - 0.1 * param_A', 'param_E - 0.1 * param_A', is_parametric)

    lines = band_sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(-D/2 + 0.05 * A + 0.15 , 0, 0))
    constraints = band_sketch.geometricConstraints
    line1.startSketchPoint.isfixed = True
    line1.isConstruction = True
    constraints.addCoincident(line1.startSketchPoint, band_sketch.originPoint)
    if is_parametric:
        band_sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(D/4, 0, 0)).parameter.expression = 'param_D/2 - 0.05 * param_A -'+ str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.15))

    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-D/2 + 0.05 * A + 0.15 , E/2 - s, 0))
    if is_parametric:
        band_sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-D/2 + 0.05 * A + 0.15, b/2, 0)).parameter.expression = 'param_E/2 - 0.05 * param_A'

    line3 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-D/2 + 0.05 * A + 0.15 , -E/2 + s, 0))
    if is_parametric:
        band_sketch.sketchDimensions.addDistanceDimension(line3.startSketchPoint, line3.endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                        adsk.core.Point3D.create(-D/2 + 0.05 * A + 0.15 , -b/2, 0)).parameter.expression = 'param_E/2 - 0.05 * param_A'
    constraints.addHorizontal(line1)
    constraints.addVertical(line2)
    constraints.addVertical(line3)

    ext_band = band_sketch.profiles.item(0)
    band = model_3d_feature.create_extrude(root_comp,ext_band, 0.0002 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    band.name = 'Band'
    model_3d_utility.apply_appearance(app, design, band.bodies.item(0), model_3d_utility.APPEARANCE_ID_ALUMINUM_POLISHED)

    if not polarityBand:
        band.isSuppressed = True

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
    molded(params, design, target_comp)
