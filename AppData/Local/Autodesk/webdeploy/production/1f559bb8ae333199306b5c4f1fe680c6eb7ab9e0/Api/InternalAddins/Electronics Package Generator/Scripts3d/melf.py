import adsk.core,traceback, adsk.fusion, math
from .Utils import model_3d_sketch
from .Utils import model_3d_feature
from .Utils import model_3d_utility
from ..user_preference import _LCLZ

app = adsk.core.Application.get()

def map_model_parameters(root_comp):
    for param in root_comp.modelParameters:
        if param.role=="AlongDistance":
            if param.createdBy.name=="TerminalOffset":
                param.expression = 'param_D/2 '
            if param.createdBy.name == "Terminal":
                param.expression = '-param_L'
            if param.createdBy.name=="EndBodyOffset":
                param.expression = 'param_D/2 - param_L'
            if param.createdBy.name=="inner_body" or param.createdBy.name=="outer_body":
                param.expression = '-(param_D - 2 * param_L)'
            if param.createdBy.name=="BandOffset":
                param.expression = '-param_D/2 + param_L + (param_D - 2 * param_L) * 0.1'
            if param.createdBy.name=="Band":
                param.expression = '(param_D - 2 * param_L) * 0.2'

        if param.role=="Linear Dimension-4":
            if param.createdBy.name=="BandSketch":
                param.value = 0.003  

def melf(params, design = None, target_comp = None):

    E = params.get('E') or 0.16 #Body width(E)
    D = params.get('D') or 0.37 #Body length(D)
    L = params.get('L') or 0.05 #Bandwidth range(L)

    polarityBand = params['isPolarized'] if 'isPolarized' in params else 0 #Polarity Band
    is_parametric = params['isParametric'] if 'isParametric' in params else 1

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
        is_update = False
        isUpdate = model_3d_utility.process_user_param(design, 'param_E', E, default_unit, _LCLZ("BodyWidth", "body width"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_D', D, default_unit, _LCLZ("BodyLength", "body length"))
        isUpdate = model_3d_utility.process_user_param(design, 'param_L', L, default_unit, _LCLZ("BandwidthRange", "bandwidth range"))

        if isUpdate:
            inner_body = root_comp.features.itemByName('InnerBody')
            outer_body = root_comp.features.itemByName('OuterBody')
            band = root_comp.features.itemByName('Band')            
            if polarityBand:
                band.isSuppressed = False
                model_3d_utility.apply_material(app, design, outer_body.bodies.item(0), model_3d_utility.MATERIAL_ID_GLASS)
                model_3d_utility.apply_appearance(app, design, outer_body.bodies.item(0), model_3d_utility.APPEARANCE_ID_GLASS_CLEAR)
                model_3d_utility.apply_rgb_appearance(app, design, inner_body.bodies.item(0),color_r, color_g, color_b, model_3d_utility.COLOR_NAME_MELF_BODY)              
                model_3d_utility.apply_rgb_appearance(app, design, band.bodies.item(0), 10, 10, 10, model_3d_utility.COLOR_NAME_MELF_BAND)
            else:
                band.isSuppressed = True
                model_3d_utility.apply_material(app, design, outer_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
                model_3d_utility.apply_appearance(app, design, outer_body.bodies.item(0),model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)                    
            return

    sketches = root_comp.sketches
    #Create body
    end_body_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.yZConstructionPlane, D/2 - L)
    end_body_offset.name = 'EndBodyOffset'
    end_body_sketch = sketches.add(end_body_offset)
    end_body_sketch.name = 'EndBodySketch'
    
    sketchpoints = end_body_sketch.sketchPoints
    sk_center = sketchpoints.add(adsk.core.Point3D.create(-E/2, 0, 0))
    
    # Draw circles and extrude them.
    circles = end_body_sketch.sketchCurves.sketchCircles
    circle2 = circles.addByCenterRadius(sk_center, E*0.035)
    #Give the radial dimension
    if is_parametric:
        end_body_sketch.sketchDimensions.addDiameterDimension(circle2, adsk.core.Point3D.create(0.02, 0.02, 0), 
                                                        True).parameter.expression = 'param_E * 0.77'
        end_body_sketch.sketchDimensions.addDistanceDimension(end_body_sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, 1, 0)).parameter.expression = 'param_E/2'
        end_body_sketch.sketchDimensions.addDistanceDimension(end_body_sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.expression = '0'
    

    #extrude the bodies
    inner_prof = end_body_sketch.profiles.item(0)
    inner_body = model_3d_feature.create_extrude(root_comp, inner_prof, -(D - 2 * L) , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    inner_body.name = 'InnerBody'
    model_3d_utility.apply_material(app, design, inner_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)


    circle1 = circles.addByCenterRadius(sk_center, E*0.04)
    if is_parametric:
        end_body_sketch.sketchDimensions.addDiameterDimension(circle1, adsk.core.Point3D.create(0.01, 0.01, 0), 
                                                        True).parameter.expression = 'param_E * 0.8'
    #get the proper profile
    for profile_i in end_body_sketch.profiles:
        if profile_i.profileLoops.count == 2: 
            outer_prof = profile_i
    outer_body = model_3d_feature.create_extrude(root_comp, outer_prof, -(D - 2 * L) , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    outer_body.name = 'OuterBody'
    model_3d_utility.apply_material(app, design, outer_body.bodies.item(0), model_3d_utility.MATERIAL_ID_GLASS)

    body_appear = design.appearances.itemByName(model_3d_utility.COLOR_NAME_MELF_BODY)
    if body_appear == None:  # the appearance in design match the name, assign it
        lib = app.materialLibraries.itemById(model_3d_utility.APPEARANCE_LIB_ID)
        lib_appear = lib.appearances.itemById(model_3d_utility.APPEARANCE_ID_ALUMINUM_POLISHED)
        design.appearances.addByCopy(lib_appear, model_3d_utility.COLOR_NAME_MELF_BODY) 
   
    model_3d_utility.apply_rgb_appearance(app, design, inner_body.bodies.item(0),  color_r, color_g, color_b, model_3d_utility.COLOR_NAME_MELF_BODY)

    # Create Terminal
    terminal_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.yZConstructionPlane, D/2)
    terminal_offset.name = 'TerminalOffset'
    terminal_sketch = sketches.add(terminal_offset)

    model_3d_sketch.create_center_point_circle(terminal_sketch, adsk.core.Point3D.create(-E/2, 0, 0),'param_E/2', '0',  E, 'param_E', is_parametric)
    ext_terminal = terminal_sketch.profiles.item(0)
    terminal = model_3d_feature.create_extrude(root_comp,ext_terminal, -L , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    terminal.name = 'Terminal'
    model_3d_utility.apply_material(app, design, terminal.bodies.item(0), model_3d_utility.MATERIAL_ID_TIN)

    model_3d_feature.create_mirror(root_comp, terminal, root_comp.yZConstructionPlane)

    #create band
    band_offset = model_3d_utility.create_offset_plane(root_comp, root_comp.yZConstructionPlane, -D/2 + L + (D - 2 * L) * 0.1)
    band_offset.name = 'BandOffset'
    band_sketch = sketches.add(band_offset)
    band_sketch.name = 'BandSketch'
    E_param = 'param_E * 0.77 + ' + str(model_3d_utility.convert_internal_to_default_unit(root_comp, 0.0003))
    circle = model_3d_sketch.create_center_point_circle(band_sketch, adsk.core.Point3D.create(-E/2, 0, 0),'param_E/2', '0',  E * 0.077 + 0.0003 , E_param, is_parametric)
    ext_band = band_sketch.profiles.item(0)
    band = model_3d_feature.create_extrude(root_comp,ext_band, (D - 2 * L) * 0.2 , adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    band.name = 'Band'
    #apply the band color
    model_3d_utility.apply_material(app, design, band.bodies.item(0), model_3d_utility.MATERIAL_ID_PBT_PLASTIC)
    model_3d_utility.apply_rgb_appearance(app, design, band.bodies.item(0), 10, 10, 10,model_3d_utility.COLOR_NAME_MELF_BAND)

    if not polarityBand:
        band.isSuppressed = True
        model_3d_utility.apply_material(app, design, outer_body.bodies.item(0), model_3d_utility.MATERIAL_ID_CERAMIC)
        model_3d_utility.apply_appearance(app, design, outer_body.bodies.item(0),model_3d_utility.APPEARANCE_ID_BODY_DEFAULT)        

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
    melf(params, design, target_comp)
