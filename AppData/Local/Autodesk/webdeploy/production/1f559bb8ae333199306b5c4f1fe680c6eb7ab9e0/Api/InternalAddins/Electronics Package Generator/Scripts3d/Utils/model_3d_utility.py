
"""
this is the utility module which defined functions to 3d Package generator in general.
"""

import adsk.core
from . import model_3d_feature
from . import model_3d_sketch

# define the materials by using the id 
MATERIAL_LIB_ID = 'C1EEA57C-3F56-45FC-B8CB-A9EC46A9994C'  # 'Fusion 360 Material Library'
MATERIAL_ID_BODY_DEFAULT = 'PrismMaterial-402'  #'Discrete Component' 
MATERIAL_ID_TERMINAL_DEFAULT = 'PrismMaterial-090' #'Copper, Alloy'

MATERIAL_ID_COPPER_ALLOY = 'PrismMaterial-090'
MATERIAL_ID_EPOXY_RESIN = 'PrismMaterial-220'
MATERIAL_ID_PBT_PLASTIC = 'PrismMaterial-277'
MATERIAL_ID_PLASTIC_TRANSP = 'PrismMaterial-052'
MATERIAL_ID_CERAMIC = 'PrismMaterial-213'
MATERIAL_ID_ALUMINUM = 'PrismMaterial-002'
MATERIAL_ID_GLASS = 'PrismMaterial-086'
MATERIAL_ID_DISCRETE_COMP = 'PrismMaterial-402'
MATERIAL_ID_BRASS = 'PrismMaterial-003'
MATERIAL_ID_NYLON = 'PrismMaterial-223'
MATERIAL_ID_TIN = "PrismMaterial-403"
MATERIAL_ID_LEAD_SOLDER = "PrismMaterial-404"
# define the appearance by using the id
APPEARANCE_LIB_ID = 'BA5EE55E-9982-449B-9D66-9F036540E140'  # 'Fusion 360 Appearance Library'
APPEARANCE_ID_BODY_DEFAULT = 'Prism-113'  # 'Plastic - Matte (Black)'
APPEARANCE_ID_TERMINAL_DEFAULT = 'Prism-053' # 'Nickel polished'

APPEARANCE_ID_NICKEL_POLISHED =  'Prism-053'
APPEARANCE_ID_ALUMINUM_POLISHED =  'Prism-027' 
APPEARANCE_ID_GLASS =  'Prism-155' 
APPEARANCE_ID_GLASS_CLEAR =  'Prism-152'
APPEARANCE_ID_GLASS_LIGHT = 'Prism-163'
APPEARANCE_ID_GOLD_POLISHED = 'Prism-052' 
APPEARANCE_ID_EMISSIVE_LED = 'Prism-417'

# define the color property id to get the color
COLOR_PROP_ID_DEFAULT = 'opaque_albedo' # name is 'Color'
COLOR_PROP_ID_SURFACE = 'surface_albedo' # name is 'Color'
COLOR_PROP_ID_TRANSPARENT = 'transparent_color' # name is 'Color'
COLOR_PROP_ID_LUMINANCE = 'opaque_luminance_modifier' # the light color property 
FLOAT_PROP_ID_LUMINANCE = 'opaque_luminance' # the luminance value

# define the customerize color names which will be used in packages
COLOR_NAME_AXIAL_DIODE_BODY = 'Axial Diode Body'
COLOR_NAME_AXIAL_POLAR_CAP_BODY = 'Axial Capacitor Body'
COLOR_NAME_AXIAL_RESISTOR_BODY = 'Axial Resistor Body'
COLOR_NAME_BGA_MID_BODY = 'BGA Middle Body'
COLOR_NAME_CHIP_BODY = 'Chip Body'
COLOR_NAME_MELF_BODY = 'Melf Body'
COLOR_NAME_MELF_BAND = 'Melf Band'
COLOR_NAME_ECAP_BODY = 'ECap Body'
COLOR_NAME_ECAP_BAND = 'ECap Band'
COLOR_NAME_RADIAL_INDUCTOR_BODY = 'Radial Inductor Body'
COLOR_NAME_RADIAL_LED_LIGHT = 'Radial LED'
COLOR_NAME_RADIAL_LED_BODY = 'Radial LED Body'
COLOR_NAME_CHIP_LED_LIGHT = 'Chip LED'
COLOR_NAME_CHIP_LED_CASE = 'Chip LED Case'
COLOR_NAME_SNAP_LOCK_BODY = 'Snap Lock Body'

#convert the internal unit to defualt unit
def convert_internal_to_default_unit(component, value):
    design = component.parentDesign
    default_unit = design.unitsManager.defaultLengthUnits
    result = design.unitsManager.convert(value, 'cm', default_unit)
    return result

# deal with the user paramters in the edit workflow. if it is exist, update it. if it is not exist, create it.
# the return value show the process result, true means update, false means create.
def process_user_param(design, name, value, units, comment):
    user_param = design.userParameters.itemByName(name)
    if user_param:  # the user parameter is already exist. update the value
        if user_param.value == value:
            return True
        else:
            user_param.value = value
            return True
    else:  # the user parameter is not exist, create a new one
        user_value = adsk.core.ValueInput.createByReal(value)
        new_param = design.userParameters.add(name, user_value, units, comment)
        return False


def apply_material(app, design, body, material_id):
    # get materials from current design
    material_in_design = design.materials.itemById(material_id)
    if material_in_design:
        body.material = material_in_design
    else:
        #get the material from library
        material_lib = app.materialLibraries.itemById(MATERIAL_LIB_ID)
        material = material_lib.materials.itemById(material_id)
        if material:
            body.material = material            


# apply appearance to Brep entities
def apply_appearance(app, design, body, appear_id):
    # check if the appear is already in the current design
    appear_in_design = design.appearances.itemById(appear_id)
    if appear_in_design: # assign to the brep entity directly.
        body.appearance = appear_in_design
    else:
        # get the appearance from library
        appear_lib = app.materialLibraries.itemById(APPEARANCE_LIB_ID)
        appear = appear_lib.appearances.itemById(appear_id)
        if appear:
            body.appearance = appear


# apply Emissive appearance to Brep entities
def apply_emissive_appearance(app, design, body, luminance, color_r, color_g, color_b, appear_name):
    
    appear_in_design = design.appearances.itemByName(appear_name)
    if appear_in_design:  # the appearance in design match the name, assign it
        new_appear = appear_in_design
    else:  # the appearance does not exist. get
        # Get the body appearance and create a copy by the given name.
        ref_appear = design.appearances.itemById(APPEARANCE_ID_EMISSIVE_LED)
        if ref_appear:
            new_appear = ref_appear
        else:# find it in lib
            lib = app.materialLibraries.itemById(APPEARANCE_LIB_ID)
            lib_appear = lib.appearances.itemById(APPEARANCE_ID_EMISSIVE_LED)
            new_appear = design.appearances.addByCopy(lib_appear, appear_name)
    
    # update the emissive values to the apprearance 
    rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
    #updatebase body color
    body_color = new_appear.appearanceProperties.itemById(COLOR_PROP_ID_DEFAULT)
    if body_color:
        color_prop = adsk.core.ColorProperty.cast(body_color)
        color_prop.value = rgb    
    #update light color
    light_color = new_appear.appearanceProperties.itemById(COLOR_PROP_ID_LUMINANCE)
    if light_color:
        color_prop = adsk.core.ColorProperty.cast(light_color)
        color_prop.value = rgb
    #update the luminance value
    lumi = new_appear.appearanceProperties.itemById(FLOAT_PROP_ID_LUMINANCE)
    if lumi:
        lumi.value = luminance  
    # assgin the new appearance back to the body
    body.appearance = new_appear

# update the emissive properties in the existing emissive appreance
def update_emissive_appearance(app, design, luminance, color_r, color_g, color_b, appear_name):
    appear_in_design = design.appearances.itemByName(appear_name)
    if appear_in_design:  # the appearance in design match the name, assign it       
        # update the emissive values to the apprearance 
        rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
        #updatebase body color
        body_color = appear_in_design.appearanceProperties.itemById(COLOR_PROP_ID_DEFAULT)
        if body_color:
            color_prop = adsk.core.ColorProperty.cast(body_color)
            color_prop.value = rgb    
        #update light color
        light_color = appear_in_design.appearanceProperties.itemById(COLOR_PROP_ID_LUMINANCE)
        if light_color:
            color_prop = adsk.core.ColorProperty.cast(light_color)
            color_prop.value = rgb
        #update the luminance value
        lumi = appear_in_design.appearanceProperties.itemById(FLOAT_PROP_ID_LUMINANCE)
        if lumi:
            lumi.value = luminance  

# apply new color by customizing the default appearance to Brep entities
def apply_rgb_appearance(app, design, body, color_r, color_g, color_b, appear_name):
    rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
    appear_in_design = design.appearances.itemByName(appear_name)

    if appear_in_design:  # the appearance in design match the name, assign it
        new_appear = appear_in_design
    else:  # the appearance does not exist. get
        # Get the body appearance and create a copy by the given name.
        new_appear = design.appearances.addByCopy(body.appearance, appear_name)

    # get the color property from the new appearance
    prop = new_appear.appearanceProperties.itemById(COLOR_PROP_ID_DEFAULT)
    if prop :
        color_prop = adsk.core.ColorProperty.cast(prop)
        color_prop.value = rgb
    else :
        prop = new_appear.appearanceProperties.itemById(COLOR_PROP_ID_SURFACE)
        if prop :
            color_prop = adsk.core.ColorProperty.cast(prop)
            color_prop.value = rgb
        prop = new_appear.appearanceProperties.itemById(COLOR_PROP_ID_TRANSPARENT)
        if prop :
            color_prop = adsk.core.ColorProperty.cast(prop)
            color_prop.value = rgb
    # assgin the new appearance back to the body
    body.appearance = new_appear

#update the RGB color  in the existing  appreance
def update_rgb_appearance(app, design, color_r, color_g, color_b, appear_name, color_id):
    appear_in_design = design.appearances.itemByName(appear_name)
    if appear_in_design:  # the appearance in design match the name, assign it       
        # update the emissive values to the apprearance 
        rgb = adsk.core.Color.create(color_r, color_g, color_b, 0)
        #updatebase body color
        body_color = appear_in_design.appearanceProperties.itemById(color_id)
        if body_color:
            color_prop = adsk.core.ColorProperty.cast(body_color)
            color_prop.value = rgb

# create an offset construction plane based on the input plane
def create_offset_plane(root_comp, base_plane, offset):
    planes = root_comp.constructionPlanes
    plane_input = planes.createInput()
    offset_distance = adsk.core.ValueInput.createByReal(offset)
    plane_input.setByOffset(base_plane, offset_distance)
    return planes.add(plane_input)


# create the pin one mark feature on the input body
def create_pin_one_mark(root_comp, body_height_A, param_A, body_length_D, body_param_D, body_width_E, body_param_E, is_parametric):

    # step 5. create the pin one mark.
    pin_one_mark_plane_xy = create_offset_plane(root_comp, root_comp.xYConstructionPlane, body_height_A)
    pin_one_mark_plane_xy.name = 'PinOneMarkPlaneXy'
    pin_one_mark_sketch = root_comp.sketches.add(pin_one_mark_plane_xy)

    pin_one_mark_sketch.isComputeDeferred = True
    mark_radius = body_width_E/20
    circle_origin = adsk.core.Point3D.create(-body_width_E/2+ body_width_E/10 + mark_radius, body_length_D/2- body_width_E/10-mark_radius, 0)

    sketch_point = pin_one_mark_sketch.sketchPoints.add(circle_origin)
    pin_one_mark_sketch.sketchCurves.sketchCircles.addByCenterRadius(sketch_point, mark_radius)
    if is_parametric:
        pin_one_mark_sketch.sketchDimensions.addRadialDimension(pin_one_mark_sketch.sketchCurves[0],
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = body_param_E + '/20'
        pin_one_mark_sketch.sketchDimensions.addDistanceDimension(sketch_point, pin_one_mark_sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = body_param_E + '/2-' + param_A+'/10-'+ body_param_E + '/10'
        pin_one_mark_sketch.sketchDimensions.addDistanceDimension(sketch_point, pin_one_mark_sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0, 0)).parameter.expression = body_param_D + '/2-' + param_A+'/10-'+ body_param_E + '/10'

    pin_one_mark_sketch.isComputeDeferred = False
    prof = pin_one_mark_sketch.profiles[0]
    pin_one_mark = root_comp.features.extrudeFeatures.addSimple(prof, adsk.core.ValueInput.createByReal(-body_height_A*0.1), adsk.fusion.FeatureOperations.CutFeatureOperation)
    pin_one_mark.name = 'PinOneMark'
    return pin_one_mark


# get the appearance
def get_appearance(app, design, appear_name):
    
    appearance_in_design = design.appearances.itemByName(appear_name)
    
    if appearance_in_design:  # the appearance in design match the name, return the appreance
        appearance = appearance_in_design
    else:  # the appearance does not exist. get
        # Get a reference to an appearance in the library.
        ref_appearance = design.appearances.itemById(APPEARANCE_ID_BODY_DEFAULT)
        if ref_appearance:
            lib_appearance = ref_appearance
        else:
            lib = app.materialLibraries.itemById(APPEARANCE_LIB_ID)
            lib_appearance = lib.appearances.itemById(APPEARANCE_ID_BODY_DEFAULT)
        # Create a copy of the existing appearance.
        appearance = design.appearances.addByCopy(lib_appearance, appear_name)
    return appearance

#Createing thermal pad
def create_thermal_pad(app, root_comp,plane_offset, center_point, param_x, param_y, end_point, length, width, thickness, thermal_flag, is_parametric ):
    sketches = root_comp.sketches
    thermal_plane_offset = create_offset_plane(root_comp, root_comp.xYConstructionPlane, plane_offset)
    thermal_plane_offset.name = 'ThermalPlaneOffset'
    thermal_sketch = sketches.add(thermal_plane_offset)
    thermal_sketch.name = 'ThermalSketch'
    model_3d_sketch.create_center_point_rectangle(thermal_sketch, center_point , param_x, param_y,  end_point ,
                             length, width, is_parametric)
    thermal_ext = thermal_sketch.profiles.item(0)
    thermal_pad = model_3d_feature.create_extrude(root_comp,thermal_ext, thickness, adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
    thermal_pad.name = 'ThermalPad'
    apply_material(app, root_comp.parentDesign, thermal_pad.bodies.item(0), MATERIAL_ID_ALUMINUM)

    if not thermal_flag:
        thermal_pad.isSuppressed = True

def get_dfn_terminal_thickness(root_comp, A):
    if(A < 0.05):
        terminal_thickness = 0.002
    else:
        terminal_thickness = 0.005
    return terminal_thickness
