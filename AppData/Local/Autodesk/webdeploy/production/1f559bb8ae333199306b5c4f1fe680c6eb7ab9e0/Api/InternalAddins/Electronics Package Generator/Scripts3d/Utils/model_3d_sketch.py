"""
this is the utility module which defined several functions to create sketches. 
"""
import adsk.core, adsk.fusion

TERMINAL_THICKNESS_J_LEAD = 0.02  # UNIT is cm

def create_center_point_rectangle(sketch, center_point, param_point_x, param_point_y, end_point, param_horizontal, param_verticle, is_parametric):
    
    sketch.isComputeDeferred = True
    lines = sketch.sketchCurves.sketchLines
    line_count = lines.count
    rect = lines.addCenterPointRectangle(center_point, end_point)

    # Constrain the Rectangle to stay rectangular
    constraints = sketch.geometricConstraints
    constraints.addPerpendicular(lines.item(line_count+0), lines.item(line_count+1))
    constraints.addHorizontal(lines.item(line_count+0))
    constraints.addParallel(lines.item(line_count+0), lines.item(line_count+2))
    constraints.addParallel(lines.item(line_count+1), lines.item(line_count+3))

    # Add construction lines to constrain the rectangle to the center point
    lines = sketch.sketchCurves.sketchLines
    diagonal1 = lines.addByTwoPoints(lines.item(line_count+0).startSketchPoint, lines.item(line_count+2).startSketchPoint)
    diagonal1.isConstruction = True
    diagonal1.isVisible = False
    diagonal2 = lines.addByTwoPoints(lines.item(line_count+1).startSketchPoint, lines.item(line_count+3).startSketchPoint)
    diagonal2.isConstruction = True
    diagonal2.isVisible = False

    # Constrain the rectangle to be centered on the center point
    sketchpoints = sketch.sketchPoints
    sk_center = sketchpoints.add(center_point)

    constraints.addCoincident(sk_center, diagonal1)
    constraints.addCoincident(sk_center, diagonal2)

    if is_parametric:
        # Dimension the rectangle with the user parameters
        if param_point_x == '':
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.value = abs(sk_center.worldGeometry.x)
        else:
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_point_x

        if param_point_y == '':
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.value = abs(sk_center.worldGeometry.y)
        else:
             sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_point_y
               
        if param_horizontal == '':
            sketch.sketchDimensions.addDistanceDimension(lines.item(line_count+0).startSketchPoint, lines.item(line_count+0).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, 1, 0)).parameter.value = abs(sk_center.worldGeometry.x - end_point.worldGeometry.x)*2
        else:    
            sketch.sketchDimensions.addDistanceDimension(lines.item(line_count+0).startSketchPoint, lines.item(line_count+0).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, 1, 0)).parameter.expression = param_horizontal
        
        if param_verticle == '':
            sketch.sketchDimensions.addDistanceDimension(lines.item(line_count+1).startSketchPoint, lines.item(line_count+1).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.value = abs(sk_center.worldGeometry.y - end_point.worldGeometry.y)*2
        else:
            sketch.sketchDimensions.addDistanceDimension(lines.item(line_count+1).startSketchPoint, lines.item(line_count+1).endSketchPoint,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_verticle
    sketch.isComputeDeferred = False
    return rect

###############################################
#Gull Wing Lead

#                                     +                                +
#                                     +<---------+BodyWidth+---------->+

#                                     +--------------------------------+
#                                     |                                |
#                                     |                                |
#                               X+----+                                |
#                              X |   ||                                +--> bodyCenterZ
#                   slope<--+ X X+----+                                |
#           Land(L) <--+     X X      |                                |
#                      |    X X       |                                |
#                  +---+--+X X        |                                |
# terminalThickness|      | X         +---------------+----------------+
#                  +------+X                          |
#                  |                                  |
#                  + <-------+ span/2 +-------------> +


def create_gull_wing_lead(sketch, span, param_span, body_width,  param_body_width, body_center_z, terminal_thickness, L, lead_slope, is_parametric):

    sketch.isComputeDeferred = True
    lines = sketch.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(-span/2, 0, 0), adsk.core.Point3D.create(-span/2+L, 0, 0))
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(-span/2+L+lead_slope, -(body_center_z-terminal_thickness/2), 0))
    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(max(-body_width/2,-span/2+L+lead_slope*2), -(body_center_z-terminal_thickness/2), 0))
    line4 = lines.addByTwoPoints(line3.endSketchPoint, adsk.core.Point3D.create(max(-body_width/2,-span/2+L+lead_slope*2), -(body_center_z+terminal_thickness/2), 0))
    line5 = lines.addByTwoPoints(line4.endSketchPoint, adsk.core.Point3D.create(-span/2+L+lead_slope-terminal_thickness, -(body_center_z+terminal_thickness/2), 0))
    line6 = lines.addByTwoPoints(line5.endSketchPoint, adsk.core.Point3D.create(-span/2+L-terminal_thickness, -terminal_thickness, 0))
    line7 = lines.addByTwoPoints(line6.endSketchPoint, adsk.core.Point3D.create(-span/2, -terminal_thickness, 0))
    line8 = lines.addByTwoPoints(line7.endSketchPoint, adsk.core.Point3D.create(-span/2, 0, 0))
    arc = sketch.sketchCurves.sketchArcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, terminal_thickness)
    arc1 = sketch.sketchCurves.sketchArcs.addFillet(line6, line6.endSketchPoint.geometry, line7, line7.startSketchPoint.geometry, terminal_thickness/4)
    arc2 = sketch.sketchCurves.sketchArcs.addFillet(line5, line5.endSketchPoint.geometry, line6, line6.startSketchPoint.geometry, terminal_thickness)
    arc3 = sketch.sketchCurves.sketchArcs.addFillet(line2, line2.endSketchPoint.geometry, line3, line3.startSketchPoint.geometry, terminal_thickness/4)
    lineC = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, -0.1, 0))
    lineC.isConstruction = True
    lineC.isFixed = True

    if is_parametric:
        #pin dimensions and constraints
        sketch.sketchDimensions.addDistanceDimension(lines.item(0).startSketchPoint, lines.item(0).endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0))
        sketch.sketchDimensions.addDistanceDimension(lines.item(3).startSketchPoint, lines.item(3).endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_terminalThickness'
        sketch.sketchDimensions.addDistanceDimension(lineC.startSketchPoint, lines.item(7).endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_span

        sketch.sketchDimensions.addRadialDimension(arc, adsk.core.Point3D.create(1, 0, 0))
        sketch.sketchDimensions.addRadialDimension(arc1, adsk.core.Point3D.create(1, 0, 0))
        sketch.geometricConstraints.addEqual(arc, arc2)
        sketch.geometricConstraints.addEqual(arc1, arc3)
        sketch.geometricConstraints.addEqual(line8, line4)
        sketch.geometricConstraints.addEqual(line2, line6)
        sketch.geometricConstraints.addCoincident(lines.item(7).endSketchPoint, lines.item(0).startSketchPoint)
        sketch.geometricConstraints.addPerpendicular(line8, line1)
        sketch.geometricConstraints.addPerpendicular(line7, line8)
        sketch.geometricConstraints.addPerpendicular(line3, line4)
        sketch.geometricConstraints.addPerpendicular(line4, line5)

        sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line6.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = 'param_terminalThickness'
        sketch.sketchDimensions.addDistanceDimension(lines.item(3).startSketchPoint, lineC.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_body_width
        sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line5.startSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = '(param_A + param_A1 + param_terminalThickness)/2'
        line1.isFixed = True
        sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(1, 0, 0)).parameter.expression = '(param_L-param_terminalThickness)'
    sketch.isComputeDeferred = False



def create_j_lead(sketch, body_width_E1, param_E1, pin_span_E, param_E, weld_space_E2, param_E2,
                    body_height_A, param_A, body_offset_A1, param_A1, is_parametric):
   
    sketch.isComputeDeferred = True
    # define some common value and parameter names
    circle_out_diameter = pin_span_E - weld_space_E2
    circle_out_diameter_param = param_E + '-' + param_E2
    circle_out_radius = circle_out_diameter /2
    circle_out_radius_param = '('+ circle_out_diameter_param+')/2'


    point_center = adsk.core.Point3D.create(weld_space_E2/2, - circle_out_diameter/2,0)
    # create the outer circle
    circle_out = create_center_point_circle(sketch, point_center, param_E2+'/2', circle_out_radius_param, circle_out_diameter, circle_out_diameter_param, is_parametric)
    # create the inner circle
    circles = sketch.sketchCurves.sketchCircles
    circle_in = circles.addByCenterRadius(circle_out.centerSketchPoint, circle_out_radius - TERMINAL_THICKNESS_J_LEAD)
    # add the diameter constrains for the inner circle
    if(is_parametric):
        sketch.sketchDimensions.addDiameterDimension(circle_in, adsk.core.Point3D.create(-0.1,-0.1, 0), 
                                                        True).parameter.value =  circle_out_diameter - TERMINAL_THICKNESS_J_LEAD*2
    


    point_left = adsk.core.Point3D.create(circle_out.centerSketchPoint.geometry.x+circle_out_radius, circle_out.centerSketchPoint.geometry.y, circle_out.centerSketchPoint.geometry.z)
    point_right = adsk.core.Point3D.create(circle_out.centerSketchPoint.geometry.x-circle_out_radius, circle_out.centerSketchPoint.geometry.y, circle_out.centerSketchPoint.geometry.z)
    point_top = adsk.core.Point3D.create(circle_out.centerSketchPoint.geometry.x,circle_out.centerSketchPoint.geometry.y-circle_out_radius, circle_out.centerSketchPoint.geometry.z)

    #draw a line to cut the circle to semi circle.
    lines = sketch.sketchCurves.sketchLines
    split_line = lines.addByTwoPoints(point_left,point_right)
    geom_constrains = sketch.geometricConstraints
    geom_constrains.addHorizontal(split_line)
    if(is_parametric):
        sketch.sketchDimensions.addDistanceDimension(split_line.startSketchPoint, sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0.1, 0)).parameter.expression = circle_out_radius_param
    # trim the circle to me the half 
    arc_collection = circle_out.trim(point_top)
    arc_out = adsk.fusion.SketchArc.cast(arc_collection.item(0))
    arc_collection = circle_in.trim(point_top)
    arc_in = adsk.fusion.SketchArc.cast(arc_collection.item(0))


    split_lines = split_line.trim(point_center)
    split_line_left = adsk.fusion.SketchLine.cast(split_lines.item(1))
    split_line_right = adsk.fusion.SketchLine.cast(split_lines.item(0))

    body_mid_place_height = (body_height_A + body_offset_A1)/2
    #start create the 2nd profile
    point_out_rect = adsk.core.Point3D.create(pin_span_E/2,-body_mid_place_height-TERMINAL_THICKNESS_J_LEAD,0)
    line_out_ver = lines.addByTwoPoints(split_line_right.startSketchPoint,point_out_rect) 
    point_in_rect = adsk.core.Point3D.create(pin_span_E/2-TERMINAL_THICKNESS_J_LEAD,-body_mid_place_height,0)
    line_in_ver = lines.addByTwoPoints(split_line_right.endSketchPoint,point_in_rect) 

    point_out_end = adsk.core.Point3D.create(body_width_E1/2,-body_mid_place_height-TERMINAL_THICKNESS_J_LEAD,0)
    line_out_hori = lines.addByTwoPoints(line_out_ver.endSketchPoint,point_out_end) 
    point_in_end = adsk.core.Point3D.create(body_width_E1/2,-body_mid_place_height,0)
    line_in_hori = lines.addByTwoPoints(line_in_ver.endSketchPoint,point_in_end) 

    line_end = lines.addByTwoPoints(line_out_hori.endSketchPoint,line_in_hori.endSketchPoint)

    # add line constrains 
    geom_constrains.addHorizontal(line_out_hori)
    geom_constrains.addHorizontal(line_in_hori)
    geom_constrains.addVertical(line_out_ver)
    geom_constrains.addVertical(line_in_ver)
    geom_constrains.addVertical(line_end)

    if is_parametric:
        sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, line_out_ver.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0.1, 0)).parameter.value = body_height_A/2 + body_offset_A1/2 + TERMINAL_THICKNESS_J_LEAD/2 

        sketch.sketchDimensions.addDistanceDimension(line_end.startSketchPoint, line_end.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.1, 0.2, 0)).parameter.value = TERMINAL_THICKNESS_J_LEAD

        sketch.sketchDimensions.addDistanceDimension(line_out_hori.startSketchPoint, line_out_hori.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.2, 0.1, 0)).parameter.expression = '('+ param_E + '-' + param_E1+')/2'    

    sketch.isComputeDeferred = False                       

def create_center_point_circle(sketch,center_point, param_point_x, param_point_y, diameter, param_diameter, is_parametric):
    
    sketch.isComputeDeferred = True
    constraints = sketch.geometricConstraints
    sketchpoints = sketch.sketchPoints
    sk_center = sketchpoints.add(center_point)
    
    # Draw circles and extrude them.
    circles = sketch.sketchCurves.sketchCircles
    circle1 = circles.addByCenterRadius(sk_center,diameter/2)
    #Give the radial dimension
    if is_parametric:

        if param_diameter == '':
            sketch.sketchDimensions.addDiameterDimension(circle1, adsk.core.Point3D.create(diameter/8, diameter/8, 0), 
                                                        True).parameter.value = diameter
        else:
            sketch.sketchDimensions.addDiameterDimension(circle1, adsk.core.Point3D.create(diameter/8, diameter/8, 0), 
                                                        True).parameter.expression = param_diameter
        
        if param_point_x == '':
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, 1, 0)).parameter.value = abs(sk_center.worldGeometry.x)
        else:
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                         adsk.core.Point3D.create(0, 1, 0)).parameter.expression = param_point_x

        if param_point_y == '':
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.value = abs(sk_center.worldGeometry.y)
        else:
             sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, sk_center,
                                                         adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                         adsk.core.Point3D.create(1, 0, 0)).parameter.expression = param_point_y

    sketch.isComputeDeferred = True
    return circle1 


# this function is defined to create pin path for Axial packages 
def create_axial_pin_path(sketch, pin_pitch, param_pin_pitch, body_width,param_body_width, height_over_board, param_height_over_board, total_height, param_total_height, arc_radius, param_arc_radius, is_parametric):
    
    sketch.isComputeDeferred = True
    lines = sketch.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(body_width/2, -height_over_board, 0), adsk.core.Point3D.create(pin_pitch/2, -height_over_board, 0))
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(pin_pitch/2, total_height, 0))
    arc = sketch.sketchCurves.sketchArcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, arc_radius)

    sketch.geometricConstraints.addHorizontal(line1)
    sketch.geometricConstraints.addPerpendicular(line1, line2)

    if is_parametric:
        if param_body_width == '':
            sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.05, 0.1, 0)).parameter.value = body_width/2
        else:
            sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(0.05, 0.1, 0)).parameter.expression = param_body_width+'/2'
    
        if param_height_over_board == '':
            sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-0.05, 0.05, 0)).parameter.value = height_over_board
        else:
            sketch.sketchDimensions.addDistanceDimension(line1.startSketchPoint, sketch.originPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(-0.05, 0.05, 0)).parameter.expression = param_height_over_board

        if param_pin_pitch == '':
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, line2.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(-0.1, 0.05, 0)).parameter.value = pin_pitch/2
        else:
            sketch.sketchDimensions.addDistanceDimension(sketch.originPoint, line2.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                                     adsk.core.Point3D.create(-0.1, 0.05, 0)).parameter.expression = param_pin_pitch+'/2'
    
    
        if param_total_height == '':
            sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0, 0.05, 0)).parameter.value = total_height               
        else:
            sketch.sketchDimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint,
                                                     adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                                     adsk.core.Point3D.create(0, 0.05, 0)).parameter.expression = param_total_height

        if  param_arc_radius == '':
            sketch.sketchDimensions.addRadialDimension(arc, adsk.core.Point3D.create(0, 0.05, 0)).parameter.value = arc_radius
        else:                                                                       
            sketch.sketchDimensions.addRadialDimension(arc, adsk.core.Point3D.create(0, 0.05, 0)).parameter.expression = param_arc_radius

    sketch.isComputeDeferred = False
